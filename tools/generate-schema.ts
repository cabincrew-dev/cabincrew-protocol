import * as TJS from "typescript-json-schema";
import * as fs from "fs";
import * as path from "path";

const SCHEMA_FILE = path.resolve(__dirname, "../schemas/draft/schema.json");
const DOCS_FILE = path.resolve(__dirname, "../schemas/draft/schema.mdx");
const SRC_FILE = path.resolve(__dirname, "../src/index.ts");

// Type categories for documentation organization
const CATEGORIES = {
    "JSON-RPC": ["EngineInput", "EngineOutput", "EngineMeta", "EngineOrchestrator", "EngineArtifact", "EngineMetric"],
    "Orchestration": ["PreflightInput", "PreflightOutput", "ApprovalRequest", "ApprovalResponse", "WorkflowState", "PreflightEvidence", "PreflightRequires"],
    "Security": ["PlanToken", "PlanArtifactHash", "AuditEvent", "AuditDest", "AuditWorkflow", "AuditEngine", "AuditArtifact", "AuditPolicy", "AuditApproval", "AuditIntegrity", "AuditGateway"],
    "Gateways": ["LLMGatewayRequest", "LLMGatewayResponse", "LLMGatewayPolicyConfig", "LLMGatewayRule", "GatewayApproval", "MCPGatewayRequest", "MCPGatewayResponse", "MCPGatewayPolicyConfig", "MCPGatewayRule"],
    "Common Types": ["Artifact", "Body", "Mode", "Decision", "State", "Severity", "AnyMap", "RecordStringAny"]
};

function generate() {
    console.log("Generating monolithic schema...");

    // Ensure output directories exist
    const schemasDir = path.dirname(SCHEMA_FILE);
    const docsDir = path.dirname(DOCS_FILE);
    if (!fs.existsSync(schemasDir)) fs.mkdirSync(schemasDir, { recursive: true });
    if (!fs.existsSync(docsDir)) fs.mkdirSync(docsDir, { recursive: true });

    const settings: TJS.PartialArgs = {
        required: true,
        noExtraProps: true,
        ignoreErrors: true,
    };

    const compilerOptions = {
        strictNullChecks: true,
        target: 99 as any, // ES2020
    };

    const program = TJS.getProgramFromFiles([SRC_FILE], compilerOptions);
    let schema = TJS.generateSchema(program, "*", settings);

    if (!schema) {
        throw new Error("Failed to generate schema");
    }

    // Post-process schema to fix RecordStringAny
    // RecordStringAny should allow arbitrary properties, but typescript-json-schema
    // generates it with additionalProperties: {} (empty object) due to index signature
    if (schema.definitions?.RecordStringAny && typeof schema.definitions.RecordStringAny === 'object') {
        const recordDef = schema.definitions.RecordStringAny as any;
        recordDef.additionalProperties = true;
        // Remove the empty properties object if it exists
        delete recordDef.properties;
    }

    // Post-process schema to remove duplicate Record<string,any> type
    // typescript-json-schema creates both RecordStringAny and Record<string,any>
    // We need to redirect all references to RecordStringAny and remove the duplicate
    const schemaStr = JSON.stringify(schema);
    const fixedSchemaStr = schemaStr
        .replace(/#\/definitions\/Record<string,any>/g, '#/definitions/RecordStringAny')
        .replace(/"Record<string,any>":\s*\{[^}]*\},?/g, ''); // Remove the duplicate definition
    schema = JSON.parse(fixedSchemaStr);

    // Write schema file
    fs.writeFileSync(SCHEMA_FILE, JSON.stringify(schema, null, 2));
    console.log(`Generated ${SCHEMA_FILE}`);

    // Generate documentation
    generateDocs(schema);
}

function generateDocs(schema: any) {
    let mdx = "# Schema Reference\n\n";

    for (const [category, typeNames] of Object.entries(CATEGORIES)) {
        mdx += `{/* @category ${category} */}\n`;
        mdx += `## ${category}\n\n`;

        for (const typeName of typeNames) {
            const typeDef = schema.definitions?.[typeName];
            if (!typeDef) continue;

            mdx += `### ${typeName}\n\n`;

            if (typeDef.description) {
                mdx += `${typeDef.description}\n\n`;
            }

            if (typeDef.properties) {
                mdx += renderProperties(typeDef.properties, typeDef.required || []);
            } else if (typeDef.enum) {
                mdx += `**Enum values**: ${typeDef.enum.map((v: any) => `\`${v}\``).join(", ")}\n\n`;
            }
        }
    }

    fs.writeFileSync(DOCS_FILE, mdx);
    console.log(`Generated ${DOCS_FILE}`);
}

function renderProperties(props: any, required: string[] = []) {
    let md = "| Property | Type | Required | Description |\n";
    md += "|---|---|---|---|\n";

    for (const [key, value] of Object.entries(props)) {
        const v = value as any;
        let type = v.type;

        if (!type && v.$ref) type = `[${v.$ref.split('/').pop()}]`;
        if (v.anyOf || v.oneOf) type = "complex";
        if (Array.isArray(type)) type = type.join(" | ");
        if (!type) type = "any";

        const req = required.includes(key) ? "Yes" : "No";
        const desc = (v.description || "").replace(/\n/g, " ");
        md += `| \`${key}\` | \`${type}\` | ${req} | ${desc} |\n`;
    }
    return md + "\n";
}

generate();
