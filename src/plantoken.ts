export interface PlanArtifactHash {
    name: string;
    hash: string;
    size?: number;
}

/**
 * Plan-token binds artifacts to subsequent take-off.
 * Extended with version and governance provenance for safe upgrades and auditability.
 */
export interface PlanToken {
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
     * Per-artifact hashes that contributed to this plan token.
     */
    artifacts: PlanArtifactHash[];
    /**
     * AI Model identifier used to generate this plan (e.g. 'gpt-4', 'claude-3').
     * Required for provenance.
     */
    model: string;
    /**
     * Engine identity that produced this plan.
     */
    engine_id: string;
    /**
     * Engine protocol version used when this plan was produced.
     */
    protocol_version: string;
    /**
     * Hash of the workspace state when the plan was created.
     */
    workspace_hash: string;
    /**
     * Timestamp when the plan was created (RFC3339).
     * @format date-time
     */
    created_at: string;

    /**
     * SHA256 digest of all policy configurations evaluated during flight-plan.
     * OPTIONAL but recommended for governance provenance.
     * Proves which policy set was active when plan-token was created.
     */
    policy_digest?: string;

    /**
     * SHA256 hash of governance context (OPA policies, ONNX models, gateway rules).
     * OPTIONAL but recommended for compliance verification.
     * Enables auditors to verify governance configuration at plan-time.
     */
    governance_hash?: string;
}
