export interface CabinCrewProtocol {
    AggregationMethod?:      AggregationMethod;
    AnyMap?:                 { [key: string]: any };
    ApprovalReceivedData?:   ApprovalReceivedData;
    ApprovalRecord?:         ApprovalRecord;
    ApprovalRequest?:        ApprovalRequest;
    ApprovalRequestedData?:  ApprovalRequestedData;
    ApprovalResponse?:       ApprovalResponse;
    Artifact?:               Artifact;
    ArtifactCreatedData?:    ArtifactCreatedData;
    ArtifactRecord?:         ArtifactRecord;
    AuditApproval?:          AuditApproval;
    AuditArtifact?:          AuditArtifact;
    AuditEngine?:            AuditEngine;
    AuditEvent?:             AuditEvent;
    AuditGateway?:           AuditGateway;
    AuditIntegrity?:         AuditIntegrity;
    AuditPolicy?:            AuditPolicy;
    AuditWorkflow?:          AuditWorkflow;
    Decision?:               Decision;
    DecisionSeverity?:       number;
    EngineArtifact?:         EngineArtifact;
    EngineInput?:            EngineInput;
    EngineMeta?:             EngineMeta;
    EngineMetric?:           EngineMetric;
    EngineOrchestrator?:     EngineOrchestrator;
    EngineOutput?:           EngineOutput;
    GatewayApproval?:        GatewayApproval;
    LLMGatewayPolicyConfig?: LLMGatewayPolicyConfig;
    LLMGatewayRequest?:      LLMGatewayRequest;
    LLMGatewayResponse?:     LLMGatewayResponse;
    LLMGatewayRule?:         LLMGatewayRule;
    MCPGatewayPolicyConfig?: MCPGatewayPolicyConfig;
    MCPGatewayRequest?:      MCPGatewayRequest;
    MCPGatewayResponse?:     MCPGatewayResponse;
    MCPGatewayRule?:         MCPGatewayRule;
    Mode?:                   Mode;
    PlanArtifactHash?:       PlanArtifactHash;
    PlanToken?:              PlanToken;
    PolicyEvaluatedData?:    PolicyEvaluatedData;
    PolicyEvaluation?:       PolicyEvaluation;
    PolicyEvaluationRecord?: PolicyEvaluationRecord;
    PreflightEvidence?:      PreflightEvidence;
    PreflightInput?:         PreflightInput;
    PreflightOutput?:        PreflightOutput;
    PreflightRequires?:      PreflightRequires;
    "Record<string,any>"?:   RecordStringAny;
    RecordStringAny?:        { [key: string]: any };
    State?:                  State;
    StepCompletedData?:      StepCompletedData;
    StepStartedData?:        StepStartedData;
    WALEntry?:               WALEntry;
    WALEntryData?:           WALEntryData;
    WALEntryType?:           WALEntryType;
    WorkflowCompletedData?:  WorkflowCompletedData;
    WorkflowFailedData?:     WorkflowFailedData;
    WorkflowStartedData?:    WorkflowStartedData;
    WorkflowState?:          WorkflowState;
    WorkflowStateRecord?:    WorkflowStateRecord;
    [property: string]: any;
}

/**
 * Policy aggregation strategy.
 * Defines how multiple policy decisions are combined into a final decision.
 *
 * Aggregation method used to combine individual policy decisions.
 * REQUIRED if multiple policies were evaluated.
 * Ensures deterministic aggregation across orchestrators.
 */
export type AggregationMethod = "all_allow" | "any_deny" | "custom" | "majority" | "most_restrictive" | "unanimous";

export interface ApprovalReceivedData {
    approval_id: string;
    approved:    boolean;
    approver:    string;
}

/**
 * Durable approval record.
 * Tracks who approved what, when, bound to specific plan-token hash.
 */
export interface ApprovalRecord {
    approval_id:      string;
    approved:         boolean;
    approved_at:      string;
    approver:         string;
    evidence_hashes?: string[];
    plan_token_hash:  string;
    reason?:          string;
    step_id:          string;
}

/**
 * Request for human approval before proceeding with execution.
 *
 * Security: The plan_token_hash MUST be verified to match the current plan-token
 * to prevent approval replay attacks against mutated plans.
 */
export interface ApprovalRequest {
    approval_id:    string;
    engine_output?: RecordStringAny;
    evidence?:      PreflightEvidence[];
    /**
     * SHA256 hash of the plan-token that this approval is bound to.
     * REQUIRED to prevent approval replay attacks.
     * The orchestrator MUST verify this matches the current plan-token before accepting
     * approval.
     */
    plan_token_hash: string;
    reason:          string;
    required_role:   string;
    step_id:         string;
    workflow_id:     string;
}

/**
 * Arbitrary metadata. Optional.
 *
 * Evidence supporting this decision (e.g., rule matches, model scores).
 */
export interface RecordStringAny {
}

export interface PreflightEvidence {
    hash: string;
    name: string;
    path: string;
}

export interface ApprovalRequestedData {
    approval_id:   string;
    required_role: string;
    step_id:       string;
}

export interface ApprovalResponse {
    approval_id: string;
    approved:    boolean;
    approver?:   string;
    reason?:     string;
    timestamp?:  string;
}

/**
 * Canonical artifact interface.
 * Defined in schemas/draft/artifact.schema.json
 */
export interface Artifact {
    /**
     * Operation to perform with this artifact (create, update, delete, apply, execute, etc).
     * Free-form and engine-defined.
     */
    action: string;
    /**
     * Type of artifact (file, diff, patch, action, message, etc). Free-form and engine-defined.
     */
    artifact_type: string;
    /**
     * Inline content for small artifacts.
     * Can be string, object, array, or null.
     */
    body?: any[] | { [key: string]: any } | null | string;
    /**
     * Indicates an external data file within the artifact directory.
     */
    body_file?: string;
    /**
     * Arbitrary metadata. Optional.
     */
    metadata?: RecordStringAny;
    /**
     * MIME type describing content.
     */
    mime: string;
    /**
     * Path, resource, or identifier this artifact applies to. Optional.
     */
    target?: string;
}

export interface ArtifactCreatedData {
    artifact_hash: string;
    artifact_id:   string;
    artifact_type: string;
}

/**
 * Durable artifact record.
 * Tracks artifacts with SHA256 hashes for integrity verification.
 */
export interface ArtifactRecord {
    artifact_hash: string;
    artifact_id:   string;
    artifact_type: string;
    created_at:    string;
    metadata?:     RecordStringAny;
    step_id:       string;
}

/**
 * Audit record for approval events.
 * Extended to ensure approval binding is auditable.
 */
export interface AuditApproval {
    /**
     * Unique approval identifier.
     * REQUIRED to correlate request and response.
     */
    approval_id: string;
    /**
     * Whether approval was granted.
     * REQUIRED for audit trail.
     */
    approved: boolean;
    /**
     * Identity of the approver.
     * REQUIRED for accountability.
     */
    approver: string;
    /**
     * SHA256 hash of the plan-token this approval is bound to.
     * REQUIRED to prove approval binding and prevent replay attacks.
     */
    plan_token_hash: string;
    /**
     * Optional reason for approval/denial.
     */
    reason?: string;
    /**
     * Required role for this approval.
     * REQUIRED to verify authorization.
     */
    required_role: string;
    /**
     * ISO 8601 timestamp when approval was granted/denied.
     * REQUIRED for temporal ordering.
     */
    timestamp: string;
}

export interface AuditArtifact {
    hash?: string;
    name?: string;
    path?: string;
    role?: string;
    size?: number;
}

export interface AuditEngine {
    engine_id?:  string;
    error?:      string;
    receipt_id?: string;
    status?:     string;
}

/**
 * Canonical schema for all audit log events.
 * Defined in schemas/draft/audit-event.schema.json
 */
export interface AuditEvent {
    /**
     * Audit record for approval events.
     * Extended to ensure approval binding is auditable.
     */
    approval?:  AuditApproval;
    artifacts?: AuditArtifact[];
    /**
     * Hash of the previous event in the chain. Allows for ledger-style verification.
     */
    chain_hash?: string;
    engine?:     AuditEngine;
    /**
     * Unique identifier for this audit event.
     */
    event_id: string;
    /**
     * Free-form event category.
     */
    event_type:       string;
    gateway?:         AuditGateway;
    integrity_check?: AuditIntegrity;
    message?:         string;
    /**
     * Plan-token binds artifacts to subsequent take-off.
     * Extended with version and governance provenance for safe upgrades and auditability.
     */
    plan_token?: PlanToken;
    /**
     * Policy evaluation audit record.
     * Extended to support chain-of-custody reconstruction.
     */
    policy?:   AuditPolicy;
    severity?: Severity;
    /**
     * Cryptographic signature of this event hash.
     */
    signature?: string;
    /**
     * Reference to the key used for signing (e.g. 'engine-key-1', 'orchestrator-key-prod').
     */
    signature_key_ref?: string;
    /**
     * RFC3339 timestamp of when the event occurred.
     */
    timestamp: string;
    workflow?: AuditWorkflow;
    /**
     * Workflow state when this event was emitted.
     * REQUIRED for temporal chain-of-custody reconstruction.
     */
    workflow_state: string;
}

export interface AuditGateway {
    gateway_type?:    string;
    model?:           string;
    policy_decision?: Decision;
    request_id?:      string;
    tool?:            string;
}

/**
 * Final aggregated decision after all policy evaluations.
 * REQUIRED for chain-of-custody.
 *
 * Decision from this specific policy.
 */
export type Decision = "allow" | "deny" | "require_approval" | "warn";

export interface AuditIntegrity {
    actual_plan_token?:   string;
    artifacts_match?:     boolean;
    differences?:         string[];
    expected_plan_token?: string;
    plan_token_match?:    boolean;
}

/**
 * Plan-token binds artifacts to subsequent take-off.
 * Extended with version and governance provenance for safe upgrades and auditability.
 */
export interface PlanToken {
    /**
     * Per-artifact hashes that contributed to this plan token.
     */
    artifacts: PlanArtifactHash[];
    /**
     * Timestamp when the plan was created (RFC3339).
     */
    created_at: string;
    /**
     * Engine identity that produced this plan.
     */
    engine_id: string;
    /**
     * SHA256 hash of governance context (OPA policies, ONNX models, gateway rules).
     * OPTIONAL but recommended for compliance verification.
     * Enables auditors to verify governance configuration at plan-time.
     */
    governance_hash?: string;
    /**
     * AI Model identifier used to generate this plan (e.g. 'gpt-4', 'claude-3').
     * Required for provenance.
     */
    model: string;
    /**
     * SHA256 digest of all policy configurations evaluated during flight-plan.
     * OPTIONAL but recommended for governance provenance.
     * Proves which policy set was active when plan-token was created.
     */
    policy_digest?: string;
    /**
     * Engine protocol version used when this plan was produced.
     */
    protocol_version: string;
    /**
     * Primary plan token identifier, e.g. SHA256 over all plan artifacts + context.
     */
    token: string;
    /**
     * Plan-token format version.
     * REQUIRED for forward-compatibility handshake in mixed-version deployments.
     * Format: "1", "2", etc. (semantic versioning for plan-token structure)
     */
    version: string;
    /**
     * Hash of the workspace state when the plan was created.
     */
    workspace_hash: string;
}

export interface PlanArtifactHash {
    hash:  string;
    name:  string;
    size?: number;
}

/**
 * Policy evaluation audit record.
 * Extended to support chain-of-custody reconstruction.
 */
export interface AuditPolicy {
    /**
     * Aggregation method used to combine individual policy decisions.
     * REQUIRED if multiple policies were evaluated.
     * Ensures deterministic aggregation across orchestrators.
     */
    aggregation_method?: AggregationMethod;
    /**
     * Final aggregated decision after all policy evaluations.
     * REQUIRED for chain-of-custody.
     */
    decision: Decision;
    /**
     * Legacy field for backward compatibility.
     */
    engine?: string;
    /**
     * Individual policy evaluation results.
     * Captures which specific policies (OPA/ONNX/gateway) produced which decisions.
     */
    policy_evaluations?: PolicyEvaluation[];
    /**
     * Policy violations detected.
     */
    violations?: string[];
    /**
     * Policy warnings (non-blocking).
     */
    warnings?: string[];
    /**
     * Workflow state when this policy evaluation occurred.
     * REQUIRED for temporal chain-of-custody.
     */
    workflow_state: string;
}

/**
 * Individual policy evaluation result.
 * Captures decision source and evidence.
 */
export interface PolicyEvaluation {
    /**
     * Decision from this specific policy.
     */
    decision: Decision;
    /**
     * Evaluation timestamp.
     */
    evaluated_at: string;
    /**
     * Evidence supporting this decision (e.g., rule matches, model scores).
     */
    evidence?: RecordStringAny;
    /**
     * Policy identifier (e.g., OPA policy name, ONNX model name).
     */
    policy_id: string;
    /**
     * Reason for this decision.
     */
    reason?: string;
    /**
     * Decision severity for aggregation ordering.
     * 0=allow, 1=warn, 2=require_approval, 3=deny
     * REQUIRED for deterministic "most restrictive" aggregation.
     */
    severity: number;
    /**
     * Policy source type.
     */
    source: Source;
}

/**
 * Policy source type.
 */
export type Source = "custom" | "llm_gateway" | "mcp_gateway" | "onnx" | "opa";

export type Severity = "critical" | "debug" | "error" | "info" | "warning";

export interface AuditWorkflow {
    mode?:        string;
    step_id?:     string;
    workflow_id?: string;
}

export interface EngineArtifact {
    hash:  string;
    name:  string;
    path:  string;
    role:  string;
    size?: number;
}

/**
 * Input delivered via STDIN or CABINCREW_INPUT_FILE.
 * Defined in schemas/draft/engine.schema.json
 */
export interface EngineInput {
    allowed_secrets?:     string[];
    config?:              { [key: string]: any };
    context?:             { [key: string]: any };
    expected_plan_token?: string;
    /**
     * Ephemeral identity token (e.g. OIDC, JWT) for the workload.
     * Preferred over static secrets.
     */
    identity_token?: string;
    meta:            EngineMeta;
    /**
     * Execution mode: 'flight-plan' or 'take-off'.
     */
    mode:             Mode;
    orchestrator?:    EngineOrchestrator;
    protocol_version: string;
    secrets?:         { [key: string]: any };
}

export interface EngineMeta {
    step_id:     string;
    workflow_id: string;
}

/**
 * Execution mode: 'flight-plan' or 'take-off'.
 */
export type Mode = "flight-plan" | "take-off";

export interface EngineOrchestrator {
    artifacts_salt?: string;
    run_index?:      number;
    workspace_hash?: string;
}

export interface EngineMetric {
    name:  string;
    tags?: { [key: string]: any };
    value: number;
}

/**
 * Output delivered via STDOUT or CABINCREW_OUTPUT_FILE.
 * Defined in schemas/draft/engine.schema.json
 */
export interface EngineOutput {
    artifacts?:   EngineArtifact[];
    diagnostics?: any;
    engine_id:    string;
    error?:       string;
    metrics?:     EngineMetric[];
    mode:         Mode;
    /**
     * SHA256 hash referencing a plan-token.json file.
     */
    plan_token?:      string;
    protocol_version: string;
    receipt_id:       string;
    /**
     * Execution status: 'success' or 'failure'.
     */
    status:    string;
    warnings?: string[];
}

export interface GatewayApproval {
    approval_id?:   string;
    reason?:        string;
    required_role?: string;
}

export interface LLMGatewayPolicyConfig {
    model_routing?: RecordStringAny;
    onnx_models?:   string[];
    opa_policies?:  string[];
    rules?:         LLMGatewayRule[];
}

export interface LLMGatewayRule {
    action:    string;
    match:     RecordStringAny;
    metadata?: RecordStringAny;
}

export interface LLMGatewayRequest {
    context?:   RecordStringAny;
    input:      RecordStringAny;
    model:      string;
    provider?:  string;
    request_id: string;
    source?:    string;
    timestamp:  string;
}

export interface LLMGatewayResponse {
    approval?:        GatewayApproval;
    decision:         Decision;
    gateway_payload?: RecordStringAny;
    request_id:       string;
    rewritten_input?: RecordStringAny;
    routed_model?:    string;
    timestamp:        string;
    violations?:      string[];
    warnings?:        string[];
}

export interface MCPGatewayPolicyConfig {
    onnx_models?:  string[];
    opa_policies?: string[];
    rules?:        MCPGatewayRule[];
}

export interface MCPGatewayRule {
    action:    string;
    match:     RecordStringAny;
    metadata?: RecordStringAny;
}

export interface MCPGatewayRequest {
    context?:   RecordStringAny;
    method:     string;
    params?:    RecordStringAny;
    request_id: string;
    server_id:  string;
    source?:    string;
    timestamp:  string;
}

export interface MCPGatewayResponse {
    approval?:          GatewayApproval;
    decision:           Decision;
    request_id:         string;
    rewritten_request?: RecordStringAny;
    timestamp:          string;
    violations?:        string[];
    warnings?:          string[];
}

export interface PolicyEvaluatedData {
    decision:      Decision;
    evaluation_id: string;
    policy_name:   string;
}

/**
 * Durable policy evaluation record.
 * Tracks policy decisions with evidence for audit trail.
 */
export interface PolicyEvaluationRecord {
    decision:         Decision;
    evaluated_at:     string;
    evaluation_id:    string;
    evidence_hashes?: string[];
    policy_name:      string;
    reason?:          string;
    step_id:          string;
}

export interface PreflightInput {
    context?:      RecordStringAny;
    engine_output: RecordStringAny;
    evidence?:     PreflightEvidence[];
    mode:          Mode;
    /**
     * Plan-token binds artifacts to subsequent take-off.
     * Extended with version and governance provenance for safe upgrades and auditability.
     */
    plan_token?: PlanToken;
    step_id:     string;
    workflow_id: string;
}

export interface PreflightOutput {
    decision:    Decision;
    requires?:   PreflightRequires;
    violations?: string[];
    warnings?:   string[];
}

export interface PreflightRequires {
    reason?: string;
    role?:   string;
}

export type State = "APPROVED" | "ARTIFACTS_VALIDATED" | "AWAITING_APPROVAL" | "COMPLETED" | "EXECUTION_COMPLETE" | "FAILED" | "INIT" | "PLAN_GENERATED" | "PLAN_RUNNING" | "PREFLIGHT_COMPLETE" | "PRE_FLIGHT_RUNNING" | "READY_FOR_TAKEOFF" | "TAKEOFF_RUNNING" | "TOKEN_CREATED";

export interface StepCompletedData {
    artifacts?: string[];
    step_id:    string;
}

export interface StepStartedData {
    step_id:   string;
    step_type: string;
}

/**
 * Write-Ahead Log entry for deterministic replay.
 * Enables crash recovery and multi-orchestrator consistency.
 */
export interface WALEntry {
    checksum:    string;
    data:        WALEntryData;
    entry_type:  WALEntryType;
    sequence:    number;
    timestamp:   string;
    workflow_id: string;
}

export interface WALEntryData {
    initial_state?:   State;
    plan_token_hash?: string;
    step_id?:         string;
    step_type?:       string;
    artifacts?:       string[];
    approval_id?:     string;
    required_role?:   string;
    approved?:        boolean;
    approver?:        string;
    artifact_hash?:   string;
    artifact_id?:     string;
    artifact_type?:   string;
    decision?:        Decision;
    evaluation_id?:   string;
    policy_name?:     string;
    final_state?:     State;
    error?:           string;
    failed_step?:     string;
}

export type WALEntryType = "approval_received" | "approval_requested" | "artifact_created" | "policy_evaluated" | "step_completed" | "step_started" | "workflow_completed" | "workflow_failed" | "workflow_started";

export interface WorkflowCompletedData {
    artifacts:   string[];
    final_state: State;
}

export interface WorkflowFailedData {
    error:        string;
    failed_step?: string;
}

export interface WorkflowStartedData {
    initial_state:   State;
    plan_token_hash: string;
}

export interface WorkflowState {
    last_decision?:   Decision;
    plan_token_hash?: string;
    state:            State;
    step_id?:         string;
    workflow_id?:     string;
}

/**
 * Durable workflow state record for restart-safety.
 * Contains all information needed to deterministically resume workflow execution.
 */
export interface WorkflowStateRecord {
    approvals:          ApprovalRecord[];
    artifacts:          ArtifactRecord[];
    created_at:         string;
    current_state:      State;
    metadata?:          RecordStringAny;
    plan_token_hash:    string;
    policy_evaluations: PolicyEvaluationRecord[];
    steps_completed:    string[];
    steps_pending:      string[];
    updated_at:         string;
    workflow_id:        string;
}
