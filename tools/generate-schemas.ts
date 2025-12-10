import * as TJS from "typescript-json-schema";
import * as fs from "fs";
import * as path from "path";

const ARTIFACTS_DIR = path.resolve(__dirname, "../schemas/draft");
const DOCS_DIR = path.resolve(__dirname, "../docs/schemas");
const TS_BASE_DIR = path.resolve(__dirname, "../src");

if (!fs.existsSync(ARTIFACTS_DIR)) fs.mkdirSync(ARTIFACTS_DIR, { recursive: true });
if (!fs.existsSync(DOCS_DIR)) fs.mkdirSync(DOCS_DIR, { recursive: true });

const settings: TJS.PartialArgs = {
    required: true,
    noExtraProps: true,
    ignoreErrors: true,
};

import * as ts from "typescript";

const compilerOptions = {
    strictNullChecks: true,
    target: ts.ScriptTarget.ES2020 as any,
};

interface Mapping {
    output: string;
    tsFile: string;
    // If root is provided, it's the main type.
    // If types is provided, we create a schema with these as definitions.
    root?: string;
    types?: string[];
}

const mappings: Mapping[] = [
    { output: "artifact.schema.json", tsFile: "artifact.ts", root: "Artifact" },
    { output: "plan-token.schema.json", tsFile: "plantoken.ts", root: "PlanToken" },
    { output: "audit-event.schema.json", tsFile: "audit.ts", root: "AuditEvent" },
    {
        output: "engine.schema.json",
        tsFile: "engine.ts",
        types: ["EngineInput", "EngineOutput"]
    },
    {
        output: "llm-gateway.json",
        tsFile: "gateway_llm.ts",
        types: ["LLMGatewayRequest", "LLMGatewayResponse", "LLMGatewayPolicyConfig"]
    },
    {
        output: "mcp-gateway.json",
        tsFile: "gateway_mcp.ts",
        types: ["MCPGatewayRequest", "MCPGatewayResponse", "MCPGatewayPolicyConfig"]
    },
    {
        output: "orchestrator.schema.json",
        tsFile: "orchestrator.ts",
        types: ["PreflightInput", "PreflightOutput", "ApprovalRequest", "ApprovalResponse", "WorkflowState"]
    }
];

function generate() {
    console.log("Generating schemas...");

    for (const m of mappings) {
        try {
            console.log(`Processing ${m.tsFile}...`);
            const program = TJS.getProgramFromFiles(
                [path.join(TS_BASE_DIR, m.tsFile)],
                compilerOptions
            );

            let schema: TJS.Definition | null = null;

            if (m.root) {
                schema = TJS.generateSchema(program, m.root, settings);
            } else if (m.types) {
                // Generate a schema that acts as a container for these types
                schema = {
                    $schema: "http://json-schema.org/draft-07/schema#",
                    title: m.output.replace(".json", ""),
                    type: "object",
                    properties: {},
                    definitions: {}
                };

                const generator = TJS.buildGenerator(program, settings);
                if (generator) {
                    for (const typeName of m.types) {
                        const s = generator.getSchemaForSymbol(typeName);

                        // Merge nested definitions to root
                        if (s.definitions) {
                            for (const [defKey, defVal] of Object.entries(s.definitions)) {
                                if (schema.definitions && !schema.definitions[defKey]) {
                                    schema.definitions[defKey] = defVal;
                                }
                            }
                            delete s.definitions;
                        }

                        if (schema.definitions) {
                            schema.definitions[typeName] = s;
                        }
                        // Also expose as property
                        if (schema.properties) {
                            schema.properties[typeName] = { $ref: `#/definitions/${typeName}` };
                        }
                    }
                }
            }

            if (schema) {
                fs.writeFileSync(path.join(ARTIFACTS_DIR, m.output), JSON.stringify(schema, null, 4));
                generateMDX(m.output, schema);
            } else {
                console.error(`Failed to generate schema for ${m.tsFile}`);
            }
        } catch (e) {
            console.error(`Error processing ${m.tsFile}:`);
            console.error(e);
        }
    }
}

function generateMDX(filename: string, schema: any) {
    const name = filename.replace(/\.(schema)?\.json$/, "").replace(".json", ""); // handle llm-gateway.json
    const title = schema.title || name;

    let content = `# ${title}\n\n`;
    if (schema.description) {
        content += `${schema.description}\n\n`;
    }

    content += `## Structures\n\n`;

    // Flatten definitions if root has properties (single type)
    if (schema.properties && !schema.definitions) {
        content += `### ${title}\n\n`;
        content += renderProperties(schema.properties, schema.required);
    } else {
        // Multi-type or definitions
        // If properties exist and point to definitions, skip them in listing if they are just wrappers

        let defsToRender = schema.definitions || {};

        // If it's a root type schema, it might have definitions for nested types
        if (schema.properties && schema.required) {
            content += `### ${title}\n\n`;
            content += renderProperties(schema.properties, schema.required);
        }

        for (const [defName, def] of Object.entries(defsToRender)) {
            const d = def as any;
            content += `### ${defName}\n\n`;
            if (d.description) content += `${d.description}\n\n`;
            if (d.properties) {
                content += renderProperties(d.properties, d.required);
            }
        }
    }

    fs.writeFileSync(path.join(DOCS_DIR, `${name}.mdx`), content);
    console.log(`Generated docs/${name}.mdx`);
}

function renderProperties(props: any, required: string[] = []) {
    let md = "| Property | Type | Required | Description |\n";
    md += "|---|---|---|---|\n";

    for (const [key, value] of Object.entries(props)) {
        const v = value as any;
        let type = v.type;

        if (!type && v.$ref) type = `[${v.$ref.split('/').pop()}]`;
        if (v.anyOf || v.oneOf) type = "complex"; // Simplified
        if (Array.isArray(type)) type = type.join(" | ");
        if (!type) type = "any";

        const req = required.includes(key) ? "Yes" : "No";
        const desc = (v.description || "").replace(/\n/g, " ");
        md += `| \`${key}\` | \`${type}\` | ${req} | ${desc} |\n`;
    }
    return md + "\n";
}

generate();
