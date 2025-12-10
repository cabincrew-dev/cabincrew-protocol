import { PlanToken } from './plantoken';

/**
 * Generic record type for arbitrary key-value pairs.
 * Used for config, context, metadata, evidence, etc.
 * @additionalProperties true
 */
export interface RecordStringAny {
    [key: string]: any;
}

export interface PreflightEvidence {
    name: string;
    path: string;
    hash: string;
}

export interface PreflightInput {
    workflow_id: string;
    step_id: string;
    mode: 'flight-plan' | 'take-off';
    engine_output: Record<string, any>;
    evidence?: PreflightEvidence[];
    context?: Record<string, any>;
    plan_token?: PlanToken;
}

export interface PreflightRequires {
    role?: string;
    reason?: string;
}

export type Decision = 'allow' | 'warn' | 'require_approval' | 'deny';

export interface PreflightOutput {
    decision: Decision;
    violations?: string[];
    warnings?: string[];
    requires?: PreflightRequires;
}

/**
 * Request for human approval before proceeding with execution.
 * 
 * Security: The plan_token_hash MUST be verified to match the current plan-token
 * to prevent approval replay attacks against mutated plans.
 */
export interface ApprovalRequest {
    approval_id: string;
    workflow_id: string;
    step_id: string;
    reason: string;
    required_role: string;
    engine_output?: Record<string, any>;
    evidence?: PreflightEvidence[];
    /**
     * SHA256 hash of the plan-token that this approval is bound to.
     * REQUIRED to prevent approval replay attacks.
     * The orchestrator MUST verify this matches the current plan-token before accepting approval.
     */
    plan_token_hash: string;
}

export interface ApprovalResponse {
    approval_id: string;
    approved: boolean;
    approver?: string;
    reason?: string;
    timestamp?: string;
}

export type State = 'INIT' | 'PLAN_RUNNING' | 'PLAN_GENERATED' | 'ARTIFACTS_VALIDATED' | 'TOKEN_CREATED' | 'PRE_FLIGHT_RUNNING' | 'PREFLIGHT_COMPLETE' | 'AWAITING_APPROVAL' | 'APPROVED' | 'READY_FOR_TAKEOFF' | 'TAKEOFF_RUNNING' | 'EXECUTION_COMPLETE' | 'COMPLETED' | 'FAILED';

export interface WorkflowState {
    state: State;
    workflow_id?: string;
    step_id?: string;
    last_decision?: Decision;
    plan_token_hash?: string;
}

// ============================================================================
// Restart-Safe Persistence Schema
// ============================================================================

/**
 * Durable workflow state record for restart-safety.
 * Contains all information needed to deterministically resume workflow execution.
 */
export interface WorkflowStateRecord {
    workflow_id: string;
    current_state: State;
    plan_token_hash: string;
    created_at: string; // ISO 8601
    updated_at: string; // ISO 8601

    // Execution history
    steps_completed: string[];
    steps_pending: string[];

    // Approval tracking
    approvals: ApprovalRecord[];

    // Artifact tracking
    artifacts: ArtifactRecord[];

    // Policy results
    policy_evaluations: PolicyEvaluationRecord[];

    // Metadata
    metadata?: Record<string, any>;
}

/**
 * Durable approval record.
 * Tracks who approved what, when, bound to specific plan-token hash.
 */
export interface ApprovalRecord {
    approval_id: string;
    step_id: string;
    plan_token_hash: string; // Hash at time of approval
    approved: boolean;
    approver: string;
    approved_at: string; // ISO 8601
    reason?: string;
    evidence_hashes?: string[]; // SHA256 of evidence artifacts
}

/**
 * Durable artifact record.
 * Tracks artifacts with SHA256 hashes for integrity verification.
 */
export interface ArtifactRecord {
    artifact_id: string;
    step_id: string;
    artifact_hash: string; // SHA256 of artifact content
    artifact_type: string;
    created_at: string; // ISO 8601
    metadata?: Record<string, any>;
}

/**
 * Durable policy evaluation record.
 * Tracks policy decisions with evidence for audit trail.
 */
export interface PolicyEvaluationRecord {
    evaluation_id: string;
    step_id: string;
    policy_name: string;
    decision: Decision;
    evaluated_at: string; // ISO 8601
    reason?: string;
    evidence_hashes?: string[];
}

/**
 * Write-Ahead Log entry for deterministic replay.
 * Enables crash recovery and multi-orchestrator consistency.
 */
export interface WALEntry {
    sequence: number; // Monotonic sequence number
    timestamp: string; // ISO 8601
    workflow_id: string;
    entry_type: WALEntryType;
    data: WALEntryData;
    checksum: string; // SHA256 of entry content
}

export type WALEntryType =
    | 'workflow_started'
    | 'step_started'
    | 'step_completed'
    | 'approval_requested'
    | 'approval_received'
    | 'artifact_created'
    | 'policy_evaluated'
    | 'workflow_completed'
    | 'workflow_failed';

export type WALEntryData =
    | WorkflowStartedData
    | StepStartedData
    | StepCompletedData
    | ApprovalRequestedData
    | ApprovalReceivedData
    | ArtifactCreatedData
    | PolicyEvaluatedData
    | WorkflowCompletedData
    | WorkflowFailedData;

export interface WorkflowStartedData {
    plan_token_hash: string;
    initial_state: State;
}

export interface StepStartedData {
    step_id: string;
    step_type: string;
}

export interface StepCompletedData {
    step_id: string;
    artifacts?: string[]; // Artifact IDs
}

export interface ApprovalRequestedData {
    approval_id: string;
    step_id: string;
    required_role: string;
}

export interface ApprovalReceivedData {
    approval_id: string;
    approved: boolean;
    approver: string;
}

export interface ArtifactCreatedData {
    artifact_id: string;
    artifact_hash: string;
    artifact_type: string;
}

export interface PolicyEvaluatedData {
    evaluation_id: string;
    policy_name: string;
    decision: Decision;
}

export interface WorkflowCompletedData {
    final_state: State;
    artifacts: string[];
}

export interface WorkflowFailedData {
    error: string;
    failed_step?: string;
}
