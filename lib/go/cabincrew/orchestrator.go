package cabincrew

// PreflightInput is input given to the preflight (policy) stage.
// Defined in schemas/draft/orchestrator.schema.json
type PreflightInput struct {
	WorkflowID   string                 `json:"workflow_id"`
	StepID       string                 `json:"step_id"`
	Mode         string                 `json:"mode"`
	EngineOutput map[string]interface{} `json:"engine_output"`
	Evidence     []PreflightEvidence    `json:"evidence,omitempty"`
	Context      map[string]interface{} `json:"context,omitempty"`
	PlanToken    *PlanToken             `json:"plan_token,omitempty"`
}

type PreflightEvidence struct {
	Name string `json:"name"`
	Path string `json:"path"`
	Hash string `json:"hash"`
}

// PreflightOutput is unified decision structure emitted after OPA/ONNX evaluation.
// Defined in schemas/draft/orchestrator.schema.json
type PreflightOutput struct {
	Decision   string             `json:"decision"` // ALLOW, WARN, REQUIRE_APPROVAL, DENY
	Violations []string           `json:"violations,omitempty"`
	Warnings   []string           `json:"warnings,omitempty"`
	Requires   *PreflightRequires `json:"requires,omitempty"`
}

type PreflightRequires struct {
	Role   string `json:"role,omitempty"`
	Reason string `json:"reason,omitempty"`
}

// ApprovalRequest is approval packet sent to a human or approval system.
// Defined in schemas/draft/orchestrator.schema.json
type ApprovalRequest struct {
	ApprovalID    string                 `json:"approval_id"`
	WorkflowID    string                 `json:"workflow_id"`
	StepID        string                 `json:"step_id"`
	Reason        string                 `json:"reason"`
	RequiredRole  string                 `json:"required_role"`
	EngineOutput  map[string]interface{} `json:"engine_output,omitempty"`
	Evidence      []PreflightEvidence    `json:"evidence,omitempty"`
	PlanTokenHash string                 `json:"plan_token_hash,omitempty"`
}

// ApprovalResponse is response from the human approver or approval system.
// Defined in schemas/draft/orchestrator.schema.json
type ApprovalResponse struct {
	ApprovalID string `json:"approval_id"`
	Approved   bool   `json:"approved"`
	Approver   string `json:"approver,omitempty"`
	Reason     string `json:"reason,omitempty"`
	Timestamp  string `json:"timestamp,omitempty"`
}

// WorkflowState is state machine snapshot for the orchestrator.
// Defined in schemas/draft/orchestrator.schema.json
type WorkflowState struct {
	State         string `json:"state"`
	WorkflowID    string `json:"workflow_id,omitempty"`
	StepID        string `json:"step_id,omitempty"`
	LastDecision  string `json:"last_decision,omitempty"`
	PlanTokenHash string `json:"plan_token_hash,omitempty"`
}
