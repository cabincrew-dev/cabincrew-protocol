package cabincrew

type MCPGatewayPolicyConfig struct {
	OnnxModels  []string         `json:"onnx_models,omitempty"`
	OpaPolicies []string         `json:"opa_policies,omitempty"`
	Rules       []MCPGatewayRule `json:"rules,omitempty"`
}

type MCPGatewayRule struct {
	Action   string       `json:"action"`
	Match    ParamsClass  `json:"match"`
	Metadata *ParamsClass `json:"metadata,omitempty"`
}

type ParamsClass struct {
}

type MCPGatewayRequest struct {
	Context   *ParamsClass `json:"context,omitempty"`
	Method    string       `json:"method"`
	Params    *ParamsClass `json:"params,omitempty"`
	RequestID string       `json:"request_id"`
	ServerID  string       `json:"server_id"`
	Source    *string      `json:"source,omitempty"`
	Timestamp string       `json:"timestamp"`
}

type MCPGatewayResponse struct {
	Approval         *MCPGatewayResponseApproval `json:"approval,omitempty"`
	Decision         LLMGatewayResponseDecision  `json:"decision"`
	RequestID        string                      `json:"request_id"`
	RewrittenRequest *ParamsClass                `json:"rewritten_request,omitempty"`
	Timestamp        string                      `json:"timestamp"`
	Violations       []string                    `json:"violations,omitempty"`
	Warnings         []string                    `json:"warnings,omitempty"`
}

type MCPGatewayResponseApproval struct {
	ApprovalID   *string `json:"approval_id,omitempty"`
	Reason       *string `json:"reason,omitempty"`
	RequiredRole *string `json:"required_role,omitempty"`
}
