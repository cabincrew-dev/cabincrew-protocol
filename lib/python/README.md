# CabinCrew Protocol - Python Library

Python bindings for the CabinCrew Protocol, generated from JSON Schema using [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator).

## Features

- **Pydantic v2 Models**: Type-safe data models with automatic validation
- **Required Field Enforcement**: Proper handling of required vs optional fields
- **JSON Schema Validation**: Built-in validation based on the protocol schema
- **Type Hints**: Full type annotations for IDE support and static analysis

## Installation

```bash
pip install cabincrew-protocol
```

## Development

### Prerequisites

To regenerate the Python library from the JSON schema, you need:

```bash
# Install development dependencies (from repository root)
pip install -r requirements-dev.txt

# Or in a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

### Regenerating the Library

From the repository root:

```bash
npm run generate:python
```

This will:
1. Read the JSON schema from `schemas/draft/schema.json`
2. Generate Pydantic v2 models in `lib/python/src/cabincrew_protocol/protocol.py`
3. Properly handle required fields, enums, and validation constraints

## Usage

```python
from cabincrew_protocol.protocol import (
    EngineOutput,
    Status,
    Mode,
    PlanToken,
    AuditEvent
)

# Create an engine output with required fields
output = EngineOutput(
    engine_id="my-engine",
    mode=Mode.FLIGHT_PLAN,
    protocol_version="1.0.0",
    receipt_id="receipt-123",
    status=Status.SUCCESS
)

# Pydantic will validate required fields and types
print(output.model_dump_json(indent=2))
```

## Benefits over Dataclasses

The Python library uses Pydantic models instead of dataclasses because:

- **Validation**: Automatic validation of field types and constraints
- **Required Fields**: Proper enforcement without field ordering issues
- **JSON Schema**: Native JSON schema support for serialization/deserialization
- **Better Errors**: Clear validation error messages
- **Extensibility**: Easy to add custom validators and transformers

## Dependencies

- `pydantic>=2.0`: Core validation and modeling
- `python-dateutil>=2.8.0`: DateTime parsing for timestamp fields
