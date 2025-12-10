# CabinCrew Workflow Lifecycle
Version: draft

This document provides a detailed, implementer-friendly description of the **full workflow lifecycle** in the CabinCrew Protocol. It explains how the Orchestrator, Engines, Gateways, Policies, and Humans interact from the moment a workflow is triggered until it completes or fails.  

This document is non-normative and supplements the formal specs in `spec/draft/`.

---

# 1. High-Level Overview

A CabinCrew workflow consists of two primary execution phases:

1. **flight-plan** — compute intent with zero side effects  
2. **take-off** — apply validated and approved intent  

Surrounding these phases are governance steps, approvals, and audit logging.

---

# 2. Workflow Trigger

A workflow may be triggered by:

- a user request  
- an agent or tool invocation  
- a scheduled operation  
- CI/CD or repo events  
- an external system  

Upon start, the Orchestrator:

1. Creates workflow_id and step_id  
2. Prepares working directories  
3. Loads configuration  
4. Emits an audit event  

The workflow is now in state **INIT**.

---

# 3. Running the Engine in Flight-Plan Mode

## 3.1 Directory Setup
The Orchestrator prepares:

- `CABINCREW_WORKSPACE`  
- `CABINCREW_ARTIFACTS_DIR` (empty)  
- `CABINCREW_TEMP_DIR`  

## 3.2 Engine Invocation
The Orchestrator launches the Engine with:

```
--mode flight-plan
```

Input is passed via STDIN.

## 3.3 Engine Responsibilities
The engine must:

- read workspace  
- compute intent  
- write artifacts to `CABINCREW_ARTIFACTS_DIR`  
- not modify the workspace  
- produce structured JSON receipt  

## 3.4 Post-Completion
The Orchestrator:

- parses receipt  
- audits engine completion  
- moves workflow to **PLAN_GENERATED**  

If errors occur → workflow enters **FAILED**.

---

# 4. Artifact Processing

The Orchestrator:

1. Scans artifact directories  
2. Validates artifact metadata  
3. Computes integrity hashes  
4. Produces deterministic artifact ordering  

Invalid artifacts → workflow **FAILED**.

If successful → workflow enters **ARTIFACTS_VALIDATED**.

---

# 5. Plan-Token Creation

The Orchestrator:

1. Computes composite plan hash  
2. Creates plan-token  
3. Stores it persistently  
4. Emits audit event  

Plan-token binds the workflow state and artifacts immutably.

Workflow enters **TOKEN_CREATED**.

---

# 6. Preflight Governance Phase

The Orchestrator now evaluates artifacts using:

- **OPA policies**  
- **ONNX models**  
- optional custom rule engines  

Evaluations occur for both:

- artifact metadata  
- artifact content (body.data)  

## 6.1 Decision Outcomes

### **deny**
Workflow stops → **FAILED**.

### **require_approval**
Workflow pauses → **AWAITING_APPROVAL**.

### **warn**
Continue, but audit warning.

### **allow**
Continue normally.

## 6.2 Audit Events
The Orchestrator logs:

- raw policy results  
- ONNX inferences  
- aggregated decision  

Workflow enters **PREFLIGHT_COMPLETE** (or **AWAITING_APPROVAL**).

---

# 7. Human Approval Workflow (Optional)

If preflight requires approval:

1. Orchestrator creates **ApprovalRequest**  
2. Human reviews artifacts & context  
3. Human responds with **ApprovalResponse**  
4. Orchestrator validates binding to plan-token  

If approval granted → workflow moves to **APPROVED**.  
If rejected → **FAILED**.

Approval state must survive restarts.

---

# 8. Prepare for Take-Off

Before take-off, the Orchestrator:

1. Recomputes artifact hashes  
2. Compares with plan-token  
3. Validates approval status (if required)  
4. Ensures workspace is writable  
5. Ensures gateways are active  

Mismatch → workflow **FAILED**.

Workflow enters **READY_FOR_TAKEOFF**.

---

# 9. Running the Engine in Take-Off Mode

The Orchestrator launches engine with:

```
--mode take-off
```

Engine receives:

- plan-token  
- input context  
- validated state artifacts  

Engine must:

- apply intended actions  
- produce receipt  
- record logs  

No new artifacts required, but allowed.

Upon completion:

- orchestrator reads receipt  
- audits event  
- transitions to **EXECUTION_COMPLETE**  

Engine failures → workflow **FAILED**.

---

# 10. Post-Execution Governance

After take-off:

- OPA may re-evaluate outputs  
- ONNX may evaluate logs, results  
- audit events must be written  
- warnings may be generated  

This phase acts as a second safety net.

---

# 11. Finalization & Cleanup

The Orchestrator:

1. Writes final audit event  
2. Stores workflow summary  
3. Cleans temp directories  
4. Retains artifacts (depending on retention policy)  

Workflow enters **COMPLETED**.

If errors occur → **FAILED**.

---

# 12. Workflow Lifecycle States Summary

| State | Description |
|-------|-------------|
| INIT | Workflow created |
| PLAN_GENERATED | Engine produced flight-plan artifacts |
| ARTIFACTS_VALIDATED | Artifacts verified, hashed |
| TOKEN_CREATED | Plan-token generated |
| PREFLIGHT_COMPLETE | Governance evaluation done |
| AWAITING_APPROVAL | Paused for human approval |
| APPROVED | Human approval granted |
| READY_FOR_TAKEOFF | All checks passed |
| EXECUTION_COMPLETE | Engine take-off finished |
| COMPLETED | Workflow completed successfully |
| FAILED | Workflow terminated due to error or denial |

---

# 13. Restart Safety Behavior

The Orchestrator must restore:

- workflow state  
- plan-token  
- artifacts metadata  
- approval status  
- audit offsets  

It must re-run:

- artifact integrity checks  
- governance checks (configurable)  

It must **not**:

- skip steps  
- rerun steps silently  
- regenerate artifacts  

If state mismatch occurs → abort.

---

# 14. End-to-End Example (Simplified)

```
User → "Update dependency"
        ↓
Engine (flight-plan)
        ↓
Artifacts (diff.json)
        ↓
Plan-token created
        ↓
OPA/ONNX preflight → require_approval
        ↓
Human approves
        ↓
Engine (take-off) applies diff
        ↓
Audit logs written
        ↓
Workflow complete
```

---

# 15. Summary

The CabinCrew Workflow Lifecycle ensures:

- deterministic state transitions  
- governance and safety before execution  
- auditability at every stage  
- stability across restarts  
- a strict separation of planning and execution  

This lifecycle is the backbone of safe, enterprise-grade AI automation.

