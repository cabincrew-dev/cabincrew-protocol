package cabincrew

type AuditEvent struct {
	Approval                                                                   *AuditApproval       `json:"approval,omitempty"`
	Artifacts                                                                  []AuditArtifact      `json:"artifacts,omitempty"`
	Engine                                                                     *AuditEngine         `json:"engine,omitempty"`
	// Unique identifier for this audit event.                                                      
	EventID                                                                    string               `json:"event_id"`
	// Free-form event category.                                                                    
	EventType                                                                  string               `json:"event_type"`
	Gateway                                                                    *AuditGateway        `json:"gateway,omitempty"`
	IntegrityCheck                                                             *AuditIntegrity      `json:"integrity_check,omitempty"`
	Message                                                                    *string              `json:"message,omitempty"`
	// Cryptographic binding between a flight-plan and its subsequent take-off.                     
	// Defined in schemas/draft/plan-token.schema.json                                              
	PlanToken                                                                  *AuditEventPlanToken `json:"plan_token,omitempty"`
	Policy                                                                     *AuditPolicy         `json:"policy,omitempty"`
	Severity                                                                   *Severity            `json:"severity,omitempty"`
	// RFC3339 timestamp of when the event occurred.                                                
	Timestamp                                                                  string               `json:"timestamp"`
	Workflow                                                                   *AuditWorkflow       `json:"workflow,omitempty"`
}

type AuditApproval struct {
	ApprovalID   *string `json:"approval_id,omitempty"`
	Approved     *bool   `json:"approved,omitempty"`
	Approver     *string `json:"approver,omitempty"`
	Reason       *string `json:"reason,omitempty"`
	RequiredRole *string `json:"required_role,omitempty"`
}

type AuditArtifact struct {
	Hash *string  `json:"hash,omitempty"`
	Name *string  `json:"name,omitempty"`
	Path *string  `json:"path,omitempty"`
	Role *string  `json:"role,omitempty"`
	Size *float64 `json:"size,omitempty"`
}

type AuditEngine struct {
	EngineID  *string `json:"engine_id,omitempty"`
	Error     *string `json:"error,omitempty"`
	ReceiptID *string `json:"receipt_id,omitempty"`
	Status    *string `json:"status,omitempty"`
}

type AuditGateway struct {
	GatewayType    *string `json:"gateway_type,omitempty"`
	Model          *string `json:"model,omitempty"`
	PolicyDecision *string `json:"policy_decision,omitempty"`
	RequestID      *string `json:"request_id,omitempty"`
	Tool           *string `json:"tool,omitempty"`
}

type AuditIntegrity struct {
	ActualPlanToken   *string  `json:"actual_plan_token,omitempty"`
	ArtifactsMatch    *bool    `json:"artifacts_match,omitempty"`
	Differences       []string `json:"differences,omitempty"`
	ExpectedPlanToken *string  `json:"expected_plan_token,omitempty"`
	PlanTokenMatch    *bool    `json:"plan_token_match,omitempty"`
}

// Cryptographic binding between a flight-plan and its subsequent take-off.
// Defined in schemas/draft/plan-token.schema.json
type AuditEventPlanToken struct {
	// Per-artifact hashes that contributed to this plan token.                                              
	Artifacts                                                                       []PlanArtifactHash `json:"artifacts"`
	// Timestamp when the plan was created (RFC3339).                                                        
	CreatedAt                                                                       string                   `json:"created_at"`
	// Engine identity that produced this plan.                                                              
	EngineID                                                                        string                   `json:"engine_id"`
	// Engine protocol version used when this plan was produced.                                             
	ProtocolVersion                                                                 string                   `json:"protocol_version"`
	// Primary plan token identifier, e.g. SHA256 over all plan artifacts + context.                         
	Token                                                                           string                   `json:"token"`
	// Hash of the workspace state when the plan was created.                                                
	WorkspaceHash                                                                   string                   `json:"workspace_hash"`
}

type AuditPolicy struct {
	Decision   *string  `json:"decision,omitempty"`
	Engine     *string  `json:"engine,omitempty"`
	Violations []string `json:"violations,omitempty"`
	Warnings   []string `json:"warnings,omitempty"`
}

type AuditWorkflow struct {
	Mode       *string `json:"mode,omitempty"`
	StepID     *string `json:"step_id,omitempty"`
	WorkflowID *string `json:"workflow_id,omitempty"`
}

type Severity string

const (
	Critical Severity = "critical"
	Debug    Severity = "debug"
	Error    Severity = "error"
	Info     Severity = "info"
	Warning  Severity = "warning"
)
