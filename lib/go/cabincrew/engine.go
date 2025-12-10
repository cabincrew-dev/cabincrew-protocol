package cabincrew

type EngineInput struct {
	AllowedSecrets                                 []string               `json:"allowed_secrets,omitempty"`
	Config                                         map[string]interface{} `json:"config,omitempty"`
	Context                                        map[string]interface{} `json:"context,omitempty"`
	ExpectedPlanToken                              *string                `json:"expected_plan_token,omitempty"`
	Meta                                           EngineMeta             `json:"meta"`
	// Execution mode: 'flight-plan' or 'take-off'.                       
	Mode                                           string                 `json:"mode"`
	Orchestrator                                   *EngineOrchestrator    `json:"orchestrator,omitempty"`
	ProtocolVersion                                string                 `json:"protocol_version"`
	Secrets                                        map[string]interface{} `json:"secrets,omitempty"`
}

type EngineMeta struct {
	StepID     string `json:"step_id"`
	WorkflowID string `json:"workflow_id"`
}

type EngineOrchestrator struct {
	ArtifactsSalt *string  `json:"artifacts_salt,omitempty"`
	RunIndex      *float64 `json:"run_index,omitempty"`
	WorkspaceHash *string  `json:"workspace_hash,omitempty"`
}

// Output delivered via STDOUT or CABINCREW_OUTPUT_FILE.
// Defined in schemas/draft/engine.schema.json
type EngineOutput struct {
	Artifacts                                         []EngineArtifact `json:"artifacts,omitempty"`
	Diagnostics                                       interface{}      `json:"diagnostics"`
	EngineID                                          string           `json:"engine_id"`
	Error                                             *string          `json:"error,omitempty"`
	Metrics                                           []EngineMetric   `json:"metrics,omitempty"`
	Mode                                              string           `json:"mode"`
	// SHA256 hash referencing a plan-token.json file.                 
	PlanToken                                         *string          `json:"plan_token,omitempty"`
	ProtocolVersion                                   string           `json:"protocol_version"`
	ReceiptID                                         string           `json:"receipt_id"`
	// Execution status: 'success' or 'failure'.                       
	Status                                            string           `json:"status"`
	Warnings                                          []string         `json:"warnings,omitempty"`
}

type EngineArtifact struct {
	Hash string   `json:"hash"`
	Name string   `json:"name"`
	Path string   `json:"path"`
	Role string   `json:"role"`
	Size *float64 `json:"size,omitempty"`
}

type EngineMetric struct {
	Name  string                 `json:"name"`
	Tags  map[string]interface{} `json:"tags,omitempty"`
	Value float64                `json:"value"`
}

type EngineOutputClass struct {
}

type Mode string

const (
	FlightPlan Mode = "flight-plan"
	TakeOff    Mode = "take-off"
)
