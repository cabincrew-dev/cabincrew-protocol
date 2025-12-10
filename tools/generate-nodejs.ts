import * as fs from "fs";
import * as path from "path";

const SRC_DIR = path.resolve(__dirname, "../src");
const LIB_TYPES_DIR = path.resolve(__dirname, "../lib/nodejs/src/types");
const LIB_INDEX_FILE = path.resolve(__dirname, "../lib/nodejs/src/index.ts");

if (!fs.existsSync(LIB_TYPES_DIR)) {
    fs.mkdirSync(LIB_TYPES_DIR, { recursive: true });
}

// Clean Types Directory
const oldFiles = fs.readdirSync(LIB_TYPES_DIR).filter(f => f.endsWith(".ts"));
for (const f of oldFiles) {
    fs.unlinkSync(path.join(LIB_TYPES_DIR, f));
}

const files = fs.readdirSync(SRC_DIR).filter(f => f.endsWith(".ts") && !f.startsWith("generate-"));

const exportLines: string[] = [];

for (const file of files) {
    const srcPath = path.join(SRC_DIR, file);
    const destPath = path.join(LIB_TYPES_DIR, file);

    fs.copyFileSync(srcPath, destPath);
    console.log(`Copied ${file} to lib/nodejs/src/types/`);

    const baseName = file.replace(".ts", "");
    exportLines.push(`export * from "./types/${baseName}";`);
}

fs.writeFileSync(LIB_INDEX_FILE, exportLines.join("\n"));
console.log(`Generated lib/nodejs/src/index.ts`);
