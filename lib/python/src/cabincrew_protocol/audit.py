from typing import List, Optional, Any
from pydantic import BaseModel, Field
from .plantoken import PlanToken

class AuditWorkflow(BaseModel):
    workflow_id: Optional[str] = None
    step_id: Optional[str] = None
    mode: Optional[str] = None

class AuditEngine(BaseModel):
    engine_id: Optional[str] = None
    receipt_id: Optional[str] = None
    status: Optional[str] = None
    error: Optional[str] = None

class AuditArtifact(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    path: Optional[str] = None
    hash: Optional[str] = None
    size: Optional[float] = None

class AuditPolicy(BaseModel):
    decision: Optional[str] = None
    violations: Optional[List[str]] = None
    warnings: Optional[List[str]] = None
    engine: Optional[str] = Field(None, description="Name of policy engine used (e.g. 'OPA', 'ONNX').")

class AuditApproval(BaseModel):
    approval_id: Optional[str] = None
    required_role: Optional[str] = None
    approved: Optional[bool] = None
    approver: Optional[str] = None
    reason: Optional[str] = None

class AuditIntegrity(BaseModel):
    expected_plan_token: Optional[str] = None
    actual_plan_token: Optional[str] = None
    plan_token_match: Optional[bool] = None
    artifacts_match: Optional[bool] = None
    differences: Optional[List[str]] = Field(None, description="Artifact names that failed integrity verification.")

class AuditGateway(BaseModel):
    gateway_type: Optional[str] = None
    request_id: Optional[str] = None
    model: Optional[str] = None
    tool: Optional[str] = None
    policy_decision: Optional[str] = None

class AuditEvent(BaseModel):
    """
    Canonical schema for all audit log events.
    Defined in schemas/draft/audit-event.schema.json
    """
    event_id: str = Field(..., description="Unique identifier for this audit event.")
    timestamp: str = Field(..., description="RFC3339 timestamp of when the event occurred.")
    event_type: str = Field(..., description="Free-form event category.")
    
    workflow: Optional[AuditWorkflow] = None
    engine: Optional[AuditEngine] = Field(None, description="Engine metadata when event relates to an engine run.")
    plan_token: Optional[PlanToken] = Field(None, description="Embedded plan-token if event concerns plan creation or verification.")
    artifacts: Optional[List[AuditArtifact]] = None
    policy: Optional[AuditPolicy] = None
    approval: Optional[AuditApproval] = None
    integrity_check: Optional[AuditIntegrity] = None
    gateway: Optional[AuditGateway] = None
    
    message: Optional[str] = Field(None, description="Human-readable message summarizing the event.")
    severity: Optional[str] = Field(None, description="Severity of event (e.g. 'info', 'warning', 'error', 'critical').")
