import {
    quicktype,
    InputData,
    JSONSchemaInput,
    FetchingJSONSchemaStore
} from "quicktype-core";
import * as fs from "fs";
import * as path from "path";

const SCHEMA_FILE = path.resolve(__dirname, "../schemas/draft/schema.json");
const GO_OUT_FILE = path.resolve(__dirname, "../lib/go/cabincrew/protocol.go");

async function generate() {
    console.log("Generating Go library from monolithic schema...");

    // Ensure output directory exists
    const outDir = path.dirname(GO_OUT_FILE);
    if (!fs.existsSync(outDir)) {
        fs.mkdirSync(outDir, { recursive: true });
    }

    // Clean up old files
    if (fs.existsSync(outDir)) {
        const oldFiles = fs.readdirSync(outDir).filter(f => f.endsWith(".go"));
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
        lang: "go",
        rendererOptions: {
            "package": "cabincrew",
            "just-types-and-package": "true"
        }
    });

    let goCode = lines.join("\n");

    // Post-process: Replace empty RecordStringAny struct with map[string]interface{}
    // Quicktype can't generate proper map types from additionalProperties: true
    goCode = goCode.replace(
        /type RecordStringAny struct\s*\{\s*\}/g,
        'type RecordStringAny map[string]interface{}'
    );

    // Post-process: Move import statements to top of file
    // Quicktype sometimes generates imports in the middle of the file when using date-time format
    const importMatches = goCode.match(/^import\s+"[^"]+"\s*$/gm);
    if (importMatches && importMatches.length > 0) {
        // Remove imports from their current locations
        goCode = goCode.replace(/^import\s+"[^"]+"\s*$/gm, '');
        // Find package declaration
        const packageMatch = goCode.match(/^package\s+\w+/m);
        if (packageMatch) {
            const packageEnd = packageMatch.index! + packageMatch[0].length;
            // Insert all imports after package declaration
            const imports = [...new Set(importMatches)].join('\n'); // Deduplicate
            goCode = goCode.slice(0, packageEnd) + '\n\n' + imports + '\n' + goCode.slice(packageEnd);
        }
    }

    fs.writeFileSync(GO_OUT_FILE, goCode);
    console.log(`Generated ${GO_OUT_FILE}`);

    // Verify no collision types
    const collisionTypes = goCode.match(/(Purple|Fluffy|Tentacled|Sticky|Indigo|Hilarious)\w+/g);
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
