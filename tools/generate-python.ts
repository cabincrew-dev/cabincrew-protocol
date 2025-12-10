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

    // Use datamodel-code-generator (Python tool) to generate Pydantic models
    // This provides much better handling of required fields, validation, and type safety
    // Install with: pip install datamodel-code-generator

    const { execSync } = require('child_process');

    try {
        // Generate Pydantic models from JSON Schema
        execSync(
            `datamodel-codegen --input ${SCHEMA_FILE} --output ${PY_OUT_FILE} --input-file-type jsonschema --output-model-type pydantic_v2.BaseModel --field-constraints --use-standard-collections --use-schema-description --use-field-description --use-default --collapse-root-models --target-python-version 3.9`,
            { stdio: 'inherit' }
        );

        console.log(`Generated ${PY_OUT_FILE}`);
    } catch (error) {
        console.error("Error generating Python library:");
        console.error("Make sure datamodel-code-generator is installed:");
        console.error("  pip install 'datamodel-code-generator[http]'");
        throw error;
    }
}

generate().catch(err => {
    console.error(err);
    process.exit(1);
});
