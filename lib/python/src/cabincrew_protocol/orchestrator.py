from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .plantoken import PlanToken

class PreflightEvidence(BaseModel):
    name: str
    path: str
    hash: str

class PreflightInput(BaseModel):
    """
    Input given to the preflight (policy) stage.
    Defined in schemas/draft/orchestrator.schema.json
    """
    workflow_id: str
    step_id: str
    mode: str = Field(..., description="flight-plan or take-off")
    engine_output: Dict[str, Any]
    evidence: Optional[List[PreflightEvidence]] = None
    context: Optional[Dict[str, Any]] = None
    plan_token: Optional[PlanToken] = None

class PreflightRequires(BaseModel):
    role: Optional[str] = None
    reason: Optional[str] = None

class PreflightOutput(BaseModel):
    """
    Unified decision structure emitted after OPA/ONNX evaluation.
    Defined in schemas/draft/orchestrator.schema.json
    """
    decision: str = Field(..., description="ALLOW, WARN, REQUIRE_APPROVAL, DENY")
    violations: Optional[List[str]] = None
    warnings: Optional[List[str]] = None
    requires: Optional[PreflightRequires] = None

class ApprovalRequest(BaseModel):
    """
    Approval packet sent to a human or approval system.
    Defined in schemas/draft/orchestrator.schema.json
    """
    approval_id: str
    workflow_id: str
    step_id: str
    reason: str
    required_role: str
    engine_output: Optional[Dict[str, Any]] = None
    evidence: Optional[List[PreflightEvidence]] = None
    plan_token_hash: Optional[str] = None

class ApprovalResponse(BaseModel):
    """
    Response from the human approver or approval system.
    Defined in schemas/draft/orchestrator.schema.json
    """
    approval_id: str
    approved: bool
    approver: Optional[str] = None
    reason: Optional[str] = None
    timestamp: Optional[str] = None

class WorkflowState(BaseModel):
    """
    State machine snapshot for the orchestrator.
    Defined in schemas/draft/orchestrator.schema.json
    """
    state: str = Field(..., description="INIT, PLAN_RUNNING, PRE_FLIGHT_RUNNING, WAITING_APPROVAL, APPROVED, TAKEOFF_RUNNING, COMPLETED, FAILED")
    workflow_id: Optional[str] = None
    step_id: Optional[str] = None
    last_decision: Optional[str] = None
    plan_token_hash: Optional[str] = None
