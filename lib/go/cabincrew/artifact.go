package cabincrew

type Artifact struct {
	// Operation to perform with this artifact (create, update, delete, apply, execute, etc).                     
	// Free-form and engine-defined.                                                                              
	Action                                                                                      string            `json:"action"`
	// Type of artifact (file, diff, patch, action, message, etc). Free-form and engine-defined.                  
	ArtifactType                                                                                string            `json:"artifact_type"`
	// Inline content for small artifacts.                                                                        
	// Can be string, object, array, or null.                                                                     
	Body                                                                                        *Body             `json:"body"`
	// Indicates an external data file within the artifact directory.                                             
	BodyFile                                                                                    *string           `json:"body_file,omitempty"`
	// Arbitrary metadata. Optional.                                                                              
	Metadata                                                                                    *ArtifactMetadata `json:"metadata,omitempty"`
	// MIME type describing content.                                                                              
	MIME                                                                                        string            `json:"mime"`
	// Path, resource, or identifier this artifact applies to. Optional.                                          
	Target                                                                                      *string           `json:"target,omitempty"`
}

// Arbitrary metadata. Optional.
type ArtifactMetadata struct {
}

// Canonical schema for all audit log events.
// Defined in schemas/draft/audit-event.schema.json
type Body struct {
	AnythingArray []interface{}
	AnythingMap   map[string]interface{}
	String        *string
}
