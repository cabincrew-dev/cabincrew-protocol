package cabincrew

type PlanArtifactHash struct {
	Hash string   `json:"hash"`
	Name string   `json:"name"`
	Size *float64 `json:"size,omitempty"`
}

type PlanToken struct {
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
