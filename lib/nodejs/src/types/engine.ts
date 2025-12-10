export interface EngineMeta {
    workflow_id: string;
    step_id: string;
}

export interface EngineOrchestrator {
    run_index?: number;
    workspace_hash?: string;
    artifacts_salt?: string;
}

/**
 * Input delivered via STDIN or CABINCREW_INPUT_FILE.
 * Defined in schemas/draft/engine.schema.json
 */
export interface EngineInput {
    protocol_version: string;
    /**
     * Execution mode: 'flight-plan' or 'take-off'.
     */
    mode: string;
    meta: EngineMeta;
    config?: Record<string, any>;
    secrets?: Record<string, any>;
    allowed_secrets?: string[];
    context?: Record<string, any>;
    orchestrator?: EngineOrchestrator;
    expected_plan_token?: string;
}

export interface EngineArtifact {
    name: string;
    role: string;
    path: string;
    hash: string;
    size?: number;
}

export interface EngineMetric {
    name: string;
    value: number;
    tags?: Record<string, any>;
}

/**
 * Output delivered via STDOUT or CABINCREW_OUTPUT_FILE.
 * Defined in schemas/draft/engine.schema.json
 */
export interface EngineOutput {
    protocol_version: string;
    engine_id: string;
    mode: string;
    receipt_id: string;
    /**
     * Execution status: 'success' or 'failure'.
     */
    status: string;

    error?: string;
    warnings?: string[];
    diagnostics?: any;
    artifacts?: EngineArtifact[];
    metrics?: EngineMetric[];
    /**
     * SHA256 hash referencing a plan-token.json file.
     */
    plan_token?: string;
}
