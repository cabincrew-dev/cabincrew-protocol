# Code Generation Tools

This directory contains scripts for generating language-specific libraries from the TypeScript source definitions.

## Overview

The CabinCrew Protocol uses TypeScript as the **single source of truth** for all type definitions. These scripts generate:

1. **JSON Schema** - Canonical schema for validation
2. **Go Library** - Type-safe Go bindings
3. **Python Library** - Pydantic v2 models
4. **TypeScript/Node.js Library** - Type definitions for Node.js

## Prerequisites

### Node.js Dependencies
```bash
npm install
```

### Python Generator (datamodel-code-generator)
```bash
# In a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

## Generation Scripts

### `generate-schema.ts`
Generates JSON Schema and MDX documentation from TypeScript source.

**Tool**: `typescript-json-schema`

**Output**:
- `schemas/draft/schema.json` - JSON Schema Draft-07
- `schemas/draft/schema.mdx` - Human-readable documentation

**Run**: `npm run generate`

**Key Features**:
- Extracts JSDoc comments as descriptions
- Supports `@format`, `@type`, `@minimum`, `@maximum` annotations
- Post-processes to fix `RecordStringAny` type
- Removes duplicate `Record<string,any>` definitions

### `generate-go.ts`
Generates Go library from JSON Schema.

**Tool**: `quicktype-core`

**Output**: `lib/go/cabincrew/protocol.go`

**Run**: `npm run generate:go`

**Key Features**:
- Generates Go structs with JSON tags
- Post-processes to replace `RecordStringAny` with `map[string]interface{}`
- Moves import statements to top of file
- Validates no collision types (Purple, Fluffy, etc.)

### `generate-python.ts`
Generates Python Pydantic models from JSON Schema.

**Tool**: `datamodel-code-generator`

**Output**: `lib/python/src/cabincrew_protocol/protocol.py`

**Run**: `npm run generate:python`

**Key Features**:
- Generates Pydantic v2 BaseModel classes
- Proper required vs optional field handling
- Field constraints (min, max, pattern)
- Enum support
- Timestamp removed post-generation to prevent CI desync

**Why Pydantic over dataclasses?**
- Better validation
- Proper required field enforcement
- JSON schema native support
- No field ordering issues

### `generate-nodejs.ts`
Generates TypeScript library from JSON Schema.

**Tool**: `quicktype-core`

**Output**: `lib/nodejs/src/protocol.ts`

**Run**: `npm run generate:nodejs`

**Key Features**:
- Generates TypeScript interfaces
- Type aliases for enums
- Validates no collision types

## Important Annotations

### `@type integer`
Forces JSON Schema to use `"type": "integer"` instead of `"type": "number"`:
```typescript
/**
 * Monotonic sequence number.
 * @type integer
 * @minimum 0
 */
sequence: number;
```

### `@format date-time`
Marks string fields as RFC3339 timestamps:
```typescript
/** @format date-time */
timestamp: string;
```

### `@minimum` / `@maximum`
Adds numeric constraints:
```typescript
/**
 * @minimum 0
 * @maximum 3
 */
severity: number;
```

## Smoke Tests

After generation, run smoke tests to verify libraries:

```bash
# Python
python3 tests/smoke_test_python.py

# TypeScript/Node.js
npx ts-node tests/smoke_test_nodejs.ts

# Go
GO111MODULE=off go run tests/smoke_test_go.go
```

## CI/CD

The CI pipeline (`github/workflows/ci.yml`):
1. Installs all dependencies
2. Regenerates all libraries
3. Checks for uncommitted changes (desync detection)
4. Runs smoke tests

If you modify TypeScript source, you **must** regenerate all libraries and commit the changes.

## Troubleshooting

### Python: "ModuleNotFoundError: No module named 'pydantic'"
Install dependencies: `pip install -r requirements-dev.txt`

### Go: "undefined: cabincrew"
Run with `GO111MODULE=off` or from repository root

### Timestamp causing CI desync
The Python generator includes a timestamp comment. This is automatically removed by sed in the generation script and CI.

### Collision types (Purple, Fluffy, etc.)
These indicate quicktype found naming conflicts. Review the schema for duplicate type names.
