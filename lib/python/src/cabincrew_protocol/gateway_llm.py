from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LLMGatewayRequest(BaseModel):
    """
    A request to an LLM intercepted by the gateway.
    Defined in schemas/draft/llm-gateway.json
    """
    request_id: str
    timestamp: str
    source: Optional[str] = None
    model: str
    provider: Optional[str] = None
    input: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None

class GatewayApproval(BaseModel):
    approval_id: Optional[str] = None
    required_role: Optional[str] = None
    reason: Optional[str] = None

class LLMGatewayResponse(BaseModel):
    """
    Decision produced by the LLM gateway.
    Defined in schemas/draft/llm-gateway.json
    """
    request_id: str
    timestamp: str
    decision: str = Field(..., description="allow, warn, deny, require_approval")
    warnings: Optional[List[str]] = None
    violations: Optional[List[str]] = None
    approval: Optional[GatewayApproval] = None
    routed_model: Optional[str] = None
    rewritten_input: Optional[Dict[str, Any]] = None
    gateway_payload: Optional[Dict[str, Any]] = None

class LLMGatewayRule(BaseModel):
    match: Dict[str, Any]
    action: str
    metadata: Optional[Dict[str, Any]] = None

class LLMGatewayPolicyConfig(BaseModel):
    """
    OPA + ONNX policy configuration for the LLM Gateway.
    Defined in schemas/draft/llm-gateway.json
    """
    opa_policies: Optional[List[str]] = None
    onnx_models: Optional[List[str]] = None
    model_routing: Optional[Dict[str, Any]] = None
    rules: Optional[List[LLMGatewayRule]] = None
