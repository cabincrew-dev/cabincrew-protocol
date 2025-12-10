package cabincrew

// PlanToken represents the cryptographic binding between a flight-plan and its subsequent take-off.
// Defined in schemas/draft/plan-token.schema.json
type PlanToken struct {
	// Primary plan token identifier, e.g. SHA256 over all plan artifacts + context.
	Token string `json:"token"`

	// Per-artifact hashes that contributed to this plan token.
	Artifacts []PlanArtifactHash `json:"artifacts"`

	// Engine identity that produced this plan.
	EngineID string `json:"engine_id"`

	// Engine protocol version used when this plan was produced.
	ProtocolVersion string `json:"protocol_version"`

	// Hash of the workspace state when the plan was created.
	WorkspaceHash string `json:"workspace_hash"`

	// Timestamp when the plan was created (RFC3339).
	CreatedAt string `json:"created_at"`
}

type PlanArtifactHash struct {
	Name string  `json:"name"`
	Hash string  `json:"hash"`
	Size float64 `json:"size,omitempty"`
}
