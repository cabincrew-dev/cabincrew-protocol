import { GatewayApproval } from './gateway_llm';
import { Decision } from './orchestrator';

export interface MCPGatewayRequest {
    request_id: string;
    timestamp: string;
    source?: string;
    server_id: string;
    method: string;
    params?: Record<string, any>;
    context?: Record<string, any>;
}

export interface MCPGatewayResponse {
    request_id: string;
    timestamp: string;
    decision: Decision;
    warnings?: string[];
    violations?: string[];
    approval?: GatewayApproval;
    rewritten_request?: Record<string, any>;
}

export interface MCPGatewayRule {
    match: Record<string, any>;
    action: string;
    metadata?: Record<string, any>;
}

export interface MCPGatewayPolicyConfig {
    opa_policies?: string[];
    onnx_models?: string[];
    rules?: MCPGatewayRule[];
}
