package cabincrew

// AuditEvent represents the canonical schema for all audit log events.
// Defined in schemas/draft/audit-event.schema.json
type AuditEvent struct {
	EventID   string          `json:"event_id"`
	Timestamp string          `json:"timestamp"`
	EventType string          `json:"event_type"`
	Workflow  *AuditWorkflow  `json:"workflow,omitempty"`
	Engine    *AuditEngine    `json:"engine,omitempty"`
	PlanToken *PlanToken      `json:"plan_token,omitempty"`
	Artifacts []AuditArtifact `json:"artifacts,omitempty"`
	Policy    *AuditPolicy    `json:"policy,omitempty"`
	Approval  *AuditApproval  `json:"approval,omitempty"`
	Integrity *AuditIntegrity `json:"integrity_check,omitempty"`
	Gateway   *AuditGateway   `json:"gateway,omitempty"`
	Message   string          `json:"message,omitempty"`
	Severity  string          `json:"severity,omitempty"`
}

type AuditWorkflow struct {
	WorkflowID string `json:"workflow_id,omitempty"`
	StepID     string `json:"step_id,omitempty"`
	Mode       string `json:"mode,omitempty"`
}

type AuditEngine struct {
	EngineID  string `json:"engine_id,omitempty"`
	ReceiptID string `json:"receipt_id,omitempty"`
	Status    string `json:"status,omitempty"`
	Error     string `json:"error,omitempty"`
}

type AuditArtifact struct {
	Name string  `json:"name,omitempty"`
	Role string  `json:"role,omitempty"`
	Path string  `json:"path,omitempty"`
	Hash string  `json:"hash,omitempty"`
	Size float64 `json:"size,omitempty"`
}

type AuditPolicy struct {
	Decision   string   `json:"decision,omitempty"`
	Violations []string `json:"violations,omitempty"`
	Warnings   []string `json:"warnings,omitempty"`
	Engine     string   `json:"engine,omitempty"`
}

type AuditApproval struct {
	ApprovalID   string `json:"approval_id,omitempty"`
	RequiredRole string `json:"required_role,omitempty"`
	Approved     bool   `json:"approved,omitempty"`
	Approver     string `json:"approver,omitempty"`
	Reason       string `json:"reason,omitempty"`
}

type AuditIntegrity struct {
	ExpectedPlanToken string   `json:"expected_plan_token,omitempty"`
	ActualPlanToken   string   `json:"actual_plan_token,omitempty"`
	PlanTokenMatch    bool     `json:"plan_token_match,omitempty"`
	ArtifactsMatch    bool     `json:"artifacts_match,omitempty"`
	Differences       []string `json:"differences,omitempty"`
}

type AuditGateway struct {
	GatewayType    string `json:"gateway_type,omitempty"`
	RequestID      string `json:"request_id,omitempty"`
	Model          string `json:"model,omitempty"`
	Tool           string `json:"tool,omitempty"`
	PolicyDecision string `json:"policy_decision,omitempty"`
}
