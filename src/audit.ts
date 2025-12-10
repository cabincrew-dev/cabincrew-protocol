import { PlanToken } from './plantoken';
import { Decision } from './orchestrator';

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

/**
 * Policy aggregation strategy.
 * Defines how multiple policy decisions are combined into a final decision.
 */
export type AggregationMethod =
    | 'most_restrictive'  // deny > require_approval > warn > allow
    | 'unanimous'         // all must agree, otherwise most restrictive
    | 'majority'          // majority vote, ties go to most restrictive
    | 'any_deny'          // single deny blocks all
    | 'all_allow'         // all must allow, otherwise most restrictive
    | 'custom';           // implementation-defined (must document)

/**
 * Decision severity for ordering.
 * Used to determine "most restrictive" in aggregation.
 */
export type DecisionSeverity = 0 | 1 | 2 | 3; // allow=0, warn=1, require_approval=2, deny=3

/**
 * Policy evaluation audit record.
 * Extended to support chain-of-custody reconstruction.
 */
export interface AuditPolicy {
    /**
     * Final aggregated decision after all policy evaluations.
     * REQUIRED for chain-of-custody.
     */
    decision: Decision;

    /**
     * Individual policy evaluation results.
     * Captures which specific policies (OPA/ONNX/gateway) produced which decisions.
     */
    policy_evaluations?: PolicyEvaluation[];

    /**
     * Aggregation method used to combine individual policy decisions.
     * REQUIRED if multiple policies were evaluated.
     * Ensures deterministic aggregation across orchestrators.
     */
    aggregation_method?: AggregationMethod;

    /**
     * Workflow state when this policy evaluation occurred.
     * REQUIRED for temporal chain-of-custody.
     */
    workflow_state: string;

    /**
     * Policy violations detected.
     */
    violations?: string[];

    /**
     * Policy warnings (non-blocking).
     */
    warnings?: string[];

    /**
     * Legacy field for backward compatibility.
     * @deprecated Use policy_evaluations instead.
     */
    engine?: string;
}

/**
 * Individual policy evaluation result.
 * Captures decision source and evidence.
 */
export interface PolicyEvaluation {
    /**
     * Policy source type.
     */
    source: 'opa' | 'onnx' | 'llm_gateway' | 'mcp_gateway' | 'custom';

    /**
     * Policy identifier (e.g., OPA policy name, ONNX model name).
     */
    policy_id: string;

    /**
     * Decision from this specific policy.
     */
    decision: Decision;

    /**
     * Decision severity for aggregation ordering.
     * 0=allow, 1=warn, 2=require_approval, 3=deny
     * REQUIRED for deterministic "most restrictive" aggregation.
     */
    severity: DecisionSeverity;

    /**
     * Reason for this decision.
     */
    reason?: string;

    /**
     * Evidence supporting this decision (e.g., rule matches, model scores).
     */
    evidence?: Record<string, any>;

    /**
     * Evaluation timestamp.
     * @format date-time
     */
    evaluated_at: string; // ISO 8601
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
     * Required role for this approval.
     * REQUIRED to verify authorization.
     */
    required_role: string;

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
     * ISO 8601 timestamp when approval was granted/denied.
     * REQUIRED for temporal ordering.
     * @format date-time
     */
    timestamp: string;

    /**
     * Optional reason for approval/denial.
     */
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
    policy_decision?: Decision;
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
     * @format date-time
     */
    timestamp: string;
    /**
     * Free-form event category.
     */
    event_type: string;

    workflow?: AuditWorkflow;

    /**
     * Workflow state when this event was emitted.
     * REQUIRED for temporal chain-of-custody reconstruction.
     */
    workflow_state: string;

    engine?: AuditEngine;
    plan_token?: PlanToken;
    artifacts?: AuditArtifact[];
    policy?: AuditPolicy;
    approval?: AuditApproval;
    integrity_check?: AuditIntegrity;
    gateway?: AuditGateway;

    /**
     * Cryptographic signature of this event hash.
     */
    signature?: string;
    /**
     * Reference to the key used for signing (e.g. 'engine-key-1', 'orchestrator-key-prod').
     */
    signature_key_ref?: string;
    /**
     * Hash of the previous event in the chain. Allows for ledger-style verification.
     */
    chain_hash?: string;

    message?: string;
    severity?: 'debug' | 'info' | 'warning' | 'error' | 'critical';
}
