package cabincrew

type LLMGatewayPolicyConfig struct {
	ModelRouting *ModelRoutingClass `json:"model_routing,omitempty"`
	OnnxModels   []string           `json:"onnx_models,omitempty"`
	OpaPolicies  []string           `json:"opa_policies,omitempty"`
	Rules        []LLMGatewayRule   `json:"rules,omitempty"`
}

type ModelRoutingClass struct {
}

type LLMGatewayRule struct {
	Action   string             `json:"action"`
	Match    ModelRoutingClass  `json:"match"`
	Metadata *ModelRoutingClass `json:"metadata,omitempty"`
}

type LLMGatewayRequest struct {
	Context   *ModelRoutingClass `json:"context,omitempty"`
	Input     ModelRoutingClass  `json:"input"`
	Model     string             `json:"model"`
	Provider  *string            `json:"provider,omitempty"`
	RequestID string             `json:"request_id"`
	Source    *string            `json:"source,omitempty"`
	Timestamp string             `json:"timestamp"`
}

type LLMGatewayResponse struct {
	Approval       *LLMGatewayResponseApproval `json:"approval,omitempty"`
	Decision       LLMGatewayResponseDecision  `json:"decision"`
	GatewayPayload *ModelRoutingClass          `json:"gateway_payload,omitempty"`
	RequestID      string                      `json:"request_id"`
	RewrittenInput *ModelRoutingClass          `json:"rewritten_input,omitempty"`
	RoutedModel    *string                     `json:"routed_model,omitempty"`
	Timestamp      string                      `json:"timestamp"`
	Violations     []string                    `json:"violations,omitempty"`
	Warnings       []string                    `json:"warnings,omitempty"`
}

type LLMGatewayResponseApproval struct {
	ApprovalID   *string `json:"approval_id,omitempty"`
	Reason       *string `json:"reason,omitempty"`
	RequiredRole *string `json:"required_role,omitempty"`
}

type LLMGatewayResponseDecision string

const (
	Allow           LLMGatewayResponseDecision = "allow"
	Deny            LLMGatewayResponseDecision = "deny"
	RequireApproval LLMGatewayResponseDecision = "require_approval"
	Warn            LLMGatewayResponseDecision = "warn"
)
