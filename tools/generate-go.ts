import {
    quicktype,
    InputData,
    jsonInputForTargetLanguage,
    JSONSchemaInput,
    FetchingJSONSchemaStore
} from "quicktype-core";
import * as fs from "fs";
import * as path from "path";

// Mapping of Type Name to Output Filename
const TYPE_TO_FILE: Record<string, string> = {
    "Artifact": "artifact.go",
    "ArtifactMetadata": "artifact.go",
    "Body": "artifact.go",
    "AuditEvent": "audit.go",
    "AuditDest": "audit.go", // Helper types if any

    "EngineInput": "engine.go",
    "EngineOutput": "engine.go",
    "EngineMeta": "engine.go",
    "EngineOrchestrator": "engine.go",
    "EngineArtifact": "engine.go",
    "EngineMetric": "engine.go",

    "LLMGatewayRequest": "gateway_llm.go",
    "LLMGatewayResponse": "gateway_llm.go",
    "LLMGatewayPolicyConfig": "gateway_llm.go",
    "GatewayApproval": "gateway_llm.go", // Shared but used here mostly
    "LLMGatewayRule": "gateway_llm.go",
    // Gateway LLM Extras
    "ModelRoutingClass": "gateway_llm.go",
    "LLMGatewayResponseApproval": "gateway_llm.go",
    "LLMGatewayResponseDecision": "gateway_llm.go",

    "MCPGatewayRequest": "gateway_mcp.go",
    "MCPGatewayResponse": "gateway_mcp.go",
    "MCPGatewayPolicyConfig": "gateway_mcp.go",
    "MCPGatewayRule": "gateway_mcp.go",
    "MCPGatewayResponseApproval": "gateway_mcp.go",
    "ParamsClass": "gateway_mcp.go", // Assuming it belongs here

    "PreflightInput": "orchestrator.go",
    "PreflightOutput": "orchestrator.go",
    "ApprovalRequest": "orchestrator.go",
    "ApprovalResponse": "orchestrator.go",
    "WorkflowState": "orchestrator.go",
    "PreflightEvidence": "orchestrator.go",
    "PreflightRequires": "orchestrator.go",

    "PlanToken": "plantoken.go",
    "PlanArtifactHash": "plantoken.go"
};

const SCHEMAS_DIR = path.resolve(__dirname, "../schemas/draft");
const GO_OUT_DIR = path.resolve(__dirname, "../lib/go/cabincrew");

async function generate() {
    console.log("Generating Go library...");

    // Clean up old files
    if (fs.existsSync(GO_OUT_DIR)) {
        const oldFiles = fs.readdirSync(GO_OUT_DIR).filter(f => f.endsWith(".go"));
        for (const f of oldFiles) {
            fs.unlinkSync(path.join(GO_OUT_DIR, f));
        }
    } else {
        fs.mkdirSync(GO_OUT_DIR, { recursive: true });
    }

    const files = fs.readdirSync(SCHEMAS_DIR).filter(f => f.endsWith(".json"));
    const inputData = new InputData();
    const schemaInput = new JSONSchemaInput(new FetchingJSONSchemaStore());

    for (const file of files) {
        const schemaPath = path.join(SCHEMAS_DIR, file);
        const schemaContent = fs.readFileSync(schemaPath, "utf8");
        const schema = JSON.parse(schemaContent);
        const typeName = schema.title || file.replace(".schema.json", "").replace(".json", "");
        await schemaInput.addSource({ name: typeName, schema: schemaContent });
    }

    inputData.addInput(schemaInput);

    const { lines: goCode } = await quicktype({
        inputData,
        lang: "go",
        rendererOptions: {
            "package": "cabincrew",
            "just-types": "true" // Try to skip marshaling code
        }
    });

    // 1. Join lines to do global replacements
    let fullCode = goCode.join("\n");

    // Replace Quicktype generated names for duplicates
    // We assume the "clean" name is the target.
    // Common prefixes quicktype uses: Purple, Fluffy, Tentacled, Sticky, Indigo, Indecent, Hilarious, etc.
    // We'll mostly see Purple/Fluffy/PlanTokenArtifact (which is a rename).
    // Let's force rename typical collisions back to their base name.

    const collisionRenames: Record<string, string> = {
        "PurplePlanArtifactHash": "PlanArtifactHash",
        "FluffyPlanArtifactHash": "PlanArtifactHash",
        "PlanTokenArtifact": "PlanArtifactHash",
        "PreflightInputPlanToken": "PlanToken",
        // Add others if seen
    };

    for (const [bad, good] of Object.entries(collisionRenames)) {
        // Replace "type Bad " with "type Good "
        // Replace "Bad{" with "Good{" (initialization - though we strip funcs so maybe not)
        // Replace " []Bad" with " []Good"
        // Replace " *Bad" with " *Good"
        // Replace " Bad " with " Good "

        // Simplest: Global string replace. Might be dangerous if "Bad" is a common substring, 
        // but these names are quite specific.
        fullCode = fullCode.split(bad).join(good);
    }

    const lines = fullCode.split("\n");

    // Content buffers for each file
    const fileContents: Record<string, string[]> = {};
    const getFileBuffer = (fname: string) => {
        if (!fileContents[fname]) {
            fileContents[fname] = [
                "package cabincrew",
                "",
            ];
        }
        return fileContents[fname];
    };

    let currentBlock: string[] = [];
    let currentTypeDisplayName = "";

    // Track defined types to prevent duplicates
    const definedTypes = new Set<string>();

    for (const line of lines) {
        if (line.startsWith("package ")) continue;
        if (line.startsWith("import ")) continue;
        if (line.startsWith("func ")) continue; // Skip funcs

        const typeMatch = line.match(/^type\s+([A-Z][a-zA-Z0-9_]*)\s+/);
        if (typeMatch) {
            // Flush previous block
            if (currentBlock.length > 0) {
                // If the block is a Container, skip it
                // Containers usually match the Schema Filename logic, e.g. "EngineSchema", "LlmGateway"
                // Or "OrchestratorSchema"

                const isContainer = ["EngineSchema", "LlmGateway", "McpGateway", "MCPGateway", "OrchestratorSchema", "PlanTokenSchema", "ArtifactSchema", "AuditEventSchema"].includes(currentTypeDisplayName);

                if (!isContainer && !definedTypes.has(currentTypeDisplayName)) {
                    const f = TYPE_TO_FILE[currentTypeDisplayName];
                    if (f) {
                        getFileBuffer(f).push(...currentBlock);
                        definedTypes.add(currentTypeDisplayName);
                    } else {
                        // If not mapped, it might be a generated enum or auxiliary type.
                        // Try to guess from prefix?
                        // If we strictly don't want shared.go, we should warn.
                        // For now, let's map unmapped Enums like "Severity" to audit.go if possible.

                        let guessedFile = "shared.go";
                        if (currentTypeDisplayName.startsWith("Audit")) guessedFile = "audit.go";
                        else if (currentTypeDisplayName.startsWith("Preflight")) guessedFile = "orchestrator.go";
                        else if (currentTypeDisplayName.startsWith("Engine")) guessedFile = "engine.go";
                        else if (currentTypeDisplayName === "Severity") guessedFile = "audit.go";
                        else if (currentTypeDisplayName === "Mode") guessedFile = "engine.go"; // or orchestrator
                        else if (currentTypeDisplayName === "State") guessedFile = "orchestrator.go";
                        else if (currentTypeDisplayName === "Body") guessedFile = "artifact.go";
                        else if (currentTypeDisplayName.startsWith("LLMGateway")) guessedFile = "gateway_llm.go";

                        // If specifically "AnyMap", it's shared, but maybe put in engine since usage is heavy there?
                        // Or create a common.go that IS allowed?
                        // User said "shared.go is a sign of misalignment".
                        // AnyMap is truly common. Maybe replicate it or put in artifact?
                        // Let's put AnyMap in audit.go for now or engine? engine.go seems fine.
                        else if (currentTypeDisplayName === "AnyMap") guessedFile = "engine.go";

                        if (guessedFile !== "shared.go") {
                            getFileBuffer(guessedFile).push(...currentBlock);
                            definedTypes.add(currentTypeDisplayName);
                        } else {
                            console.warn(`Warning: Unmapped type ${currentTypeDisplayName} going to shared.go`);
                            getFileBuffer("shared.go").push(...currentBlock);
                            definedTypes.add(currentTypeDisplayName);
                        }
                    }
                }
                currentBlock = [];
            }

            currentTypeDisplayName = typeMatch[1];
        }

        if (line.match(/^func\s+\(/)) continue;

        if (line === "}") {
            currentBlock.push(line);

            // Process block immediately to handle logic above cleanly? 
            // Logic is "Flush previous". This handles the block END.
            // We need to trigger the flush logic for this block next time we see "type" or at EOF.
            continue;
        }

        currentBlock.push(line);
    }

    // Flush last block
    if (currentBlock.length > 0) {
        const isContainer = ["EngineSchema", "LlmGateway", "McpGateway", "OrchestratorSchema"].includes(currentTypeDisplayName);
        if (!isContainer && !definedTypes.has(currentTypeDisplayName)) {
            const f = TYPE_TO_FILE[currentTypeDisplayName] || "shared.go"; // Fallback logic needed here too?
            // Since we duped logic, best to refactor or just copy paste lightly for now
            let target = f;
            if (target === "shared.go") {
                if (currentTypeDisplayName === "Severity") target = "audit.go";
                else if (currentTypeDisplayName === "Mode") target = "engine.go";
                else if (currentTypeDisplayName === "State") target = "orchestrator.go";
                else if (currentTypeDisplayName === "Body") target = "artifact.go";
            }
            getFileBuffer(target).push(...currentBlock);
        }
    }

    // Write files
    for (const [fname, lines] of Object.entries(fileContents)) {
        const content = lines.join("\n");
        // If shared.go has no types, skip it
        if (fname === "shared.go" && !content.includes("type ")) {
            console.log("Skipping empty shared.go");
            continue;
        }

        const outPath = path.join(GO_OUT_DIR, fname);
        fs.writeFileSync(outPath, content);
        console.log(`Generated ${fname}`);
    }
}

generate().catch(console.error);
