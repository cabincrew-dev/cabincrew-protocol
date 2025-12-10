package cabincrew

// EngineInput defines the Input delivered via STDIN or CABINCREW_INPUT_FILE.
// Defined in schemas/draft/engine.schema.json
type EngineInput struct {
	ProtocolVersion   string                 `json:"protocol_version"`
	Mode              string                 `json:"mode"` // flight-plan, take-off
	Meta              EngineMeta             `json:"meta"`
	Config            map[string]interface{} `json:"config,omitempty"`
	Secrets           map[string]interface{} `json:"secrets,omitempty"`
	AllowedSecrets    []string               `json:"allowed_secrets,omitempty"`
	Context           map[string]interface{} `json:"context,omitempty"`
	Orchestrator      *EngineOrchestrator    `json:"orchestrator,omitempty"`
	ExpectedPlanToken string                 `json:"expected_plan_token,omitempty"`
}

type EngineMeta struct {
	WorkflowID string `json:"workflow_id"`
	StepID     string `json:"step_id"`
}

type EngineOrchestrator struct {
	RunIndex      float64 `json:"run_index,omitempty"`
	WorkspaceHash string  `json:"workspace_hash,omitempty"`
	ArtifactsSalt string  `json:"artifacts_salt,omitempty"`
}

// EngineOutput defines the Output delivered via STDOUT or CABINCREW_OUTPUT_FILE.
// Defined in schemas/draft/engine.schema.json
type EngineOutput struct {
	ProtocolVersion string           `json:"protocol_version"`
	EngineID        string           `json:"engine_id"`
	Mode            string           `json:"mode"`
	ReceiptID       string           `json:"receipt_id"`
	Status          string           `json:"status"` // success, failure
	Error           string           `json:"error,omitempty"`
	Warnings        []string         `json:"warnings,omitempty"`
	Diagnostics     interface{}      `json:"diagnostics,omitempty"`
	Artifacts       []EngineArtifact `json:"artifacts,omitempty"`
	Metrics         []EngineMetric   `json:"metrics,omitempty"`
	PlanToken       string           `json:"plan_token,omitempty"`
}

type EngineArtifact struct {
	Name string  `json:"name"`
	Role string  `json:"role"`
	Path string  `json:"path"`
	Hash string  `json:"hash"`
	Size float64 `json:"size,omitempty"`
}

type EngineMetric struct {
	Name  string                 `json:"name"`
	Value float64                `json:"value"`
	Tags  map[string]interface{} `json:"tags,omitempty"`
}
