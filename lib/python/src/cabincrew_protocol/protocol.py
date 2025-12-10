from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union


class AggregationMethod(Enum):
    """Policy aggregation strategy.
    Defines how multiple policy decisions are combined into a final decision.
    
    Aggregation method used to combine individual policy decisions.
    REQUIRED if multiple policies were evaluated.
    Ensures deterministic aggregation across orchestrators.
    """
    ALL_ALLOW = "all_allow"
    ANY_DENY = "any_deny"
    CUSTOM = "custom"
    MAJORITY = "majority"
    MOST_RESTRICTIVE = "most_restrictive"
    UNANIMOUS = "unanimous"


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
    """Arbitrary metadata. Optional.
    
    Evidence supporting this decision (e.g., rule matches, model scores).
    """
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
    """Audit record for approval events.
    Extended to ensure approval binding is auditable.
    """
    approval_id: str = None
    """Unique approval identifier.
    REQUIRED to correlate request and response.
    """
    approved: bool = None
    """Whether approval was granted.
    REQUIRED for audit trail.
    """
    approver: str = None
    """Identity of the approver.
    REQUIRED for accountability.
    """
    plan_token_hash: str = None
    """SHA256 hash of the plan-token this approval is bound to.
    REQUIRED to prove approval binding and prevent replay attacks.
    """
    required_role: str = None
    """Required role for this approval.
    REQUIRED to verify authorization.
    """
    timestamp: str = None
    """ISO 8601 timestamp when approval was granted/denied.
    REQUIRED for temporal ordering.
    """
    reason: Optional[str] = None
    """Optional reason for approval/denial."""


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


class Decision(Enum):
    """Final aggregated decision after all policy evaluations.
    REQUIRED for chain-of-custody.
    
    Decision from this specific policy.
    """
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"
    WARN = "warn"


@dataclass
class AuditGateway:
    gateway_type: Optional[str] = None
    model: Optional[str] = None
    policy_decision: Optional[Decision] = None
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
    """Plan-token binds artifacts to subsequent take-off.
    Extended with version and governance provenance for safe upgrades and auditability.
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

    governance_hash: Optional[str] = None
    """SHA256 hash of governance context (OPA policies, ONNX models, gateway rules).
    OPTIONAL but recommended for compliance verification.
    Enables auditors to verify governance configuration at plan-time.
    """
    policy_digest: Optional[str] = None
    """SHA256 digest of all policy configurations evaluated during flight-plan.
    OPTIONAL but recommended for governance provenance.
    Proves which policy set was active when plan-token was created.
    """


class Source(Enum):
    """Policy source type."""

    CUSTOM = "custom"
    LLM_GATEWAY = "llm_gateway"
    MCP_GATEWAY = "mcp_gateway"
    ONNX = "onnx"
    OPA = "opa"


@dataclass
class PolicyEvaluation:
    """Individual policy evaluation result.
    Captures decision source and evidence.
    """
    decision: Decision = None
    """Decision from this specific policy."""

    evaluated_at: str = None
    """Evaluation timestamp."""

    policy_id: str = None
    """Policy identifier (e.g., OPA policy name, ONNX model name)."""

    severity: float = None
    """Decision severity for aggregation ordering.
    0=allow, 1=warn, 2=require_approval, 3=deny
    REQUIRED for deterministic "most restrictive" aggregation.
    """
    source: Source = None
    """Policy source type."""

    evidence: Optional[RecordStringAny] = None
    """Evidence supporting this decision (e.g., rule matches, model scores)."""

    reason: Optional[str] = None
    """Reason for this decision."""


@dataclass
class AuditPolicy:
    """Policy evaluation audit record.
    Extended to support chain-of-custody reconstruction.
    """
    decision: Decision = None
    """Final aggregated decision after all policy evaluations.
    REQUIRED for chain-of-custody.
    """
    workflow_state: str = None
    """Workflow state when this policy evaluation occurred.
    REQUIRED for temporal chain-of-custody.
    """
    aggregation_method: Optional[AggregationMethod] = None
    """Aggregation method used to combine individual policy decisions.
    REQUIRED if multiple policies were evaluated.
    Ensures deterministic aggregation across orchestrators.
    """
    engine: Optional[str] = None
    """Legacy field for backward compatibility."""

    policy_evaluations: Optional[List[PolicyEvaluation]] = None
    """Individual policy evaluation results.
    Captures which specific policies (OPA/ONNX/gateway) produced which decisions.
    """
    violations: Optional[List[str]] = None
    """Policy violations detected."""

    warnings: Optional[List[str]] = None
    """Policy warnings (non-blocking)."""


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

    workflow_state: str = None
    """Workflow state when this event was emitted.
    REQUIRED for temporal chain-of-custody reconstruction.
    """
    approval: Optional[AuditApproval] = None
    """Audit record for approval events.
    Extended to ensure approval binding is auditable.
    """
    artifacts: Optional[List[AuditArtifact]] = None
    chain_hash: Optional[str] = None
    """Hash of the previous event in the chain. Allows for ledger-style verification."""

    engine: Optional[AuditEngine] = None
    gateway: Optional[AuditGateway] = None
    integrity_check: Optional[AuditIntegrity] = None
    message: Optional[str] = None
    plan_token: Optional[PlanToken] = None
    """Plan-token binds artifacts to subsequent take-off.
    Extended with version and governance provenance for safe upgrades and auditability.
    """
    policy: Optional[AuditPolicy] = None
    """Policy evaluation audit record.
    Extended to support chain-of-custody reconstruction.
    """
    severity: Optional[Severity] = None
    signature: Optional[str] = None
    """Cryptographic signature of this event hash."""

    signature_key_ref: Optional[str] = None
    """Reference to the key used for signing (e.g. 'engine-key-1', 'orchestrator-key-prod')."""

    workflow: Optional[AuditWorkflow] = None


@dataclass
class RecordStringAnyClass:
    pass


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
    """Plan-token binds artifacts to subsequent take-off.
    Extended with version and governance provenance for safe upgrades and auditability.
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
    last_decision: Optional[Decision] = None
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
    aggregation_method: Optional[AggregationMethod] = None
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
    decision_severity: Optional[float] = None
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
    policy_evaluation: Optional[PolicyEvaluation] = None
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
