# Orchestrator Approval Flow Specification (Draft)

The **Approval Stage** is the human-in-the-loop checkpoint of the CabinCrew Protocol.
It is triggered when Pre-Flight returns:

```
REQUIRE_APPROVAL
```

The Orchestrator must pause execution, gather the necessary artifacts,
and request explicit human authorization before continuing to `take-off`.

Approval is a **governance and safety requirement**, not an execution step.


---

# 1. When Approval Is Required

Approval is required when:

- OPA rules set `require_approval = true`
- ONNX model scores exceed a configured threshold
- A rule detects a sensitive or high-impact operation
- A workflow step is marked as requiring manual review
- The organization’s policy mandates review (e.g., production deploys)

Approval MUST NOT be skipped unless explicitly disabled by configuration.


---

# 2. Approval Request Packet

When an approval is required, the Orchestrator constructs an `approval_request`
object and sends it to a human-facing approval system or UI.

### Structure

```json
{
  "approval_id": "string",
  "workflow_id": "string",
  "step_id": "string",

  "reason": "string",
  "required_role": "string",

  "engine_output": { ... },

  "evidence": [
    {
      "name": "string",
      "path": "string",
      "hash": "sha256"
    }
  ]
}
```

### Required Elements

- **approval_id**  
  Unique ID for correlating approval responses.

- **reason**  
  Textual explanation: why approval is needed.

- **required_role**  
  Security role required to authorize the action (e.g., `admin`, `security`, `lead`).

- **engine_output**  
  The full receipt of the engine execution.

- **evidence artifacts**  
  Only artifacts where `role = "evidence"`.

### Forbidden Elements

- Secrets  
- State artifacts  
- Log artifacts  
- Workspace content


---

# 3. Workflow State Transition

When an approval request is created, workflow state MUST transition to:

```
WAITING_APPROVAL
```

No further steps may execute until approval is resolved.


---

# 4. Approval Response Packet

A human (or human-facing system) sends an `approval_response`
back to the Orchestrator:

```json
{
  "approval_id": "string",
  "approved": true,
  "approver": "string",
  "reason": "string",
  "timestamp": "string"
}
```

### Rules

- `approved = true` → workflow resumes (`TAKEOFF_RUNNING`)
- `approved = false` → workflow fails (`FAILED`)
- `approver` should be the authenticated identity
- `timestamp` must reflect when decision was made

All approval responses MUST be logged as audit events.


---

# 5. Required Orchestrator Behavior

### 5.1 Pause Execution

Once approval is requested:

- All workflow execution MUST pause
- Engines MUST NOT run
- No gateway calls may be made

### 5.2 Store Evidence

Approval inputs must be durable:

- Evidence artifacts
- Engine output
- Reason for approval
- Policy evaluation results

These must be stored immutably.

### 5.3 Reject Invalid Responses

The Orchestrator MUST reject a response if:

- `approval_id` does not match
- timestamp is missing
- unauthorized role approves the action
- response is malformed

### 5.4 Log Audit Events

At minimum, the following MUST be logged:

- approval_request event
- approval_response event
- decision (approved/rejected)
- identity of approver
- reason


---

# 6. Approval Invariants

1. Only evidence artifacts may be shown to approvers.  
2. Approval must be explicit—no auto-approval is allowed.  
3. All approvals must be associated with a unique workflow/step.  
4. Approved steps may not revert to unapproved state.  
5. A rejected approval permanently fails the workflow.  
6. Approval decisions must not modify artifacts.  
7. Approvals must be reproducible from audit log context.  


---

# 7. Security Requirements

- Approval requests must go through an authenticated system.
- Approvers must meet the role requirements listed in the request.
- Evidence hashes must match their stored artifacts.
- Approval decisions must be immutable.
- All communication between Orchestrator and approval system must be secured.

The Orchestrator MUST NOT:

- expose secrets  
- expose logs  
- leak workspace content  
- include ONNX raw inputs in approval packets  


---

# 8. Compatibility Requirements

The Orchestrator embeds:

```
protocol_version = "2025-02-01-draft"
```

Approval systems MUST reject mismatched versions.

---

# End of Approval Specification (Draft)
