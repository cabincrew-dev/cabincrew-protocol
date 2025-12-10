import {
    quicktype,
    InputData,
    jsonInputForTargetLanguage,
    JSONSchemaInput,
    FetchingJSONSchemaStore
} from "quicktype-core";
import * as fs from "fs";
import * as path from "path";

// Mapping of Type Name to Output Filename (no extension)
const TYPE_TO_MODULE: Record<string, string> = {
    "Artifact": "artifact",
    "ArtifactMetadata": "artifact",
    "Body": "artifact",

    "AuditEvent": "audit",
    "AuditDest": "audit",
    "AuditWorkflow": "audit",
    "AuditEngine": "audit",
    "AuditArtifact": "audit",
    "AuditPolicy": "audit",
    "AuditApproval": "audit",
    "AuditIntegrity": "audit",
    "AuditGateway": "audit",
    "Severity": "audit",

    "EngineInput": "engine",
    "EngineOutput": "engine",
    "EngineMeta": "engine",
    "EngineOrchestrator": "engine",
    "EngineArtifact": "engine",
    "EngineMetric": "engine",
    "Mode": "engine",
    "AnyMap": "engine",

    "LLMGatewayRequest": "gateway_llm",
    "LLMGatewayResponse": "gateway_llm",
    "LLMGatewayPolicyConfig": "gateway_llm",
    "GatewayApproval": "gateway_llm",
    "LLMGatewayRule": "gateway_llm",
    "ModelRoutingClass": "gateway_llm",
    "LLMGatewayResponseApproval": "gateway_llm",
    "LLMGatewayResponseDecision": "gateway_llm",
    "LlmGateway": "gateway_llm", // Container

    "MCPGatewayRequest": "gateway_mcp",
    "MCPGatewayResponse": "gateway_mcp",
    "MCPGatewayPolicyConfig": "gateway_mcp",
    "MCPGatewayRule": "gateway_mcp",
    "MCPGatewayResponseApproval": "gateway_mcp",
    "ParamsClass": "gateway_mcp",
    "McpGateway": "gateway_mcp", // Container
    "MCPGateway": "gateway_mcp", // Container Cap variation

    "PreflightInput": "orchestrator",
    "PreflightOutput": "orchestrator",
    "ApprovalRequest": "orchestrator",
    "ApprovalResponse": "orchestrator",
    "WorkflowState": "orchestrator",
    "PreflightEvidence": "orchestrator",
    "PreflightRequires": "orchestrator",
    "State": "orchestrator",
    "PreflightOutputDecision": "orchestrator",
    "OrchestratorSchema": "orchestrator", // Container

    "PlanToken": "plantoken",
    "PlanArtifactHash": "plantoken",
    "PlanTokenSchema": "plantoken" // Container
};

// Container types to exclude from output if desired, similar to Go script.
// However, in Python sometimes we might want them? 
// Go script excluded them to avoid strict typing redundant roots.
// Let's exclude them to be consistent.
const EXCLUDED_TYPES = new Set([
    "EngineSchema",
    "LlmGateway",
    "McpGateway",
    "MCPGateway",
    "OrchestratorSchema",
    "PlanTokenSchema",
    "ArtifactSchema",
    "AuditEventSchema"
]);

const SCHEMAS_DIR = path.resolve(__dirname, "../schemas/draft");
const PYTHON_OUT_DIR = path.resolve(__dirname, "../lib/python/src/cabincrew_protocol");

if (!fs.existsSync(PYTHON_OUT_DIR)) fs.mkdirSync(PYTHON_OUT_DIR, { recursive: true });

async function generate() {
    console.log("Generating Python library...");

    // Clean up old files
    if (fs.existsSync(PYTHON_OUT_DIR)) {
        const oldFiles = fs.readdirSync(PYTHON_OUT_DIR).filter(f => f.endsWith(".py") && f !== "__init__.py");
        for (const f of oldFiles) {
            fs.unlinkSync(path.join(PYTHON_OUT_DIR, f));
        }
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

    const { lines: pythonCode } = await quicktype({
        inputData,
        lang: "python",
        rendererOptions: {
            "just-types": "false"
        }
    });

    let fullCode = pythonCode.join("\n");

    // Replacements
    const collisionRenames: Record<string, string> = {
        "PurplePlanArtifactHash": "PlanArtifactHash",
        "FluffyPlanArtifactHash": "PlanArtifactHash",
        "PlanTokenArtifact": "PlanArtifactHash",
        "PreflightInputPlanToken": "PlanToken",
    };
    for (const [bad, good] of Object.entries(collisionRenames)) {
        fullCode = fullCode.split(bad).join(good);
    }

    // Parsing blocks
    const lines = fullCode.split("\n");
    const blocks: Record<string, string[]> = {};
    const globals: string[] = [];

    let currentBlockName = "";
    let currentBlockLines: string[] = [];

    // Regex for start of block (class or def)
    const blockStartRegex = /^(class|def)\s+([a-zA-Z0-9_]+)/;

    for (const line of lines) {
        // Empty lines - attach to current block if active, else global
        if (line.trim() === "") {
            if (currentBlockName) currentBlockLines.push(line);
            else globals.push(line);
            continue;
        }

        const match = line.match(blockStartRegex);
        if (match) {
            // New block starts
            if (currentBlockName) {
                blocks[currentBlockName] = currentBlockLines;
            }
            currentBlockName = match[2];
            currentBlockLines = [line];
        } else {
            // Continuation logic
            // If it starts with space/tab, it belongs to block
            // If it starts with @, it behaves like preamble to next block? 
            // Quicktype puts decorators @dataclass usually right before class.

            if (currentBlockName) {
                if (line.startsWith(" ") || line.startsWith("\t") || line.startsWith("@")) {
                    currentBlockLines.push(line);
                } else {
                    // Start of something else at root level (like global var assignment)
                    blocks[currentBlockName] = currentBlockLines;
                    currentBlockName = "";
                    globals.push(line);
                }
            } else {
                // Check if it's a decorator starting a block?
                if (line.startsWith("@")) {
                    // Look ahead? Or just treat as start of block "Anonymous"?
                    // Actually quicktype output:
                    // @dataclass
                    // class Foo:
                    // So @dataclass line comes FIRST.

                    // We need to capture decorators.
                    // Let's assume decorators belong to the *next* block found.
                    // Store in a buffer?
                    currentBlockLines.push(line);
                } else {
                    globals.push(line);
                }
            }
        }
    }
    // Flush last
    if (currentBlockName) {
        blocks[currentBlockName] = currentBlockLines;
    }

    // Identify types and helpers
    // We need a specific "shared" module for helpers
    const typeToModule: Record<string, string> = { ...TYPE_TO_MODULE };
    const moduleToTypes: Record<string, string[]> = {};
    const helperNames: string[] = [];

    // RESTART strategy:
    // 1. Assign Modules to CLASSES.
    // 2. Assign Modules to FUNCTIONS (Helpers).

    const allBlockNames = new Set(Object.keys(blocks));

    // 1. Classes
    const allClasses = Array.from(allBlockNames).filter(n => n.match(/^[A-Z]/));
    for (const cls of allClasses) {
        if (EXCLUDED_TYPES.has(cls)) continue;
        if (!typeToModule[cls]) {
            // Heuristics
            let m = "shared";
            if (cls.startsWith("Audit")) m = "audit";
            else if (cls.startsWith("Engine")) m = "engine";
            else if (cls.startsWith("Plan")) m = "plantoken";

            typeToModule[cls] = m;
        }
    }

    // 2. Helpers
    const allHelpers = Array.from(allBlockNames).filter(n => n.match(/^[a-z]/));
    for (const func of allHelpers) {
        // Default to shared
        let targetMod = "shared";

        const output = blocks[func][0]; // Signature line

        // Find referenced classes
        for (const cls of allClasses) {
            if (EXCLUDED_TYPES.has(cls)) continue;
            // strict regex to match whole word class usage in signature
            // matches ": Class" or "-> Class" or "[Class]" or "'Class'"
            const usageRegex = new RegExp(`\\b${cls}\\b`);
            if (usageRegex.test(output)) {
                const clsMod = typeToModule[cls];
                if (clsMod && clsMod !== "shared") {
                    targetMod = clsMod;
                    break; // Found a specific home
                }
            }
        }

        typeToModule[func] = targetMod;
    }

    // Build moduleToTypes
    for (const t of allBlockNames) {
        if (EXCLUDED_TYPES.has(t)) continue;
        const m = typeToModule[t] || "shared";
        if (!moduleToTypes[m]) moduleToTypes[m] = [];
        moduleToTypes[m].push(t);
    }

    // Write Files
    // Iterate specific module set + generated ones
    const modulesToWrite = new Set([...Object.values(typeToModule), "shared"]);

    for (const modName of modulesToWrite) {
        if (modName === undefined) continue;

        const fileLines: string[] = [];
        fileLines.push("from __future__ import annotations");
        fileLines.push("from enum import Enum");
        fileLines.push("from dataclasses import dataclass");
        fileLines.push("from typing import Any, List, Optional, Dict, Union, TypeVar, Callable, Type, cast");
        fileLines.push("import json");
        fileLines.push("from datetime import datetime"); // Often used
        fileLines.push("");

        // If not shared, import * from shared (for helpers)
        if (modName !== "shared") {
            fileLines.push("from .shared import *");
            fileLines.push("");
        }

        const typesInModule = moduleToTypes[modName] || [];

        // Dependencies
        const importsNeeded = new Set<string>();
        for (const t of typesInModule) {
            const blockContent = blocks[t].join("\n");
            for (const otherT of allBlockNames) {
                if (otherT === t) continue;
                if (EXCLUDED_TYPES.has(otherT)) continue;

                const otherMod = typeToModule[otherT];
                if (otherMod && otherMod !== modName && otherMod !== "shared") {
                    const regex = new RegExp(`\\b${otherT}\\b`);
                    if (regex.test(blockContent)) {
                        importsNeeded.add(`from .${otherMod} import ${otherT}`);
                    }
                }
            }
        }
        if (importsNeeded.size > 0) {
            fileLines.push(...Array.from(importsNeeded).sort());
            fileLines.push("");
        }

        // Globals (T = TypeVar etc) - put in SHARED only? or all?
        // simple globals like TypeVar should align with where they are used.
        // Easiest is to verify where they are used.
        // Or just dump them in shared and everyone imports * from shared.
        // Let's put globals in shared.

        if (modName === "shared") {
            for (const gLine of globals) {
                if (gLine.startsWith("import") || gLine.startsWith("from")) continue;
                if (gLine.trim() === "") continue;
                fileLines.push(gLine);
            }
            fileLines.push("");
        }

        for (const t of typesInModule) {
            fileLines.push(...blocks[t]);
            fileLines.push("");
        }

        const outPath = path.join(PYTHON_OUT_DIR, `${modName}.py`);
        fs.writeFileSync(outPath, fileLines.join("\n"));
        console.log(`Generated ${modName}.py`);
    }
}

generate().catch(console.error);
