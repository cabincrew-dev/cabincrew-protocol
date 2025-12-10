# CabinCrew Audit Event Specification
Version: draft

The audit subsystem provides a complete, immutable, and structured record of all meaningful actions taken by the Orchestrator, Engines, Gateways, and human approvers. Audit events establish chain-of-custody guarantees, enable forensic analysis, support compliance requirements, and ensure full transparency in automated workflows.

This document defines the required semantics of audit events.

## 1. Purpose of the Audit System

The audit system ensures:

- **Traceability**: every action is recorded.
- **Determinism**: events reflect the true state transitions.
- **Integrity**: events cannot be forged or modified without detection.
- **Reproducibility**: workflows can be reconstructed from audit logs.
- **Compliance**: organizations can review and prove safe operation.
- **Governance**: policy decisions, approvals, and rejections are logged.

All components must generate audit events for their respective responsibilities.

---

## 2. What Must Generate an Audit Event

Audit events are required for:

### **2.1 Orchestrator Actions**
- engine launch
- engine completion
- environment preparation
- artifact validation results
- plan-token creation
- plan-token verification
- workflow state transitions
- workflow completion or failure

### **2.2 Preflight Evaluation**
- OPA policy evaluations
- ONNX model evaluations
- aggregated decisions (allow/warn/deny/require_approval)
- preflight failures

### **2.3 Approval Workflow**
- ApprovalRequest creation
- ApprovalResponse result
- approval binding to plan-token
- approval rejection
- approval mismatch

### **2.4 MCP Gateway**
- request interception
- OPA + ONNX evaluation results
- aggregated decision
- forwarded requests and responses
- denied or blocked requests

### **2.5 LLM Gateway**
- original and rewritten prompts
- selected model routing
- OPA + ONNX evaluations
- aggregated decision
- unsafe or high-risk output detection
- approval-triggered responses

### **2.6 Errors & System Events**
- invalid artifacts
- malformed requests
- IO or permission failures
- model or policy loader failures
- unhandled exceptions

If in doubt, an event should be logged.

---

## 3. Audit Event Structure

Audit events must conform to audit-event.schema.json.

Fields include:

- **event_id**  
  Unique identifier for the event.

- **timestamp**  
  ISO 8601 timestamp for event occurrence.

- **source**  
  Component that generated the event:  
  `orchestrator`, `engine`, `mcp_gateway`, `llm_gateway`, `approval_system`.

- **workflow_id / step_id**  
  Identifiers for workflow correlation.

- **event_type**  
  Examples:  
  `engine_start`, `engine_complete`, `policy_result`,  
  `approval_request`, `approval_response`,  
  `mcp_request`, `mcp_decision`,  
  `llm_request`, `llm_decision`,  
  `workflow_failure`, `workflow_complete`.

- **payload**  
  Structured data specific to each event type.

- **decision** (optional)  
  allow, warn, deny, require_approval

- **artifacts** (optional)  
  Artifact metadata and hashes involved in the event.

- **plan_token** (optional)  
  Token hash for chain-of-custody verification.

- **approval_id** (optional)  
  Bound to approval requests and responses.

- **workflow_state** (optional)  
  Workflow state when this event was emitted.  
  Required for temporal chain-of-custody reconstruction.

- **policy_evaluations** (in policy field)  
  Array of individual policy evaluation results.  
  Each includes:
  - **source**: Policy source type (opa, onnx, llm_gateway, mcp_gateway, custom)
  - **policy_id**: Policy identifier (e.g., OPA policy name, ONNX model name)
  - **decision**: Decision from this specific policy (allow, warn, require_approval, deny)
  - **reason**: Reason for this decision
  - **evidence**: Supporting data (e.g., rule matches, model scores)
  - **evaluated_at**: ISO 8601 timestamp

- **aggregation_method** (in policy field)  
  Method used to combine individual policy decisions.  
  Examples: most_restrictive, unanimous, majority

---

## 4. Immutability Requirements

Audit events must be:

- append-only
- never altered after writing
- cryptographically verifiable (optional but recommended)
- stored in sequential order or with retrievable sequence numbers

Vendors may implement:
- tamper-evident logs
- hashing chains
- signed logs
- write-once storage

---

## 5. Ordering Guarantees

Audit logs must preserve:

1. **Engine lifecycle ordering**  
2. **Policy evaluation ordering**  
3. **Approval workflow ordering**  
4. **Gateway request/response ordering**  
5. **Workflow step ordering**

Events may be concurrent but must be timestamped and traceable.

---

## 6. Secret-Handling Rules

Audit payloads must not contain:

- plaintext secrets  
- tokens or credentials  
- private keys  
- unredacted sensitive content  

If a gateway detects secrets in a request or response, logging must redact them.

---

## 7. Restart and Resumption Behavior

On restart:

- the Orchestrator must append new events; never overwrite  
- pending approvals must resume in paused state  
- partial events must be recorded as failures or incomplete entries  
- no workflow may continue without reconstructing prior audit state  

Audit logs must support recovery and replay.

---

## 8. Retention, Rotation, and Export (Vendor Defined)

The protocol does not define retention defaults.  
Vendors may implement:

- log rotation  
- archival  
- compression  
- external export (e.g., SIEM, S3, Splunk)  
- time-based or size-based retention  

Retention policies must not compromise required auditability.

---

## 9. Prohibited Behaviors

The system must not:

- delete audit events silently  
- modify existing audit entries  
- skip events for performance reasons  
- suppress warnings or errors  
- bypass audit generation during gateway failures  
- emit unstructured free-form logs in place of audit events  

All omissions or failures must be recorded as audit events themselves.

---

## 10. Summary

The audit subsystem is a foundational part of the CabinCrew Protocol, providing governance, traceability, and safety through structured, immutable event streams. By recording every meaningful interaction across orchestrator, engines, gateways, and approvals, the system enables transparent and compliant automation in high-risk environments.

