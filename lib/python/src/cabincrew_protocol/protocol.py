from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union
from enum import Enum


@dataclass
class ApprovalReceivedData:
    approval_id: str = None
    approved: bool = None
    approver: str = None


@dataclass
class ApprovalRecord:
    """Durable approval record.
    Tracks who approved what, when, bound to specific plan-token hash.
    """
    approval_id: str = None
    approved: bool = None
    approved_at: str = None
    approver: str = None
    plan_token_hash: str = None
    step_id: str = None
    evidence_hashes: Optional[List[str]] = None
    reason: Optional[str] = None


@dataclass
class RecordStringAny:
    """Arbitrary metadata. Optional."""

    pass


@dataclass
class PreflightEvidence:
    hash: str = None
    name: str = None
    path: str = None


@dataclass
class ApprovalRequest:
    """Request for human approval before proceeding with execution.
    
    Security: The plan_token_hash MUST be verified to match the current plan-token = None
    to prevent approval replay attacks against mutated plans.
    """
    approval_id: str = None
    plan_token_hash: str = None
    """SHA256 hash of the plan-token that this approval is bound to.
    REQUIRED to prevent approval replay attacks.
    The orchestrator MUST verify this matches the current plan-token before accepting
    approval.
    """
    reason: str = None
    required_role: str = None
    step_id: str = None
    workflow_id: str = None
    engine_output: Optional[RecordStringAny] = None
    evidence: Optional[List[PreflightEvidence]] = None


@dataclass
class ApprovalRequestedData:
    approval_id: str = None
    required_role: str = None
    step_id: str = None


@dataclass
class ApprovalResponse:
    approval_id: str = None
    approved: bool = None
    approver: Optional[str] = None
    reason: Optional[str] = None
    timestamp: Optional[str] = None


@dataclass
class Artifact:
    """Canonical artifact interface.
    Defined in schemas/draft/artifact.schema.json
    """
    action: str = None
    """Operation to perform with this artifact (create, update, delete, apply, execute, etc).
    Free-form and engine-defined.
    """
    artifact_type: str = None
    """Type of artifact (file, diff, patch, action, message, etc). Free-form and engine-defined."""

    mime: str = None
    """MIME type describing content."""

    body: Optional[Union[Dict[str, Any], List[Any], str]] = None
    """Inline content for small artifacts.
    Can be string, object, array, or null.
    """
    body_file: Optional[str] = None
    """Indicates an external data file within the artifact directory."""

    metadata: Optional[RecordStringAny] = None
    """Arbitrary metadata. Optional."""

    target: Optional[str] = None
    """Path, resource, or identifier this artifact applies to. Optional."""


@dataclass
class ArtifactCreatedData:
    artifact_hash: str = None
    artifact_id: str = None
    artifact_type: str = None


@dataclass
class ArtifactRecord:
    """Durable artifact record.
    Tracks artifacts with SHA256 hashes for integrity verification.
    """
    artifact_hash: str = None
    artifact_id: str = None
    artifact_type: str = None
    created_at: str = None
    step_id: str = None
    metadata: Optional[RecordStringAny] = None


@dataclass
class AuditApproval:
    approval_id: Optional[str] = None
    approved: Optional[bool] = None
    approver: Optional[str] = None
    reason: Optional[str] = None
    required_role: Optional[str] = None


@dataclass
class AuditArtifact:
    hash: Optional[str] = None
    name: Optional[str] = None
    path: Optional[str] = None
    role: Optional[str] = None
    size: Optional[float] = None


@dataclass
class AuditEngine:
    engine_id: Optional[str] = None
    error: Optional[str] = None
    receipt_id: Optional[str] = None
    status: Optional[str] = None


@dataclass
class AuditGateway:
    gateway_type: Optional[str] = None
    model: Optional[str] = None
    policy_decision: Optional[str] = None
    request_id: Optional[str] = None
    tool: Optional[str] = None


@dataclass
class AuditIntegrity:
    actual_plan_token: Optional[str] = None
    artifacts_match: Optional[bool] = None
    differences: Optional[List[str]] = None
    expected_plan_token: Optional[str] = None
    plan_token_match: Optional[bool] = None


@dataclass
class PlanArtifactHash:
    hash: str = None
    name: str = None
    size: Optional[float] = None


@dataclass
class PlanToken:
    """Cryptographic binding between a flight-plan and its subsequent take-off.
    Defined in schemas/draft/plan-token.schema.json
    """
    artifacts: List[PlanArtifactHash] = None
    """Per-artifact hashes that contributed to this plan token."""

    created_at: str = None
    """Timestamp when the plan was created (RFC3339)."""

    engine_id: str = None
    """Engine identity that produced this plan."""

    model: str = None
    """AI Model identifier used to generate this plan (e.g. 'gpt-4', 'claude-3').
    Required for provenance.
    """
    protocol_version: str = None
    """Engine protocol version used when this plan was produced."""

    token: str = None
    """Primary plan token identifier, e.g. SHA256 over all plan artifacts + context."""

    workspace_hash: str = None
    """Hash of the workspace state when the plan was created."""


@dataclass
class AuditPolicy:
    decision: Optional[str] = None
    engine: Optional[str] = None
    violations: Optional[List[str]] = None
    warnings: Optional[List[str]] = None


class Severity(Enum):
    CRITICAL = "critical"
    DEBUG = "debug"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"


@dataclass
class AuditWorkflow:
    mode: Optional[str] = None
    step_id: Optional[str] = None
    workflow_id: Optional[str] = None


@dataclass
class AuditEvent:
    """Canonical schema for all audit log events.
    Defined in schemas/draft/audit-event.schema.json
    """
    event_id: str = None
    """Unique identifier for this audit event."""

    event_type: str = None
    """Free-form event category."""

    timestamp: str = None
    """RFC3339 timestamp of when the event occurred."""

    approval: Optional[AuditApproval] = None
    artifacts: Optional[List[AuditArtifact]] = None
    chain_hash: Optional[str] = None
    """Hash of the previous event in the chain. Allows for ledger-style verification."""

    engine: Optional[AuditEngine] = None
    gateway: Optional[AuditGateway] = None
    integrity_check: Optional[AuditIntegrity] = None
    message: Optional[str] = None
    plan_token: Optional[PlanToken] = None
    """Cryptographic binding between a flight-plan and its subsequent take-off.
    Defined in schemas/draft/plan-token.schema.json
    """
    policy: Optional[AuditPolicy] = None
    severity: Optional[Severity] = None
    signature: Optional[str] = None
    """Cryptographic signature of this event hash."""

    signature_key_ref: Optional[str] = None
    """Reference to the key used for signing (e.g. 'engine-key-1', 'orchestrator-key-prod')."""

    workflow: Optional[AuditWorkflow] = None


@dataclass
class RecordStringAnyClass:
    pass


class Decision(Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"
    WARN = "warn"


@dataclass
class EngineArtifact:
    hash: str = None
    name: str = None
    path: str = None
    role: str = None
    size: Optional[float] = None


@dataclass
class EngineMeta:
    step_id: str = None
    workflow_id: str = None


class Mode(Enum):
    """Execution mode: 'flight-plan' or 'take-off'."""

    FLIGHT_PLAN = "flight-plan"
    TAKE_OFF = "take-off"


@dataclass
class EngineOrchestrator:
    artifacts_salt: Optional[str] = None
    run_index: Optional[float] = None
    workspace_hash: Optional[str] = None


@dataclass
class EngineInput:
    """Input delivered via STDIN or CABINCREW_INPUT_FILE.
    Defined in schemas/draft/engine.schema.json
    """
    meta: EngineMeta = None
    mode: Mode = None
    """Execution mode: 'flight-plan' or 'take-off'."""

    protocol_version: str = None
    allowed_secrets: Optional[List[str]] = None
    config: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    expected_plan_token: Optional[str] = None
    identity_token: Optional[str] = None
    """Ephemeral identity token (e.g. OIDC, JWT) for the workload.
    Preferred over static secrets.
    """
    orchestrator: Optional[EngineOrchestrator] = None
    secrets: Optional[Dict[str, Any]] = None


@dataclass
class EngineMetric:
    name: str = None
    value: float = None
    tags: Optional[Dict[str, Any]] = None


@dataclass
class EngineOutput:
    """Output delivered via STDOUT or CABINCREW_OUTPUT_FILE.
    Defined in schemas/draft/engine.schema.json
    """
    engine_id: str = None
    mode: Mode = None
    protocol_version: str = None
    receipt_id: str = None
    status: str = None
    """Execution status: 'success' or 'failure'."""

    artifacts: Optional[List[EngineArtifact]] = None
    diagnostics: Any = None
    error: Optional[str] = None
    metrics: Optional[List[EngineMetric]] = None
    plan_token: Optional[str] = None
    """SHA256 hash referencing a plan-token.json file."""

    warnings: Optional[List[str]] = None


@dataclass
class GatewayApproval:
    approval_id: Optional[str] = None
    reason: Optional[str] = None
    required_role: Optional[str] = None


@dataclass
class LLMGatewayRule:
    action: str = None
    match: RecordStringAny = None
    metadata: Optional[RecordStringAny] = None


@dataclass
class LLMGatewayPolicyConfig:
    model_routing: Optional[RecordStringAny] = None
    onnx_models: Optional[List[str]] = None
    opa_policies: Optional[List[str]] = None
    rules: Optional[List[LLMGatewayRule]] = None


@dataclass
class LLMGatewayRequest:
    input: RecordStringAny = None
    model: str = None
    request_id: str = None
    timestamp: str = None
    context: Optional[RecordStringAny] = None
    provider: Optional[str] = None
    source: Optional[str] = None


@dataclass
class LLMGatewayResponse:
    decision: Decision = None
    request_id: str = None
    timestamp: str = None
    approval: Optional[GatewayApproval] = None
    gateway_payload: Optional[RecordStringAny] = None
    rewritten_input: Optional[RecordStringAny] = None
    routed_model: Optional[str] = None
    violations: Optional[List[str]] = None
    warnings: Optional[List[str]] = None


@dataclass
class MCPGatewayRule:
    action: str = None
    match: RecordStringAny = None
    metadata: Optional[RecordStringAny] = None


@dataclass
class MCPGatewayPolicyConfig:
    onnx_models: Optional[List[str]] = None
    opa_policies: Optional[List[str]] = None
    rules: Optional[List[MCPGatewayRule]] = None


@dataclass
class MCPGatewayRequest:
    method: str = None
    request_id: str = None
    server_id: str = None
    timestamp: str = None
    context: Optional[RecordStringAny] = None
    params: Optional[RecordStringAny] = None
    source: Optional[str] = None


@dataclass
class MCPGatewayResponse:
    decision: Decision = None
    request_id: str = None
    timestamp: str = None
    approval: Optional[GatewayApproval] = None
    rewritten_request: Optional[RecordStringAny] = None
    violations: Optional[List[str]] = None
    warnings: Optional[List[str]] = None


@dataclass
class PolicyEvaluatedData:
    decision: Decision = None
    evaluation_id: str = None
    policy_name: str = None


@dataclass
class PolicyEvaluationRecord:
    """Durable policy evaluation record.
    Tracks policy decisions with evidence for audit trail.
    """
    decision: Decision = None
    evaluated_at: str = None
    evaluation_id: str = None
    policy_name: str = None
    step_id: str = None
    evidence_hashes: Optional[List[str]] = None
    reason: Optional[str] = None


@dataclass
class PreflightInput:
    engine_output: RecordStringAny = None
    mode: Mode = None
    step_id: str = None
    workflow_id: str = None
    context: Optional[RecordStringAny] = None
    evidence: Optional[List[PreflightEvidence]] = None
    plan_token: Optional[PlanToken] = None
    """Cryptographic binding between a flight-plan and its subsequent take-off.
    Defined in schemas/draft/plan-token.schema.json
    """


@dataclass
class PreflightRequires:
    reason: Optional[str] = None
    role: Optional[str] = None


@dataclass
class PreflightOutput:
    decision: Decision = None
    requires: Optional[PreflightRequires] = None
    violations: Optional[List[str]] = None
    warnings: Optional[List[str]] = None


class State(Enum):
    APPROVED = "APPROVED"
    ARTIFACTS_VALIDATED = "ARTIFACTS_VALIDATED"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    EXECUTION_COMPLETE = "EXECUTION_COMPLETE"
    FAILED = "FAILED"
    INIT = "INIT"
    PLAN_GENERATED = "PLAN_GENERATED"
    PLAN_RUNNING = "PLAN_RUNNING"
    PREFLIGHT_COMPLETE = "PREFLIGHT_COMPLETE"
    PRE_FLIGHT_RUNNING = "PRE_FLIGHT_RUNNING"
    READY_FOR_TAKEOFF = "READY_FOR_TAKEOFF"
    TAKEOFF_RUNNING = "TAKEOFF_RUNNING"
    TOKEN_CREATED = "TOKEN_CREATED"


@dataclass
class StepCompletedData:
    step_id: str = None
    artifacts: Optional[List[str]] = None


@dataclass
class StepStartedData:
    step_id: str = None
    step_type: str = None


@dataclass
class WALEntryData:
    initial_state: Optional[State] = None
    plan_token_hash: Optional[str] = None
    step_id: Optional[str] = None
    step_type: Optional[str] = None
    artifacts: Optional[List[str]] = None
    approval_id: Optional[str] = None
    required_role: Optional[str] = None
    approved: Optional[bool] = None
    approver: Optional[str] = None
    artifact_hash: Optional[str] = None
    artifact_id: Optional[str] = None
    artifact_type: Optional[str] = None
    decision: Optional[Decision] = None
    evaluation_id: Optional[str] = None
    policy_name: Optional[str] = None
    final_state: Optional[State] = None
    error: Optional[str] = None
    failed_step: Optional[str] = None


class WALEntryType(Enum):
    APPROVAL_RECEIVED = "approval_received"
    APPROVAL_REQUESTED = "approval_requested"
    ARTIFACT_CREATED = "artifact_created"
    POLICY_EVALUATED = "policy_evaluated"
    STEP_COMPLETED = "step_completed"
    STEP_STARTED = "step_started"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"
    WORKFLOW_STARTED = "workflow_started"


@dataclass
class WALEntry:
    """Write-Ahead Log entry for deterministic replay.
    Enables crash recovery and multi-orchestrator consistency.
    """
    checksum: str = None
    data: WALEntryData = None
    entry_type: WALEntryType = None
    sequence: float = None
    timestamp: str = None
    workflow_id: str = None


@dataclass
class WorkflowCompletedData:
    artifacts: List[str] = None
    final_state: State = None


@dataclass
class WorkflowFailedData:
    error: str = None
    failed_step: Optional[str] = None


@dataclass
class WorkflowStartedData:
    initial_state: State = None
    plan_token_hash: str = None


@dataclass
class WorkflowState:
    state: State = None
    last_decision: Optional[str] = None
    plan_token_hash: Optional[str] = None
    step_id: Optional[str] = None
    workflow_id: Optional[str] = None


@dataclass
class WorkflowStateRecord:
    """Durable workflow state record for restart-safety.
    Contains all information needed to deterministically resume workflow execution.
    """
    approvals: List[ApprovalRecord] = None
    artifacts: List[ArtifactRecord] = None
    created_at: str = None
    current_state: State = None
    plan_token_hash: str = None
    policy_evaluations: List[PolicyEvaluationRecord] = None
    steps_completed: List[str] = None
    steps_pending: List[str] = None
    updated_at: str = None
    workflow_id: str = None
    metadata: Optional[RecordStringAny] = None


@dataclass
class CabinCrewProtocol:
    any_map: Optional[Dict[str, Any]] = None
    approval_received_data: Optional[ApprovalReceivedData] = None
    approval_record: Optional[ApprovalRecord] = None
    approval_request: Optional[ApprovalRequest] = None
    approval_requested_data: Optional[ApprovalRequestedData] = None
    approval_response: Optional[ApprovalResponse] = None
    artifact: Optional[Artifact] = None
    artifact_created_data: Optional[ArtifactCreatedData] = None
    artifact_record: Optional[ArtifactRecord] = None
    audit_approval: Optional[AuditApproval] = None
    audit_artifact: Optional[AuditArtifact] = None
    audit_engine: Optional[AuditEngine] = None
    audit_event: Optional[AuditEvent] = None
    audit_gateway: Optional[AuditGateway] = None
    audit_integrity: Optional[AuditIntegrity] = None
    audit_policy: Optional[AuditPolicy] = None
    audit_workflow: Optional[AuditWorkflow] = None
    decision: Optional[Decision] = None
    engine_artifact: Optional[EngineArtifact] = None
    engine_input: Optional[EngineInput] = None
    engine_meta: Optional[EngineMeta] = None
    engine_metric: Optional[EngineMetric] = None
    engine_orchestrator: Optional[EngineOrchestrator] = None
    engine_output: Optional[EngineOutput] = None
    gateway_approval: Optional[GatewayApproval] = None
    llm_gateway_policy_config: Optional[LLMGatewayPolicyConfig] = None
    llm_gateway_request: Optional[LLMGatewayRequest] = None
    llm_gateway_response: Optional[LLMGatewayResponse] = None
    llm_gateway_rule: Optional[LLMGatewayRule] = None
    mcp_gateway_policy_config: Optional[MCPGatewayPolicyConfig] = None
    mcp_gateway_request: Optional[MCPGatewayRequest] = None
    mcp_gateway_response: Optional[MCPGatewayResponse] = None
    mcp_gateway_rule: Optional[MCPGatewayRule] = None
    mode: Optional[Mode] = None
    plan_artifact_hash: Optional[PlanArtifactHash] = None
    plan_token: Optional[PlanToken] = None
    policy_evaluated_data: Optional[PolicyEvaluatedData] = None
    policy_evaluation_record: Optional[PolicyEvaluationRecord] = None
    preflight_evidence: Optional[PreflightEvidence] = None
    preflight_input: Optional[PreflightInput] = None
    preflight_output: Optional[PreflightOutput] = None
    preflight_requires: Optional[PreflightRequires] = None
    record_string_any: Optional[RecordStringAny] = None
    cabin_crew_protocol_record_string_any: Optional[RecordStringAnyClass] = None
    state: Optional[State] = None
    step_completed_data: Optional[StepCompletedData] = None
    step_started_data: Optional[StepStartedData] = None
    wal_entry: Optional[WALEntry] = None
    wal_entry_data: Optional[WALEntryData] = None
    wal_entry_type: Optional[WALEntryType] = None
    workflow_completed_data: Optional[WorkflowCompletedData] = None
    workflow_failed_data: Optional[WorkflowFailedData] = None
    workflow_started_data: Optional[WorkflowStartedData] = None
    workflow_state: Optional[WorkflowState] = None
    workflow_state_record: Optional[WorkflowStateRecord] = None
