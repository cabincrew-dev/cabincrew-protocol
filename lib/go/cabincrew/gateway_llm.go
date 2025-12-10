package cabincrew

// LLMGatewayRequest is a request to an LLM intercepted by the gateway.
// Defined in schemas/draft/llm-gateway.json
type LLMGatewayRequest struct {
	RequestID string                 `json:"request_id"`
	Timestamp string                 `json:"timestamp"`
	Source    string                 `json:"source,omitempty"`
	Model     string                 `json:"model"`
	Provider  string                 `json:"provider,omitempty"`
	Input     map[string]interface{} `json:"input"`
	Context   map[string]interface{} `json:"context,omitempty"`
}

// LLMGatewayResponse is a decision produced by the LLM gateway.
// Defined in schemas/draft/llm-gateway.json
type LLMGatewayResponse struct {
	RequestID      string                 `json:"request_id"`
	Timestamp      string                 `json:"timestamp"`
	Decision       string                 `json:"decision"` // allow, warn, deny, require_approval
	Warnings       []string               `json:"warnings,omitempty"`
	Violations     []string               `json:"violations,omitempty"`
	Approval       *GatewayApproval       `json:"approval,omitempty"`
	RoutedModel    string                 `json:"routed_model,omitempty"`
	RewrittenInput map[string]interface{} `json:"rewritten_input,omitempty"`
	GatewayPayload map[string]interface{} `json:"gateway_payload,omitempty"`
}

type GatewayApproval struct {
	ApprovalID   string `json:"approval_id,omitempty"`
	RequiredRole string `json:"required_role,omitempty"`
	Reason       string `json:"reason,omitempty"`
}

// LLMGatewayPolicyConfig is the OPA + ONNX policy configuration for the LLM Gateway.
// Defined in schemas/draft/llm-gateway.json
type LLMGatewayPolicyConfig struct {
	OpaPolicies  []string               `json:"opa_policies,omitempty"`
	OnnxModels   []string               `json:"onnx_models,omitempty"`
	ModelRouting map[string]interface{} `json:"model_routing,omitempty"`
	Rules        []LLMGatewayRule       `json:"rules,omitempty"`
}

type LLMGatewayRule struct {
	Match    map[string]interface{} `json:"match"`
	Action   string                 `json:"action"`
	Metadata map[string]interface{} `json:"metadata,omitempty"`
}
