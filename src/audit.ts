import { PlanToken } from './plantoken';

export interface AuditWorkflow {
    workflow_id?: string;
    step_id?: string;
    mode?: string;
}

export interface AuditEngine {
    engine_id?: string;
    receipt_id?: string;
    status?: string;
    error?: string;
}

export interface AuditArtifact {
    name?: string;
    role?: string;
    path?: string;
    hash?: string;
    size?: number;
}

export interface AuditPolicy {
    decision?: string;
    violations?: string[];
    warnings?: string[];
    engine?: string;
}

export interface AuditApproval {
    approval_id?: string;
    required_role?: string;
    approved?: boolean;
    approver?: string;
    reason?: string;
}

export interface AuditIntegrity {
    expected_plan_token?: string;
    actual_plan_token?: string;
    plan_token_match?: boolean;
    artifacts_match?: boolean;
    differences?: string[];
}

export interface AuditGateway {
    gateway_type?: string;
    request_id?: string;
    model?: string;
    tool?: string;
    policy_decision?: string;
}

/**
 * Canonical schema for all audit log events.
 * Defined in schemas/draft/audit-event.schema.json
 */
export interface AuditEvent {
    /**
     * Unique identifier for this audit event.
     */
    event_id: string;
    /**
     * RFC3339 timestamp of when the event occurred.
     */
    timestamp: string;
    /**
     * Free-form event category.
     */
    event_type: string;

    workflow?: AuditWorkflow;
    engine?: AuditEngine;
    plan_token?: PlanToken;
    artifacts?: AuditArtifact[];
    policy?: AuditPolicy;
    approval?: AuditApproval;
    integrity_check?: AuditIntegrity;
    gateway?: AuditGateway;

    message?: string;
    severity?: 'debug' | 'info' | 'warning' | 'error' | 'critical';
}
