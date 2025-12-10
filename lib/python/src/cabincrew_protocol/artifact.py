from typing import Any, Dict, Optional, Union, List
from pydantic import BaseModel, Field

class Artifact(BaseModel):
    """
    Canonical artifact interface.
    Defined in schemas/draft/artifact.schema.json
    """
    artifact_type: str = Field(..., description="Type of artifact (file, diff, patch, action, message, etc). Free-form and engine-defined.")
    action: str = Field(..., description="Operation to perform with this artifact (create, update, delete, apply, execute, etc). Free-form and engine-defined.")
    target: Optional[str] = Field(None, description="Path, resource, or identifier this artifact applies to. Optional.")
    mime: str = Field(..., description="MIME type describing content.")
    
    # Body can be string, object, array, or null.
    body: Optional[Union[str, Dict[str, Any], List[Any]]] = Field(None, description="Inline content for small artifacts.")
    
    body_file: Optional[str] = Field(None, description="Indicates an external data file within the artifact directory.")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Arbitrary metadata. Optional.")
