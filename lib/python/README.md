# CabinCrew Protocol Python Library

This library provides Pydantic models for the CabinCrew Protocol schemas.

## Installation

```bash
pip install cabincrew-protocol
```

## Usage

```python
from cabincrew_protocol import Artifact

artifact = Artifact(
    artifact_type="file",
    action="create",
    mime="text/plain",
    body="Hello world"
)
print(artifact.model_dump_json())
```
