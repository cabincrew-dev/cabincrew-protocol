import {
    quicktype,
    InputData,
    JSONSchemaInput,
    FetchingJSONSchemaStore
} from "quicktype-core";
import * as fs from "fs";
import * as path from "path";

const SCHEMA_FILE = path.resolve(__dirname, "../schemas/draft/schema.json");
const PY_OUT_FILE = path.resolve(__dirname, "../lib/python/src/cabincrew_protocol/protocol.py");

async function generate() {
    console.log("Generating Python library from monolithic schema...");

    // Ensure output directory exists
    const outDir = path.dirname(PY_OUT_FILE);
    if (!fs.existsSync(outDir)) {
        fs.mkdirSync(outDir, { recursive: true });
    }

    // Clean up old files
    if (fs.existsSync(outDir)) {
        const oldFiles = fs.readdirSync(outDir).filter(f => f.endsWith(".py") && f !== "__init__.py");
        for (const f of oldFiles) {
            fs.unlinkSync(path.join(outDir, f));
        }
    }

    const inputData = new InputData();
    const schemaInput = new JSONSchemaInput(new FetchingJSONSchemaStore());

    // Load the schema and create a wrapper that references all definitions
    const schemaContent = fs.readFileSync(SCHEMA_FILE, "utf8");
    const schema = JSON.parse(schemaContent);

    // Create a wrapper schema that forces Quicktype to generate all types
    const wrapperSchema = {
        $schema: schema.$schema,
        definitions: schema.definitions,
        type: "object",
        properties: {} as Record<string, any>
    };

    // Add each definition as a property reference
    if (schema.definitions) {
        for (const typeName of Object.keys(schema.definitions)) {
            wrapperSchema.properties[typeName] = {
                $ref: `#/definitions/${typeName}`
            };
        }
    }

    await schemaInput.addSource({
        name: "CabinCrewProtocol",
        schema: JSON.stringify(wrapperSchema)
    });

    inputData.addInput(schemaInput);

    const { lines } = await quicktype({
        inputData,
        lang: "python",
        rendererOptions: {
            "python-version": "3.7"
        }
    });

    let pythonCode = lines.join("\n");

    // Post-process: Fix dataclass field ordering
    // Python dataclasses require all fields without defaults to come before fields with defaults
    // We need to:
    // 1. Identify required fields from schema
    // 2. Remove = None from required fields
    // 3. Reorder fields within each class so required fields come first

    const schemaContentForRequired = fs.readFileSync(SCHEMA_FILE, "utf8");
    const schemaForRequired = JSON.parse(schemaContentForRequired);

    if (schemaForRequired.definitions) {
        for (const [typeName, typeDef] of Object.entries(schemaForRequired.definitions)) {
            if (typeof typeDef === 'object' && typeDef !== null && 'properties' in typeDef) {
                const properties = (typeDef as any).properties || {};
                const requiredFields = new Set((typeDef as any).required || []);

                // Find the class definition in the generated code
                const classRegex = new RegExp(`class ${typeName}[^:]*:\\s*(?:"""[^"]*"""\\s*)?([\\s\\S]*?)(?=\\n(?:class |def |\\Z))`, 'm');
                const classMatch = pythonCode.match(classRegex);

                if (classMatch && requiredFields.size > 0) {
                    const classBody = classMatch[1];
                    const fieldLines: Array<{ line: string, isRequired: boolean, fieldName: string }> = [];

                    // Parse field lines
                    const fieldRegex = /^    (\w+):\s*(.+?)(?:\s*=\s*None)?$/gm;
                    let match;
                    while ((match = fieldRegex.exec(classBody)) !== null) {
                        const fieldName = match[1];
                        const fieldType = match[2];
                        const isRequired = requiredFields.has(fieldName);
                        const hasDefault = classBody.includes(`${fieldName}:`) && classBody.includes(`= None`);

                        // Reconstruct field line
                        if (isRequired) {
                            fieldLines.push({
                                line: `    ${fieldName}: ${fieldType}`,
                                isRequired: true,
                                fieldName
                            });
                        } else {
                            fieldLines.push({
                                line: `    ${fieldName}: ${fieldType}${hasDefault ? ' = None' : ''}`,
                                isRequired: false,
                                fieldName
                            });
                        }
                    }

                    // Sort: required fields first, then optional
                    fieldLines.sort((a, b) => {
                        if (a.isRequired && !b.isRequired) return -1;
                        if (!a.isRequired && b.isRequired) return 1;
                        return 0;
                    });

                    // Rebuild class with reordered fields
                    if (fieldLines.length > 0) {
                        const newClassBody = fieldLines.map(f => f.line).join('\n');
                        pythonCode = pythonCode.replace(classMatch[0],
                            `class ${typeName}${classMatch[0].substring(classMatch[0].indexOf(':'), classMatch[0].indexOf(classBody))}${newClassBody}\n`);
                    }
                }
            }
        }
    }

    fs.writeFileSync(PY_OUT_FILE, pythonCode);
    console.log(`Generated ${PY_OUT_FILE}`);

    // Verify no collision types
    const content = fs.readFileSync(PY_OUT_FILE, "utf8");
    const collisionTypes = content.match(/(Purple|Fluffy|Tentacled|Sticky|Indigo|Hilarious)\w+/g);
    if (collisionTypes) {
        console.warn(`⚠️  Warning: Found collision types: ${[...new Set(collisionTypes)].join(", ")}`);
    } else {
        console.log("✓ No collision types found");
    }
}

generate().catch(err => {
    console.error(err);
    process.exit(1);
});
