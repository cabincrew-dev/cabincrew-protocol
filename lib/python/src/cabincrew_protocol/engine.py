from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

class EngineMeta(BaseModel):
    workflow_id: str
    step_id: str

class EngineOrchestrator(BaseModel):
    run_index: Optional[float] = None
    workspace_hash: Optional[str] = None
    artifacts_salt: Optional[str] = None

class EngineInput(BaseModel):
    """
    Input delivered via STDIN or CABINCREW_INPUT_FILE.
    Defined in schemas/draft/engine.schema.json
    """
    protocol_version: str
    mode: str = Field(..., description="Execution mode: 'flight-plan' or 'take-off'.")
    meta: EngineMeta
    config: Optional[Dict[str, Any]] = None
    secrets: Optional[Dict[str, Any]] = None
    allowed_secrets: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None
    orchestrator: Optional[EngineOrchestrator] = None
    expected_plan_token: Optional[str] = Field(None, description="Used only during take-off.")

class EngineArtifact(BaseModel):
    name: str
    role: str
    path: str
    hash: str
    size: Optional[float] = None

class EngineMetric(BaseModel):
    name: str
    value: float
    tags: Optional[Dict[str, Any]] = None

class EngineOutput(BaseModel):
    """
    Output delivered via STDOUT or CABINCREW_OUTPUT_FILE.
    Defined in schemas/draft/engine.schema.json
    """
    protocol_version: str
    engine_id: str
    mode: str
    receipt_id: str
    status: str = Field(..., description="Execution status: 'success' or 'failure'.")
    
    error: Optional[str] = None
    warnings: Optional[List[str]] = None
    diagnostics: Optional[Any] = None
    artifacts: Optional[List[EngineArtifact]] = None
    metrics: Optional[List[EngineMetric]] = None
    plan_token: Optional[str] = Field(None, description="SHA256 hash referencing a plan-token.json file.")
