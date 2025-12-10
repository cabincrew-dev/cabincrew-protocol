import {
    quicktype,
    InputData,
    JSONSchemaInput,
    FetchingJSONSchemaStore
} from "quicktype-core";
import * as fs from "fs";
import * as path from "path";

const SCHEMA_FILE = path.resolve(__dirname, "../schemas/draft/schema.json");
const TS_OUT_FILE = path.resolve(__dirname, "../lib/nodejs/src/protocol.ts");

async function generate() {
    console.log("Generating TypeScript library from monolithic schema...");

    // Ensure output directory exists
    const outDir = path.dirname(TS_OUT_FILE);
    if (!fs.existsSync(outDir)) {
        fs.mkdirSync(outDir, { recursive: true });
    }

    // Clean up old files
    if (fs.existsSync(outDir)) {
        const oldFiles = fs.readdirSync(outDir).filter(f => f.endsWith(".ts") && f !== "index.ts");
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

    const { lines: tsCode } = await quicktype({
        inputData,
        lang: "typescript",
        rendererOptions: {
            "just-types": "true",
            "prefer-unions": "true",
            "prefer-const-values": "true"
        }
    });

    fs.writeFileSync(TS_OUT_FILE, tsCode.join("\n"));
    console.log(`Generated ${TS_OUT_FILE}`);

    // Verify no collision types
    const content = fs.readFileSync(TS_OUT_FILE, "utf8");
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
