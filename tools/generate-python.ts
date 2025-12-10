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

    // Post-process: Remove = None defaults from required fields
    // Quicktype generates all fields with = None, but required fields shouldn't have defaults
    // This makes Python enforce required fields at instantiation time

    // Load schema to get required field information
    // (schemaContent and schema are already loaded above, but re-loading here for clarity as per instruction)
    const schemaContentForRequired = fs.readFileSync(SCHEMA_FILE, "utf8");
    const schemaForRequired = JSON.parse(schemaContentForRequired);

    if (schemaForRequired.definitions) {
        for (const [typeName, typeDef] of Object.entries(schemaForRequired.definitions)) {
            if (typeof typeDef === 'object' && typeDef !== null && 'required' in typeDef) {
                const requiredFields = (typeDef as any).required as string[];
                if (requiredFields && requiredFields.length > 0) {
                    // For each required field, remove the = None default
                    for (const fieldName of requiredFields) {
                        // Convert snake_case to match Python field names
                        // Quicktype converts camelCase to snake_case for Python fields
                        // Assuming fieldName from schema is camelCase or similar, and quicktype converts it.
                        // For simplicity, using fieldName directly as per instruction,
                        // but a more robust solution might involve a camelCase to snake_case conversion here.
                        const pythonFieldName = fieldName;

                        // Match pattern: fieldname: Type = None
                        // But NOT: fieldname: Optional[Type] = None (those should keep defaults)
                        const pattern = new RegExp(
                            `(\\s+${pythonFieldName}:\\s+(?!Optional)\\w+(?:\\[.*?\\])?)(\\s*=\\s*None)`,
                            'g'
                        );
                        pythonCode = pythonCode.replace(pattern, '$1');
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
