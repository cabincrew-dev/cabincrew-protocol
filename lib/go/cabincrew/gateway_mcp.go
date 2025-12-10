package cabincrew

// MCPGatewayRequest is an MCP request intercepted by the gateway.
// Defined in schemas/draft/mcp-gateway.json
type MCPGatewayRequest struct {
	RequestID string                 `json:"request_id"`
	Timestamp string                 `json:"timestamp"`
	Source    string                 `json:"source,omitempty"`
	ServerID  string                 `json:"server_id"`
	Method    string                 `json:"method"`
	Params    map[string]interface{} `json:"params,omitempty"`
	Context   map[string]interface{} `json:"context,omitempty"`
}

// MCPGatewayResponse is a decision produced by the MCP gateway.
// Defined in schemas/draft/mcp-gateway.json
type MCPGatewayResponse struct {
	RequestID        string                 `json:"request_id"`
	Timestamp        string                 `json:"timestamp"`
	Decision         string                 `json:"decision"` // allow, warn, deny, require_approval
	Warnings         []string               `json:"warnings,omitempty"`
	Violations       []string               `json:"violations,omitempty"`
	Approval         *GatewayApproval       `json:"approval,omitempty"`
	RewrittenRequest map[string]interface{} `json:"rewritten_request,omitempty"`
}

// MCPGatewayPolicyConfig is the OPA + ONNX policy configuration for the MCP Gateway.
// Defined in schemas/draft/mcp-gateway.json
type MCPGatewayPolicyConfig struct {
	OpaPolicies []string         `json:"opa_policies,omitempty"`
	OnnxModels  []string         `json:"onnx_models,omitempty"`
	Rules       []MCPGatewayRule `json:"rules,omitempty"`
}

type MCPGatewayRule struct {
	Match    map[string]interface{} `json:"match"`
	Action   string                 `json:"action"`
	Metadata map[string]interface{} `json:"metadata,omitempty"`
}
