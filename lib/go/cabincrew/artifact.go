package cabincrew

// Artifact represents the canonical artifact interface.
// Defined in schemas/draft/artifact.schema.json
type Artifact struct {
	// Type of artifact (file, diff, patch, action, message, etc). Free-form and engine-defined.
	ArtifactType string `json:"artifact_type"`

	// Operation to perform with this artifact (create, update, delete, apply, execute, etc). Free-form and engine-defined.
	Action string `json:"action"`

	// Path, resource, or identifier this artifact applies to. Optional.
	Target string `json:"target,omitempty"`

	// MIME type describing content.
	Mime string `json:"mime"`

	// Inline content for small artifacts.
	// Can be string, object, array, or null.
	// We use interface{} to handle oneOf types.
	Body interface{} `json:"body,omitempty"`

	// Indicates an external data file within the artifact directory.
	BodyFile string `json:"body_file,omitempty"`

	// Arbitrary metadata. Optional.
	Metadata map[string]interface{} `json:"metadata,omitempty"`
}
