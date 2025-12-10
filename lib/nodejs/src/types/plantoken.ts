export interface PlanArtifactHash {
    name: string;
    hash: string;
    size?: number;
}

/**
 * Cryptographic binding between a flight-plan and its subsequent take-off.
 * Defined in schemas/draft/plan-token.schema.json
 */
export interface PlanToken {
    /**
     * Primary plan token identifier, e.g. SHA256 over all plan artifacts + context.
     */
    token: string;
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
     */
    created_at: string;
}
