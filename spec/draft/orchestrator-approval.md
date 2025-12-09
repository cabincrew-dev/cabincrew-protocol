# CabinCrew Orchestrator Approval Specification
Version: draft

This document defines the normative behavior of the human‑in‑the‑loop approval system within the CabinCrew Protocol. Approval is a critical governance mechanism that ensures high‑risk changes are reviewed by authorized humans before take-off is allowed.

Approval is part of the Orchestrator’s state machine and integrates with Preflight, Gateways, and the Audit subsystem.

## 1. Purpose of Approval

The approval mechanism ensures that automated intent does not translate into action without explicit human authorization when policies or ML models detect risk.

Approval guarantees:
- human oversight
- traceability of decisions
- prevention of unsafe automation
- compliance with organizational requirements
- binding authorization to a specific plan-token

No take-off may occur if approval is required but not granted.

---

## 2. When Approval Is Required

Approval is triggered when:
- OPA policies return require_approval  
- ONNX model evaluation returns require_approval  
- Gateway evaluation for MCP or LLM requests returns require_approval  
- Workflow-specific rules demand human verification (e.g., production deploys)  

The Orchestrator must aggregate all signals and decide whether approval is mandatory.

---

## 3. ApprovalRequest Structure

When approval is required, the Orchestrator generates an ApprovalRequest containing:

- unique approval_id  
- workflow_id and step_id  
- plan-token hash  
- summary of artifacts  
- triggered policy names  
- human-readable explanation for escalation  
- timestamp  
- requester identity (engine/orchestrator/user)  

ApprovalRequests must be written to durable storage or transmitted to an external approval system.

---

## 4. ApprovalResponse Structure

A human reviewer provides an ApprovalResponse:

- approval_id  
- approved (true/false)  
- approver identity  
- approver role  
- optional comments  
- timestamp  

ApprovalResponse must reference the same approval_id.

The Orchestrator must verify that:
- approval_id matches  
- the response corresponds to the latest plan-token  
- the approver role satisfies governance rules  

If verification fails → deny take-off.

---

## 5. Binding Approval to Plan-Token

Approval MUST be bound to the plan-token produced during flight-plan.

This prevents:
- stale approval reuse  
- approval replay attacks  
- approvals for modified artifacts  

Binding rules:
- approval must include the exact plan-token hash  
- orchestrator must recompute artifact hashes  
- mismatch → workflow denied  

---

## 6. State Machine Behavior

The approval process defines the following states:

1. **preflight_requires_approval**  
   The orchestrator halts workflow and emits an ApprovalRequest.

2. **waiting_for_approval**  
   The workflow remains paused until an ApprovalResponse is received.

3. **approved**  
   The orchestrator resumes workflow at the take-off stage.

4. **rejected**  
   Workflow stops with failure.

5. **expired (optional)**  
   If configured, approvals may time out.

The orchestrator must persist enough state to resume after restarts.

---

## 7. Interaction with Gateways

Gateways may independently require approval.

Examples:
- MCP Gateway detecting dangerous write operations  
- LLM Gateway classifying a generated command as high-risk  

The orchestrator must treat gateway-level approval requirements identically to preflight approvals.

All gateway approval events must be stored in audit logs.

---

## 8. Audit Requirements

Both ApprovalRequest and ApprovalResponse must generate audit events containing:

- event_id  
- workflow and step identifiers  
- approval_id  
- triggered rules  
- approver identity  
- authorization result  
- reason for escalation  
- timestamps  

These events provide the chain of custody for governance.

---

## 9. Restart and Recovery

The orchestrator must support restart-safe behavior:

- If approval was requested but no response was received → remain in waiting state.  
- If approved → resume take-off.  
- If rejected → fail workflow.  
- If plan-token mismatches after restart → fail workflow.  

State must never be ambiguous.

---

## 10. Error Conditions

Approval must fail when:

- approval_id does not exist  
- approval_id does not match request  
- plan-token mismatch  
- approval expired (if configured)  
- approver lacks required role  
- approvalResponse malformed  
- external approval system unreachable (depending on policy)  

Failures must generate audit events.

---

## 11. Summary

The approval system ensures that human judgment is included in AI-assisted automation whenever risk is detected. By binding approval to plan-token integrity, enforcing strict verification, and capturing all events through the audit subsystem, CabinCrew maintains a safe, transparent, and compliant workflow model.

