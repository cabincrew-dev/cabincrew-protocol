package cabincrew

import "time"



type CabinCrewProtocol struct {
	AggregationMethod      *AggregationMethod      `json:"AggregationMethod,omitempty"`
	AnyMap                 map[string]interface{}  `json:"AnyMap,omitempty"`
	ApprovalReceivedData   *ApprovalReceivedData   `json:"ApprovalReceivedData,omitempty"`
	ApprovalRecord         *ApprovalRecord         `json:"ApprovalRecord,omitempty"`
	ApprovalRequest        *ApprovalRequest        `json:"ApprovalRequest,omitempty"`
	ApprovalRequestedData  *ApprovalRequestedData  `json:"ApprovalRequestedData,omitempty"`
	ApprovalResponse       *ApprovalResponse       `json:"ApprovalResponse,omitempty"`
	Artifact               *Artifact               `json:"Artifact,omitempty"`
	ArtifactCreatedData    *ArtifactCreatedData    `json:"ArtifactCreatedData,omitempty"`
	ArtifactRecord         *ArtifactRecord         `json:"ArtifactRecord,omitempty"`
	AuditApproval          *AuditApproval          `json:"AuditApproval,omitempty"`
	AuditArtifact          *AuditArtifact          `json:"AuditArtifact,omitempty"`
	AuditEngine            *AuditEngine            `json:"AuditEngine,omitempty"`
	AuditEvent             *AuditEvent             `json:"AuditEvent,omitempty"`
	AuditGateway           *AuditGateway           `json:"AuditGateway,omitempty"`
	AuditIntegrity         *AuditIntegrity         `json:"AuditIntegrity,omitempty"`
	AuditPolicy            *AuditPolicy            `json:"AuditPolicy,omitempty"`
	AuditWorkflow          *AuditWorkflow          `json:"AuditWorkflow,omitempty"`
	Decision               *Decision               `json:"Decision,omitempty"`
	DecisionSeverity       *float64                `json:"DecisionSeverity,omitempty"`
	EngineArtifact         *EngineArtifact         `json:"EngineArtifact,omitempty"`
	EngineInput            *EngineInput            `json:"EngineInput,omitempty"`
	EngineMeta             *EngineMeta             `json:"EngineMeta,omitempty"`
	EngineMetric           *EngineMetric           `json:"EngineMetric,omitempty"`
	EngineOrchestrator     *EngineOrchestrator     `json:"EngineOrchestrator,omitempty"`
	EngineOutput           *EngineOutput           `json:"EngineOutput,omitempty"`
	GatewayApproval        *GatewayApproval        `json:"GatewayApproval,omitempty"`
	LLMGatewayPolicyConfig *LLMGatewayPolicyConfig `json:"LLMGatewayPolicyConfig,omitempty"`
	LLMGatewayRequest      *LLMGatewayRequest      `json:"LLMGatewayRequest,omitempty"`
	LLMGatewayResponse     *LLMGatewayResponse     `json:"LLMGatewayResponse,omitempty"`
	LLMGatewayRule         *LLMGatewayRule         `json:"LLMGatewayRule,omitempty"`
	MCPGatewayPolicyConfig *MCPGatewayPolicyConfig `json:"MCPGatewayPolicyConfig,omitempty"`
	MCPGatewayRequest      *MCPGatewayRequest      `json:"MCPGatewayRequest,omitempty"`
	MCPGatewayResponse     *MCPGatewayResponse     `json:"MCPGatewayResponse,omitempty"`
	MCPGatewayRule         *MCPGatewayRule         `json:"MCPGatewayRule,omitempty"`
	Mode                   *Mode                   `json:"Mode,omitempty"`
	PlanArtifactHash       *PlanArtifactHash       `json:"PlanArtifactHash,omitempty"`
	PlanToken              *PlanToken              `json:"PlanToken,omitempty"`
	PolicyEvaluatedData    *PolicyEvaluatedData    `json:"PolicyEvaluatedData,omitempty"`
	PolicyEvaluation       *PolicyEvaluation       `json:"PolicyEvaluation,omitempty"`
	PolicyEvaluationRecord *PolicyEvaluationRecord `json:"PolicyEvaluationRecord,omitempty"`
	PreflightEvidence      *PreflightEvidence      `json:"PreflightEvidence,omitempty"`
	PreflightInput         *PreflightInput         `json:"PreflightInput,omitempty"`
	PreflightOutput        *PreflightOutput        `json:"PreflightOutput,omitempty"`
	PreflightRequires      *PreflightRequires      `json:"PreflightRequires,omitempty"`
	RecordStringAny        map[string]interface{}  `json:"RecordStringAny,omitempty"`
	State                  *State                  `json:"State,omitempty"`
	StepCompletedData      *StepCompletedData      `json:"StepCompletedData,omitempty"`
	StepStartedData        *StepStartedData        `json:"StepStartedData,omitempty"`
	WALEntry               *WALEntry               `json:"WALEntry,omitempty"`
	WALEntryData           *WALEntryData           `json:"WALEntryData,omitempty"`
	WALEntryType           *WALEntryType           `json:"WALEntryType,omitempty"`
	WorkflowCompletedData  *WorkflowCompletedData  `json:"WorkflowCompletedData,omitempty"`
	WorkflowFailedData     *WorkflowFailedData     `json:"WorkflowFailedData,omitempty"`
	WorkflowStartedData    *WorkflowStartedData    `json:"WorkflowStartedData,omitempty"`
	WorkflowState          *WorkflowState          `json:"WorkflowState,omitempty"`
	WorkflowStateRecord    *WorkflowStateRecord    `json:"WorkflowStateRecord,omitempty"`
}

type ApprovalReceivedData struct {
	ApprovalID string `json:"approval_id"`
	Approved   bool   `json:"approved"`
	Approver   string `json:"approver"`
}


// Durable approval record.
// Tracks who approved what, when, bound to specific plan-token hash.
type ApprovalRecord struct {
	ApprovalID     string    `json:"approval_id"`
	Approved       bool      `json:"approved"`
	ApprovedAt     time.Time `json:"approved_at"`
	Approver       string    `json:"approver"`
	EvidenceHashes []string  `json:"evidence_hashes,omitempty"`
	PlanTokenHash  string    `json:"plan_token_hash"`
	Reason         *string   `json:"reason,omitempty"`
	StepID         string    `json:"step_id"`
}

// Request for human approval before proceeding with execution.
//
// Security: The plan_token_hash MUST be verified to match the current plan-token
// to prevent approval replay attacks against mutated plans.
type ApprovalRequest struct {
	ApprovalID                                                                          string                 `json:"approval_id"`
	EngineOutput                                                                        map[string]interface{} `json:"engine_output,omitempty"`
	Evidence                                                                            []PreflightEvidence    `json:"evidence,omitempty"`
	// SHA256 hash of the plan-token that this approval is bound to.                                           
	// REQUIRED to prevent approval replay attacks.                                                            
	// The orchestrator MUST verify this matches the current plan-token before accepting                       
	// approval.                                                                                               
	PlanTokenHash                                                                       string                 `json:"plan_token_hash"`
	Reason                                                                              string                 `json:"reason"`
	RequiredRole                                                                        string                 `json:"required_role"`
	StepID                                                                              string                 `json:"step_id"`
	WorkflowID                                                                          string                 `json:"workflow_id"`
}

type PreflightEvidence struct {
	Hash string `json:"hash"`
	Name string `json:"name"`
	Path string `json:"path"`
}

type ApprovalRequestedData struct {
	ApprovalID   string `json:"approval_id"`
	RequiredRole string `json:"required_role"`
	StepID       string `json:"step_id"`
}

type ApprovalResponse struct {
	ApprovalID string  `json:"approval_id"`
	Approved   bool    `json:"approved"`
	Approver   *string `json:"approver,omitempty"`
	Reason     *string `json:"reason,omitempty"`
	Timestamp  *string `json:"timestamp,omitempty"`
}

// Canonical artifact interface.
// Defined in schemas/draft/artifact.schema.json
type Artifact struct {
	// Operation to perform with this artifact (create, update, delete, apply, execute, etc).                          
	// Free-form and engine-defined.                                                                                   
	Action                                                                                      string                 `json:"action"`
	// Type of artifact (file, diff, patch, action, message, etc). Free-form and engine-defined.                       
	ArtifactType                                                                                string                 `json:"artifact_type"`
	// Inline content for small artifacts.                                                                             
	// Can be string, object, array, or null.                                                                          
	Body                                                                                        *Body                  `json:"body"`
	// Indicates an external data file within the artifact directory.                                                  
	BodyFile                                                                                    *string                `json:"body_file,omitempty"`
	// Arbitrary metadata. Optional.                                                                                   
	Metadata                                                                                    map[string]interface{} `json:"metadata,omitempty"`
	// MIME type describing content.                                                                                   
	MIME                                                                                        string                 `json:"mime"`
	// Path, resource, or identifier this artifact applies to. Optional.                                               
	Target                                                                                      *string                `json:"target,omitempty"`
}

type ArtifactCreatedData struct {
	ArtifactHash string `json:"artifact_hash"`
	ArtifactID   string `json:"artifact_id"`
	ArtifactType string `json:"artifact_type"`
}

// Durable artifact record.
// Tracks artifacts with SHA256 hashes for integrity verification.
type ArtifactRecord struct {
	ArtifactHash string                 `json:"artifact_hash"`
	ArtifactID   string                 `json:"artifact_id"`
	ArtifactType string                 `json:"artifact_type"`
	CreatedAt    time.Time              `json:"created_at"`
	Metadata     map[string]interface{} `json:"metadata,omitempty"`
	StepID       string                 `json:"step_id"`
}

// Audit record for approval events.
// Extended to ensure approval binding is auditable.
type AuditApproval struct {
	// Unique approval identifier.                                             
	// REQUIRED to correlate request and response.                             
	ApprovalID                                                       string    `json:"approval_id"`
	// Whether approval was granted.                                           
	// REQUIRED for audit trail.                                               
	Approved                                                         bool      `json:"approved"`
	// Identity of the approver.                                               
	// REQUIRED for accountability.                                            
	Approver                                                         string    `json:"approver"`
	// SHA256 hash of the plan-token this approval is bound to.                
	// REQUIRED to prove approval binding and prevent replay attacks.          
	PlanTokenHash                                                    string    `json:"plan_token_hash"`
	// Optional reason for approval/denial.                                    
	Reason                                                           *string   `json:"reason,omitempty"`
	// Required role for this approval.                                        
	// REQUIRED to verify authorization.                                       
	RequiredRole                                                     string    `json:"required_role"`
	// ISO 8601 timestamp when approval was granted/denied.                    
	// REQUIRED for temporal ordering.                                         
	Timestamp                                                        time.Time `json:"timestamp"`
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

// Canonical schema for all audit log events.
// Defined in schemas/draft/audit-event.schema.json
type AuditEvent struct {
	// Audit record for approval events.                                                                    
	// Extended to ensure approval binding is auditable.                                                    
	Approval                                                                                *AuditApproval  `json:"approval,omitempty"`
	Artifacts                                                                               []AuditArtifact `json:"artifacts,omitempty"`
	// Hash of the previous event in the chain. Allows for ledger-style verification.                       
	ChainHash                                                                               *string         `json:"chain_hash,omitempty"`
	Engine                                                                                  *AuditEngine    `json:"engine,omitempty"`
	// Unique identifier for this audit event.                                                              
	EventID                                                                                 string          `json:"event_id"`
	// Free-form event category.                                                                            
	EventType                                                                               string          `json:"event_type"`
	Gateway                                                                                 *AuditGateway   `json:"gateway,omitempty"`
	IntegrityCheck                                                                          *AuditIntegrity `json:"integrity_check,omitempty"`
	Message                                                                                 *string         `json:"message,omitempty"`
	// Plan-token binds artifacts to subsequent take-off.                                                   
	// Extended with version and governance provenance for safe upgrades and auditability.                  
	PlanToken                                                                               *PlanToken      `json:"plan_token,omitempty"`
	// Policy evaluation audit record.                                                                      
	// Extended to support chain-of-custody reconstruction.                                                 
	Policy                                                                                  *AuditPolicy    `json:"policy,omitempty"`
	Severity                                                                                *Severity       `json:"severity,omitempty"`
	// Cryptographic signature of this event hash.                                                          
	Signature                                                                               *string         `json:"signature,omitempty"`
	// Reference to the key used for signing (e.g. 'engine-key-1', 'orchestrator-key-prod').                
	SignatureKeyRef                                                                         *string         `json:"signature_key_ref,omitempty"`
	// RFC3339 timestamp of when the event occurred.                                                        
	Timestamp                                                                               time.Time       `json:"timestamp"`
	Workflow                                                                                *AuditWorkflow  `json:"workflow,omitempty"`
	// Workflow state when this event was emitted.                                                          
	// REQUIRED for temporal chain-of-custody reconstruction.                                               
	WorkflowState                                                                           string          `json:"workflow_state"`
}

type AuditGateway struct {
	GatewayType    *string   `json:"gateway_type,omitempty"`
	Model          *string   `json:"model,omitempty"`
	PolicyDecision *Decision `json:"policy_decision,omitempty"`
	RequestID      *string   `json:"request_id,omitempty"`
	Tool           *string   `json:"tool,omitempty"`
}

type AuditIntegrity struct {
	ActualPlanToken   *string  `json:"actual_plan_token,omitempty"`
	ArtifactsMatch    *bool    `json:"artifacts_match,omitempty"`
	Differences       []string `json:"differences,omitempty"`
	ExpectedPlanToken *string  `json:"expected_plan_token,omitempty"`
	PlanTokenMatch    *bool    `json:"plan_token_match,omitempty"`
}

// Plan-token binds artifacts to subsequent take-off.
// Extended with version and governance provenance for safe upgrades and auditability.
type PlanToken struct {
	// Per-artifact hashes that contributed to this plan token.                                        
	Artifacts                                                                       []PlanArtifactHash `json:"artifacts"`
	// Timestamp when the plan was created (RFC3339).                                                  
	CreatedAt                                                                       time.Time          `json:"created_at"`
	// Engine identity that produced this plan.                                                        
	EngineID                                                                        string             `json:"engine_id"`
	// SHA256 hash of governance context (OPA policies, ONNX models, gateway rules).                   
	// OPTIONAL but recommended for compliance verification.                                           
	// Enables auditors to verify governance configuration at plan-time.                               
	GovernanceHash                                                                  *string            `json:"governance_hash,omitempty"`
	// AI Model identifier used to generate this plan (e.g. 'gpt-4', 'claude-3').                      
	// Required for provenance.                                                                        
	Model                                                                           string             `json:"model"`
	// SHA256 digest of all policy configurations evaluated during flight-plan.                        
	// OPTIONAL but recommended for governance provenance.                                             
	// Proves which policy set was active when plan-token was created.                                 
	PolicyDigest                                                                    *string            `json:"policy_digest,omitempty"`
	// Engine protocol version used when this plan was produced.                                       
	ProtocolVersion                                                                 string             `json:"protocol_version"`
	// Primary plan token identifier, e.g. SHA256 over all plan artifacts + context.                   
	Token                                                                           string             `json:"token"`
	// Plan-token format version.                                                                      
	// REQUIRED for forward-compatibility handshake in mixed-version deployments.                      
	// Format: "1", "2", etc. (semantic versioning for plan-token structure)                           
	Version                                                                         string             `json:"version"`
	// Hash of the workspace state when the plan was created.                                          
	WorkspaceHash                                                                   string             `json:"workspace_hash"`
}

type PlanArtifactHash struct {
	Hash string   `json:"hash"`
	Name string   `json:"name"`
	Size *float64 `json:"size,omitempty"`
}

// Policy evaluation audit record.
// Extended to support chain-of-custody reconstruction.
type AuditPolicy struct {
	// Aggregation method used to combine individual policy decisions.                                 
	// REQUIRED if multiple policies were evaluated.                                                   
	// Ensures deterministic aggregation across orchestrators.                                         
	AggregationMethod                                                               *AggregationMethod `json:"aggregation_method,omitempty"`
	// Final aggregated decision after all policy evaluations.                                         
	// REQUIRED for chain-of-custody.                                                                  
	Decision                                                                        Decision           `json:"decision"`
	// Legacy field for backward compatibility.                                                        
	Engine                                                                          *string            `json:"engine,omitempty"`
	// Individual policy evaluation results.                                                           
	// Captures which specific policies (OPA/ONNX/gateway) produced which decisions.                   
	PolicyEvaluations                                                               []PolicyEvaluation `json:"policy_evaluations,omitempty"`
	// Policy violations detected.                                                                     
	Violations                                                                      []string           `json:"violations,omitempty"`
	// Policy warnings (non-blocking).                                                                 
	Warnings                                                                        []string           `json:"warnings,omitempty"`
	// Workflow state when this policy evaluation occurred.                                            
	// REQUIRED for temporal chain-of-custody.                                                         
	WorkflowState                                                                   string             `json:"workflow_state"`
}

// Individual policy evaluation result.
// Captures decision source and evidence.
type PolicyEvaluation struct {
	// Decision from this specific policy.                                                         
	Decision                                                                Decision               `json:"decision"`
	// Evaluation timestamp.                                                                       
	EvaluatedAt                                                             time.Time              `json:"evaluated_at"`
	// Evidence supporting this decision (e.g., rule matches, model scores).                       
	Evidence                                                                map[string]interface{} `json:"evidence,omitempty"`
	// Policy identifier (e.g., OPA policy name, ONNX model name).                                 
	PolicyID                                                                string                 `json:"policy_id"`
	// Reason for this decision.                                                                   
	Reason                                                                  *string                `json:"reason,omitempty"`
	// Decision severity for aggregation ordering.                                                 
	// 0=allow, 1=warn, 2=require_approval, 3=deny                                                 
	// REQUIRED for deterministic "most restrictive" aggregation.                                  
	Severity                                                                float64                `json:"severity"`
	// Policy source type.                                                                         
	Source                                                                  Source                 `json:"source"`
}

type AuditWorkflow struct {
	Mode       *string `json:"mode,omitempty"`
	StepID     *string `json:"step_id,omitempty"`
	WorkflowID *string `json:"workflow_id,omitempty"`
}

type EngineArtifact struct {
	Hash string   `json:"hash"`
	Name string   `json:"name"`
	Path string   `json:"path"`
	Role string   `json:"role"`
	Size *float64 `json:"size,omitempty"`
}

// Input delivered via STDIN or CABINCREW_INPUT_FILE.
// Defined in schemas/draft/engine.schema.json
type EngineInput struct {
	AllowedSecrets                                                []string               `json:"allowed_secrets,omitempty"`
	Config                                                        map[string]interface{} `json:"config,omitempty"`
	Context                                                       map[string]interface{} `json:"context,omitempty"`
	ExpectedPlanToken                                             *string                `json:"expected_plan_token,omitempty"`
	// Ephemeral identity token (e.g. OIDC, JWT) for the workload.                       
	// Preferred over static secrets.                                                    
	IdentityToken                                                 *string                `json:"identity_token,omitempty"`
	Meta                                                          EngineMeta             `json:"meta"`
	// Execution mode: 'flight-plan' or 'take-off'.                                      
	Mode                                                          Mode                   `json:"mode"`
	Orchestrator                                                  *EngineOrchestrator    `json:"orchestrator,omitempty"`
	ProtocolVersion                                               string                 `json:"protocol_version"`
	Secrets                                                       map[string]interface{} `json:"secrets,omitempty"`
}

type EngineMeta struct {
	StepID     string `json:"step_id"`
	WorkflowID string `json:"workflow_id"`
}

type EngineOrchestrator struct {
	ArtifactsSalt                                *string `json:"artifacts_salt,omitempty"`
	// Orchestrator run index for this execution.        
	RunIndex                                     *int64  `json:"run_index,omitempty"`
	WorkspaceHash                                *string `json:"workspace_hash,omitempty"`
}

type EngineMetric struct {
	Name  string                 `json:"name"`
	Tags  map[string]interface{} `json:"tags,omitempty"`
	Value float64                `json:"value"`
}

// Output delivered via STDOUT or CABINCREW_OUTPUT_FILE.
// Defined in schemas/draft/engine.schema.json
type EngineOutput struct {
	Artifacts                                         []EngineArtifact `json:"artifacts,omitempty"`
	Diagnostics                                       interface{}      `json:"diagnostics"`
	EngineID                                          string           `json:"engine_id"`
	Error                                             *string          `json:"error,omitempty"`
	Metrics                                           []EngineMetric   `json:"metrics,omitempty"`
	Mode                                              Mode             `json:"mode"`
	// SHA256 hash referencing a plan-token.json file.                 
	PlanToken                                         *string          `json:"plan_token,omitempty"`
	ProtocolVersion                                   string           `json:"protocol_version"`
	ReceiptID                                         string           `json:"receipt_id"`
	// Execution status: 'success' or 'failure'.                       
	Status                                            Status           `json:"status"`
	Warnings                                          []string         `json:"warnings,omitempty"`
}

type GatewayApproval struct {
	ApprovalID   *string `json:"approval_id,omitempty"`
	Reason       *string `json:"reason,omitempty"`
	RequiredRole *string `json:"required_role,omitempty"`
}

type LLMGatewayPolicyConfig struct {
	ModelRouting map[string]interface{} `json:"model_routing,omitempty"`
	OnnxModels   []string               `json:"onnx_models,omitempty"`
	OpaPolicies  []string               `json:"opa_policies,omitempty"`
	Rules        []LLMGatewayRule       `json:"rules,omitempty"`
}

type LLMGatewayRule struct {
	Action   string                 `json:"action"`
	Match    map[string]interface{} `json:"match"`
	Metadata map[string]interface{} `json:"metadata,omitempty"`
}

type LLMGatewayRequest struct {
	Context   map[string]interface{} `json:"context,omitempty"`
	Input     map[string]interface{} `json:"input"`
	Model     string                 `json:"model"`
	Provider  *string                `json:"provider,omitempty"`
	RequestID string                 `json:"request_id"`
	Source    *string                `json:"source,omitempty"`
	Timestamp time.Time              `json:"timestamp"`
}

type LLMGatewayResponse struct {
	Approval       *GatewayApproval       `json:"approval,omitempty"`
	Decision       Decision               `json:"decision"`
	GatewayPayload map[string]interface{} `json:"gateway_payload,omitempty"`
	RequestID      string                 `json:"request_id"`
	RewrittenInput map[string]interface{} `json:"rewritten_input,omitempty"`
	RoutedModel    *string                `json:"routed_model,omitempty"`
	Timestamp      time.Time              `json:"timestamp"`
	Violations     []string               `json:"violations,omitempty"`
	Warnings       []string               `json:"warnings,omitempty"`
}

type MCPGatewayPolicyConfig struct {
	OnnxModels  []string         `json:"onnx_models,omitempty"`
	OpaPolicies []string         `json:"opa_policies,omitempty"`
	Rules       []MCPGatewayRule `json:"rules,omitempty"`
}

type MCPGatewayRule struct {
	Action   string                 `json:"action"`
	Match    map[string]interface{} `json:"match"`
	Metadata map[string]interface{} `json:"metadata,omitempty"`
}

type MCPGatewayRequest struct {
	Context   map[string]interface{} `json:"context,omitempty"`
	Method    string                 `json:"method"`
	Params    map[string]interface{} `json:"params,omitempty"`
	RequestID string                 `json:"request_id"`
	ServerID  string                 `json:"server_id"`
	Source    *string                `json:"source,omitempty"`
	Timestamp time.Time              `json:"timestamp"`
}

type MCPGatewayResponse struct {
	Approval         *GatewayApproval       `json:"approval,omitempty"`
	Decision         Decision               `json:"decision"`
	RequestID        string                 `json:"request_id"`
	RewrittenRequest map[string]interface{} `json:"rewritten_request,omitempty"`
	Timestamp        time.Time              `json:"timestamp"`
	Violations       []string               `json:"violations,omitempty"`
	Warnings         []string               `json:"warnings,omitempty"`
}

type PolicyEvaluatedData struct {
	Decision     Decision `json:"decision"`
	EvaluationID string   `json:"evaluation_id"`
	PolicyName   string   `json:"policy_name"`
}

// Durable policy evaluation record.
// Tracks policy decisions with evidence for audit trail.
type PolicyEvaluationRecord struct {
	Decision       Decision  `json:"decision"`
	EvaluatedAt    time.Time `json:"evaluated_at"`
	EvaluationID   string    `json:"evaluation_id"`
	EvidenceHashes []string  `json:"evidence_hashes,omitempty"`
	PolicyName     string    `json:"policy_name"`
	Reason         *string   `json:"reason,omitempty"`
	StepID         string    `json:"step_id"`
}

type PreflightInput struct {
	Context                                                                               map[string]interface{} `json:"context,omitempty"`
	EngineOutput                                                                          map[string]interface{} `json:"engine_output"`
	Evidence                                                                              []PreflightEvidence    `json:"evidence,omitempty"`
	Mode                                                                                  Mode                   `json:"mode"`
	// Plan-token binds artifacts to subsequent take-off.                                                        
	// Extended with version and governance provenance for safe upgrades and auditability.                       
	PlanToken                                                                             *PlanToken             `json:"plan_token,omitempty"`
	StepID                                                                                string                 `json:"step_id"`
	WorkflowID                                                                            string                 `json:"workflow_id"`
}

type PreflightOutput struct {
	Decision   Decision           `json:"decision"`
	Requires   *PreflightRequires `json:"requires,omitempty"`
	Violations []string           `json:"violations,omitempty"`
	Warnings   []string           `json:"warnings,omitempty"`
}

type PreflightRequires struct {
	Reason *string `json:"reason,omitempty"`
	Role   *string `json:"role,omitempty"`
}

type StepCompletedData struct {
	Artifacts []string `json:"artifacts,omitempty"`
	StepID    string   `json:"step_id"`
}

type StepStartedData struct {
	StepID   string `json:"step_id"`
	StepType string `json:"step_type"`
}

// Write-Ahead Log entry for deterministic replay.
// Enables crash recovery and multi-orchestrator consistency.
type WALEntry struct {
	Checksum                     string       `json:"checksum"`
	Data                         WALEntryData `json:"data"`
	EntryType                    WALEntryType `json:"entry_type"`
	// Monotonic sequence number.             
	Sequence                     int64        `json:"sequence"`
	Timestamp                    time.Time    `json:"timestamp"`
	WorkflowID                   string       `json:"workflow_id"`
}

type WALEntryData struct {
	InitialState  *State    `json:"initial_state,omitempty"`
	PlanTokenHash *string   `json:"plan_token_hash,omitempty"`
	StepID        *string   `json:"step_id,omitempty"`
	StepType      *string   `json:"step_type,omitempty"`
	Artifacts     []string  `json:"artifacts,omitempty"`
	ApprovalID    *string   `json:"approval_id,omitempty"`
	RequiredRole  *string   `json:"required_role,omitempty"`
	Approved      *bool     `json:"approved,omitempty"`
	Approver      *string   `json:"approver,omitempty"`
	ArtifactHash  *string   `json:"artifact_hash,omitempty"`
	ArtifactID    *string   `json:"artifact_id,omitempty"`
	ArtifactType  *string   `json:"artifact_type,omitempty"`
	Decision      *Decision `json:"decision,omitempty"`
	EvaluationID  *string   `json:"evaluation_id,omitempty"`
	PolicyName    *string   `json:"policy_name,omitempty"`
	FinalState    *State    `json:"final_state,omitempty"`
	Error         *string   `json:"error,omitempty"`
	FailedStep    *string   `json:"failed_step,omitempty"`
}

type WorkflowCompletedData struct {
	Artifacts  []string `json:"artifacts"`
	FinalState State    `json:"final_state"`
}

type WorkflowFailedData struct {
	Error      string  `json:"error"`
	FailedStep *string `json:"failed_step,omitempty"`
}

type WorkflowStartedData struct {
	InitialState  State  `json:"initial_state"`
	PlanTokenHash string `json:"plan_token_hash"`
}

type WorkflowState struct {
	LastDecision  *Decision `json:"last_decision,omitempty"`
	PlanTokenHash *string   `json:"plan_token_hash,omitempty"`
	State         State     `json:"state"`
	StepID        *string   `json:"step_id,omitempty"`
	WorkflowID    *string   `json:"workflow_id,omitempty"`
}

// Durable workflow state record for restart-safety.
// Contains all information needed to deterministically resume workflow execution.
type WorkflowStateRecord struct {
	Approvals         []ApprovalRecord         `json:"approvals"`
	Artifacts         []ArtifactRecord         `json:"artifacts"`
	CreatedAt         time.Time                `json:"created_at"`
	CurrentState      State                    `json:"current_state"`
	Metadata          map[string]interface{}   `json:"metadata,omitempty"`
	PlanTokenHash     string                   `json:"plan_token_hash"`
	PolicyEvaluations []PolicyEvaluationRecord `json:"policy_evaluations"`
	StepsCompleted    []string                 `json:"steps_completed"`
	StepsPending      []string                 `json:"steps_pending"`
	UpdatedAt         time.Time                `json:"updated_at"`
	WorkflowID        string                   `json:"workflow_id"`
}

// Policy aggregation strategy.
// Defines how multiple policy decisions are combined into a final decision.
//
// Aggregation method used to combine individual policy decisions.
// REQUIRED if multiple policies were evaluated.
// Ensures deterministic aggregation across orchestrators.
type AggregationMethod string

const (
	AggregationMethodCustom AggregationMethod = "custom"
	AllAllow                AggregationMethod = "all_allow"
	AnyDeny                 AggregationMethod = "any_deny"
	Majority                AggregationMethod = "majority"
	MostRestrictive         AggregationMethod = "most_restrictive"
	Unanimous               AggregationMethod = "unanimous"
)

// Final aggregated decision after all policy evaluations.
// REQUIRED for chain-of-custody.
//
// Decision from this specific policy.
type Decision string

const (
	Allow           Decision = "allow"
	Deny            Decision = "deny"
	RequireApproval Decision = "require_approval"
	Warn            Decision = "warn"
)

// Policy source type.
type Source string

const (
	LlmGateway   Source = "llm_gateway"
	MCPGateway   Source = "mcp_gateway"
	Onnx         Source = "onnx"
	Opa          Source = "opa"
	SourceCustom Source = "custom"
)

type Severity string

const (
	Critical Severity = "critical"
	Debug    Severity = "debug"
	Error    Severity = "error"
	Info     Severity = "info"
	Warning  Severity = "warning"
)

// Execution mode: 'flight-plan' or 'take-off'.
type Mode string

const (
	FlightPlan Mode = "flight-plan"
	TakeOff    Mode = "take-off"
)

// Execution status: 'success' or 'failure'.
type Status string

const (
	Failure Status = "failure"
	Success Status = "success"
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

type WALEntryType string

const (
	ApprovalReceived  WALEntryType = "approval_received"
	ApprovalRequested WALEntryType = "approval_requested"
	ArtifactCreated   WALEntryType = "artifact_created"
	PolicyEvaluated   WALEntryType = "policy_evaluated"
	StepCompleted     WALEntryType = "step_completed"
	StepStarted       WALEntryType = "step_started"
	WorkflowCompleted WALEntryType = "workflow_completed"
	WorkflowFailed    WALEntryType = "workflow_failed"
	WorkflowStarted   WALEntryType = "workflow_started"
)

// Inline content for small artifacts.
// Can be string, object, array, or null.
type Body struct {
	AnythingArray []interface{}
	AnythingMap   map[string]interface{}
	String        *string
}
