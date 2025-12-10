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

    const { lines: pyCode } = await quicktype({
        inputData,
        lang: "python",
        rendererOptions: {
            "python-version": "3.7",
            "just-types": "true"
        }
    });

    let output = pyCode.join("\n");

    // Make all fields optional to avoid dataclass field ordering issues
    // Replace field definitions without defaults to have = None
    output = output.replace(/^(    \w+: (?:Optional\[)?[^=\n]+)$/gm, '$1 = None');

    fs.writeFileSync(PY_OUT_FILE, output);
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
