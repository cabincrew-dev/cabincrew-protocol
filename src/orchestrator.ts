import { PlanToken } from './plantoken';

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

export interface PreflightOutput {
    decision: 'ALLOW' | 'WARN' | 'REQUIRE_APPROVAL' | 'DENY';
    violations?: string[];
    warnings?: string[];
    requires?: PreflightRequires;
}

export interface ApprovalRequest {
    approval_id: string;
    workflow_id: string;
    step_id: string;
    reason: string;
    required_role: string;
    engine_output?: Record<string, any>;
    evidence?: PreflightEvidence[];
    plan_token_hash?: string;
}

export interface ApprovalResponse {
    approval_id: string;
    approved: boolean;
    approver?: string;
    reason?: string;
    timestamp?: string;
}

export interface WorkflowState {
    state: 'INIT' | 'PLAN_RUNNING' | 'PRE_FLIGHT_RUNNING' | 'WAITING_APPROVAL' | 'APPROVED' | 'TAKEOFF_RUNNING' | 'COMPLETED' | 'FAILED';
    workflow_id?: string;
    step_id?: string;
    last_decision?: string;
    plan_token_hash?: string;
}
