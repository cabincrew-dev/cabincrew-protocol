from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .gateway_llm import GatewayApproval

class MCPGatewayRequest(BaseModel):
    """
    An MCP request intercepted by the gateway.
    Defined in schemas/draft/mcp-gateway.json
    """
    request_id: str
    timestamp: str
    source: Optional[str] = None
    server_id: str
    method: str
    params: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None

class MCPGatewayResponse(BaseModel):
    """
    Decision produced by the MCP gateway.
    Defined in schemas/draft/mcp-gateway.json
    """
    request_id: str
    timestamp: str
    decision: str = Field(..., description="allow, warn, deny, require_approval")
    warnings: Optional[List[str]] = None
    violations: Optional[List[str]] = None
    approval: Optional[GatewayApproval] = None
    rewritten_request: Optional[Dict[str, Any]] = None

class MCPGatewayRule(BaseModel):
    match: Dict[str, Any]
    action: str
    metadata: Optional[Dict[str, Any]] = None

class MCPGatewayPolicyConfig(BaseModel):
    """
    OPA + ONNX policy configuration for the MCP Gateway.
    Defined in schemas/draft/mcp-gateway.json
    """
    opa_policies: Optional[List[str]] = None
    onnx_models: Optional[List[str]] = None
    rules: Optional[List[MCPGatewayRule]] = None
