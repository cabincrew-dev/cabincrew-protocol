export interface CabinCrewProtocol {
    AnyMap?:                 { [key: string]: any };
    ApprovalRequest?:        ApprovalRequest;
    ApprovalResponse?:       ApprovalResponse;
    Artifact?:               Artifact;
    AuditApproval?:          AuditApproval;
    AuditArtifact?:          AuditArtifact;
    AuditEngine?:            AuditEngine;
    AuditEvent?:             AuditEvent;
    AuditGateway?:           AuditGateway;
    AuditIntegrity?:         AuditIntegrity;
    AuditPolicy?:            AuditPolicy;
    AuditWorkflow?:          AuditWorkflow;
    Decision?:               Decision;
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
    PreflightEvidence?:      PreflightEvidence;
    PreflightInput?:         PreflightInput;
    PreflightOutput?:        PreflightOutput;
    PreflightRequires?:      PreflightRequires;
    "Record<string,any>"?:   RecordStringAny;
    RecordStringAny?:        RecordStringAnyClass;
    State?:                  State;
    WorkflowState?:          WorkflowState;
    [property: string]: any;
}

export interface ApprovalRequest {
    approval_id:      string;
    engine_output?:   RecordStringAny;
    evidence?:        PreflightEvidence[];
    plan_token_hash?: string;
    reason:           string;
    required_role:    string;
    step_id:          string;
    workflow_id:      string;
}

/**
 * Arbitrary metadata. Optional.
 */
export interface RecordStringAny {
}

export interface PreflightEvidence {
    hash: string;
    name: string;
    path: string;
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

export interface AuditApproval {
    approval_id?:   string;
    approved?:      boolean;
    approver?:      string;
    reason?:        string;
    required_role?: string;
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
     * Cryptographic binding between a flight-plan and its subsequent take-off.
     * Defined in schemas/draft/plan-token.schema.json
     */
    plan_token?: PlanToken;
    policy?:     AuditPolicy;
    severity?:   Severity;
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
}

export interface AuditGateway {
    gateway_type?:    string;
    model?:           string;
    policy_decision?: string;
    request_id?:      string;
    tool?:            string;
}

export interface AuditIntegrity {
    actual_plan_token?:   string;
    artifacts_match?:     boolean;
    differences?:         string[];
    expected_plan_token?: string;
    plan_token_match?:    boolean;
}

/**
 * Cryptographic binding between a flight-plan and its subsequent take-off.
 * Defined in schemas/draft/plan-token.schema.json
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
     * AI Model identifier used to generate this plan (e.g. 'gpt-4', 'claude-3').
     * Required for provenance.
     */
    model: string;
    /**
     * Engine protocol version used when this plan was produced.
     */
    protocol_version: string;
    /**
     * Primary plan token identifier, e.g. SHA256 over all plan artifacts + context.
     */
    token: string;
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

export interface AuditPolicy {
    decision?:   string;
    engine?:     string;
    violations?: string[];
    warnings?:   string[];
}

export type Severity = "critical" | "debug" | "error" | "info" | "warning";

export interface AuditWorkflow {
    mode?:        string;
    step_id?:     string;
    workflow_id?: string;
}

export type Decision = "allow" | "deny" | "require_approval" | "warn";

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

export interface PreflightInput {
    context?:      RecordStringAny;
    engine_output: RecordStringAny;
    evidence?:     PreflightEvidence[];
    mode:          Mode;
    /**
     * Cryptographic binding between a flight-plan and its subsequent take-off.
     * Defined in schemas/draft/plan-token.schema.json
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

export interface RecordStringAnyClass {
}

export type State = "APPROVED" | "ARTIFACTS_VALIDATED" | "AWAITING_APPROVAL" | "COMPLETED" | "EXECUTION_COMPLETE" | "FAILED" | "INIT" | "PLAN_GENERATED" | "PLAN_RUNNING" | "PREFLIGHT_COMPLETE" | "PRE_FLIGHT_RUNNING" | "READY_FOR_TAKEOFF" | "TAKEOFF_RUNNING" | "TOKEN_CREATED";

export interface WorkflowState {
    last_decision?:   string;
    plan_token_hash?: string;
    state:            State;
    step_id?:         string;
    workflow_id?:     string;
}
