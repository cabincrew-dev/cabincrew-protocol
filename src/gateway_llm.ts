import { Decision } from './orchestrator';

export interface LLMGatewayRequest {
    request_id: string;
    /** @format date-time */
    timestamp: string;
    source?: string;
    model: string;
    provider?: string;
    input: Record<string, any>;
    context?: Record<string, any>;
}

export interface GatewayApproval {
    approval_id?: string;
    required_role?: string;
    reason?: string;
}

export interface LLMGatewayResponse {
    request_id: string;
    /** @format date-time */
    timestamp: string;
    decision: Decision;
    warnings?: string[];
    violations?: string[];
    approval?: GatewayApproval;
    routed_model?: string;
    rewritten_input?: Record<string, any>;
    gateway_payload?: Record<string, any>;
}

export interface LLMGatewayRule {
    match: Record<string, any>;
    action: string;
    metadata?: Record<string, any>;
}

export interface LLMGatewayPolicyConfig {
    opa_policies?: string[];
    onnx_models?: string[];
    model_routing?: Record<string, any>;
    rules?: LLMGatewayRule[];
}
