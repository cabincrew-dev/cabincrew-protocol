import { PlanToken } from './plantoken';

export type RecordStringAny = Record<string, any>;

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
    last_decision?: string;
    plan_token_hash?: string;
}
