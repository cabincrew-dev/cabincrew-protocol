# CabinCrew Human Approval Model
Version: draft

This document defines the **human approval subsystem** of the CabinCrew Protocol.  
Approvals are a core part of governance, allowing humans to intervene before potentially risky or unsafe AI-driven automation proceeds.

Approvals are *first-class protocol entities*, not an optional feature.

---

# 1. Purpose of Human Approval

Human approval ensures that **high-risk** or **ambiguous** operations cannot be executed automatically.

Approvals are required when:

- OPA rules return `require_approval`
- ONNX models classify high-risk content
- Patch or file diffs exceed safety thresholds
- LLM outputs are unsafe or sensitive
- Policies mandate oversight (e.g., “production changes require approval”)

Approvals serve as the last gate before take-off.

---

# 2. Approval Lifecycle (High-Level)

A full approval cycle includes:

```
Preflight → Governance Decision → Approval Requested → Human Review → ApprovalResponse → Take-Off
```

If the human denies or modifies the approval → workflow FAILS.

Approval state must be **persistent**, **tamper-proof**, and **bound to the plan-token**.

---

# 3. ApprovalRequest Structure

ApprovalRequest includes:

- workflow_id  
- step_id  
- plan_token  
- artifact metadata  
- diffs or rendered changes  
- OPA rule explanations  
- ONNX classifier outputs  
- risk summary  
- timestamps  
- requester identity  
- optional notes or labels  

This request is delivered to a human reviewer via:

- UI  
- API  
- CLI  
- messaging bot integration  

---

# 4. ApprovalResponse Structure

A human must respond with:

- approval_id  
- workflow_id  
- plan_token (must match exactly)  
- decision: approve | reject  
- reviewer identity  
- timestamp  
- optional comment  

Plan-token binding ensures:

- no replaying approvals from older plan  
- no modifying artifacts after review  
- no approval reuse across workflows  

If tokens mismatch → orchestrator denies automatically.

---

# 5. Binding Approvals to Plan-Token

The plan-token includes:

- artifact metadata canonical hash  
- deterministic artifact ordering  
- digest of contextual metadata  
- normalized configuration state  

The ApprovalResponse must include the same plan-token hash.

Workflow continues ONLY IF:

```
response.plan_token == orchestrator.plan_token
```

Otherwise → **FAILED**.

This prevents:
- malicious alteration of artifacts after review  
- LLM/agent attempts to modify plan post-approval  
- inconsistent review states  

---

# 6. Approval States

Approval introduces the following workflow stages:

| State | Description |
|-------|-------------|
| `AWAITING_APPROVAL` | Preflight requires human review |
| `APPROVAL_PENDING` | Request issued, waiting for human |
| `APPROVED` | Human explicitly approved |
| `REJECTED` | Human denied |
| `INVALID` | Token mismatch or malformed response |
| `TIMED_OUT` | No human responded within policy window |

Orchestrator must persist all state transitions.

---

# 7. Approval Sources (Implementer Options)

Approvals may be obtained via:

- Web UI  
- CLI (`cabincrew approve …`)  
- Slack/Teams bot  
- Email link  
- GitHub/GitLab workflow comments  
- Internal enterprise approval systems  

The protocol does not mandate *how* approvals are collected—only how they must be formatted and validated.

---

# 8. What a Human Reviewer Sees

Reviewers must be provided with:

### **Artifact Overview**
- file diffs  
- patch summaries  
- Kubernetes manifests  
- Terraform plan summaries  
- LLM-proposed text/code changes  

### **Governance Signals**
- OPA rule that triggered approval  
- ONNX risk classifiers  
- metrics  

### **Context**
- workflow_id  
- step_id  
- user/agent identity  
- “why you are seeing this approval” explanation  

This ensures transparency.

---

# 9. Approval Decision Logic

Human may choose:

### ✔ Approve
Workflow resumes → orchestrator validates → take-off begins.

### ✖ Reject
Workflow halts → orchestrator marks as FAILED → emits audit event.

### ⚠ Ignore (timeout)
Configured by enterprise policy.

In most enterprise environments, timeout = reject.

---

# 10. Authorization Requirements

Approval systems must enforce:

- reviewer authentication  
- role-based access (RBAC)  
- optional 2FA  
- audit trails  

Recommended reviewer roles:

- Developer  
- Infra Admin  
- Security Engineer  
- Compliance Officer  
- Release Manager  

---

# 11. Audit Requirements

Every approval must generate audit logs including:

- approval metadata  
- risk summary  
- OPA/ONNX signals  
- reviewer identity  
- timestamps  
- final decision  
- plan-token hash  
- workflow context  

Audits must be immutable.

---

# 12. Failure Modes

The orchestrator MUST treat approvals as invalid when:

- plan-token mismatch  
- missing fields  
- malformed structure  
- expired approval state  
- revoked workflow state  
- reviewer unauthorized  
- reused approval decision  

These are protocol violations and end the workflow.

---

# 13. Example Approval Flow (Simplified)

```
Engine (flight-plan)
        ↓
Artifacts created
        ↓
Preflight governance → require_approval
        ↓
ApprovalRequest created
        ↓
Human reviews changes
        ↓
Human approves (ApprovalResponse)
        ↓
Orchestrator validates plan-token
        ↓
Engine (take-off)
        ↓
Execution complete
```

---

# 14. Summary

The CabinCrew approval model ensures:

- humans remain in control of high-risk automation  
- no unsafe action can execute without explicit review  
- all approvals are tied to immutable plan-token state  
- approval flows survive restarts and system failures  
- every step is fully auditable  

Approvals are a cornerstone of CabinCrew’s **governance-first** approach, enabling safe automation in high-stakes enterprise environments.

