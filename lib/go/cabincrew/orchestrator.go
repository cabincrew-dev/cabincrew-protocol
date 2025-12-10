package cabincrew

type ApprovalRequest struct {
	ApprovalID    string              `json:"approval_id"`
	EngineOutput  *EngineOutputClass  `json:"engine_output,omitempty"`
	Evidence      []PreflightEvidence `json:"evidence,omitempty"`
	PlanTokenHash *string             `json:"plan_token_hash,omitempty"`
	Reason        string              `json:"reason"`
	RequiredRole  string              `json:"required_role"`
	StepID        string              `json:"step_id"`
	WorkflowID    string              `json:"workflow_id"`
}

type PreflightEvidence struct {
	Hash string `json:"hash"`
	Name string `json:"name"`
	Path string `json:"path"`
}

type ApprovalResponse struct {
	ApprovalID string  `json:"approval_id"`
	Approved   bool    `json:"approved"`
	Approver   *string `json:"approver,omitempty"`
	Reason     *string `json:"reason,omitempty"`
	Timestamp  *string `json:"timestamp,omitempty"`
}

type PreflightInput struct {
	Context                                                                    *EngineOutputClass       `json:"context,omitempty"`
	EngineOutput                                                               EngineOutputClass        `json:"engine_output"`
	Evidence                                                                   []PreflightEvidence      `json:"evidence,omitempty"`
	Mode                                                                       Mode                     `json:"mode"`
	// Cryptographic binding between a flight-plan and its subsequent take-off.                         
	// Defined in schemas/draft/plan-token.schema.json                                                  
	PlanToken                                                                  *PlanToken `json:"plan_token,omitempty"`
	StepID                                                                     string                   `json:"step_id"`
	WorkflowID                                                                 string                   `json:"workflow_id"`
}

// Cryptographic binding between a flight-plan and its subsequent take-off.
// Defined in schemas/draft/plan-token.schema.json
type PreflightOutput struct {
	Decision   PreflightOutputDecision `json:"decision"`
	Requires   *PreflightRequires      `json:"requires,omitempty"`
	Violations []string                `json:"violations,omitempty"`
	Warnings   []string                `json:"warnings,omitempty"`
}

type PreflightRequires struct {
	Reason *string `json:"reason,omitempty"`
	Role   *string `json:"role,omitempty"`
}

type WorkflowState struct {
	LastDecision  *string `json:"last_decision,omitempty"`
	PlanTokenHash *string `json:"plan_token_hash,omitempty"`
	State         State   `json:"state"`
	StepID        *string `json:"step_id,omitempty"`
	WorkflowID    *string `json:"workflow_id,omitempty"`
}

// Cryptographic binding between a flight-plan and its subsequent take-off.
// Defined in schemas/draft/plan-token.schema.json
type PreflightOutputDecision string

const (
	DecisionALLOW           PreflightOutputDecision = "ALLOW"
	DecisionDENY            PreflightOutputDecision = "DENY"
	DecisionREQUIREAPPROVAL PreflightOutputDecision = "REQUIRE_APPROVAL"
	DecisionWARN            PreflightOutputDecision = "WARN"
)

type State string

const (
	Approved           State = "APPROVED"
	ArtifactsValidated State = "ARTIFACTS_VALIDATED"
	AwaitingApproval   State = "AWAITING_APPROVAL"
	Completed          State = "COMPLETED"
	ExecutionComplete  State = "EXECUTION_COMPLETE"
	Failed             State = "FAILED"
	Init               State = "INIT"
	PlanGenerated      State = "PLAN_GENERATED"
	PlanRunning        State = "PLAN_RUNNING"
	PreFlightRunning   State = "PRE_FLIGHT_RUNNING"
	PreflightComplete  State = "PREFLIGHT_COMPLETE"
	ReadyForTakeoff    State = "READY_FOR_TAKEOFF"
	TakeoffRunning     State = "TAKEOFF_RUNNING"
	TokenCreated       State = "TOKEN_CREATED"
)

// Inline content for small artifacts.
// Can be string, object, array, or null.