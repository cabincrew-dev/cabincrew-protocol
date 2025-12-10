# Orchestrator Implementer’s Guide
Version: draft

This guide explains how to build a fully compliant **CabinCrew Orchestrator**.  
It is a practical, developer-facing companion to the normative specifications in:

- `spec/draft/orchestrator.md`
- `spec/draft/orchestrator-preflight.md`
- `spec/draft/orchestrator-approval.md`
- `spec/draft/plan-token.md`
- `schema/draft/orchestrator.schema.json`

The Orchestrator is the **authoritative state machine** that ensures workflows execute safely, deterministically, and with complete governance.

---

## 1. What the Orchestrator Must Do

The Orchestrator is responsible for:

### **1.1 Workflow Coordination**
- Running Engines in `flight-plan` and `take-off` modes  
- Providing workspace and artifact directories  
- Passing structured inputs  
- Reading engine receipts  

### **1.2 Governance & Safety**
- Applying OPA policies  
- Running ONNX models  
- Making aggregated decisions  
- Handling human approvals  

### **1.3 Artifact Verification**
- Validating artifact structures  
- Computing integrity hashes  
- Creating and verifying plan-tokens  

### **1.4 Audit Logging**
- Recording all events  
- Ensuring immutability and order  

### **1.5 Restart-Safe Execution**
- Restoring workflow from stable checkpoints  

---

## 2. Core State Machine

The Orchestrator should follow this sequence:

1. **Prepare Environment**
2. **Run Engine: flight-plan**
3. **Collect Artifacts**
4. **Validate Artifacts**
5. **Compute Plan-Token**
6. **Run Preflight (OPA/ONNX)**
   - allow  
   - warn  
   - deny  
   - require_approval  
7. **(Optional) Pause for Approval**
8. **Launch Engine: take-off**
9. **Collect Results**
10. **Finalize Workflow**
11. **Emit Audit Events**

The state machine must survive restarts between any step.

---

## 3. Directory Contracts

Each workflow step receives:

### **CABINCREW_WORKSPACE**
- Must exist before engine launch.  
- Orchestrator must ensure isolation if multiple workflows run concurrently.

### **CABINCREW_ARTIFACTS_DIR**
- Must be empty before every engine launch.  
- Must be scanned after engine exits.

### **CABINCREW_TEMP_DIR**
- Optional ephemeral scratch directory.

The Orchestrator must never write inside workspace except during take-off  
_and only through the Engine_.

---

## 4. Running Engines

### **4.1 Invocation**
Engines are binaries launched with:

```
--mode flight-plan
--mode take-off
```

Input is passed through STDIN or an input file.

### **4.2 Reading Output**
Engines must print a JSON receipt to STDOUT.

The Orchestrator must:

- capture stdout  
- capture stderr for logs  
- fail if output is not valid JSON  
- fail if status = "failure"  

### **4.3 Timeouts**
Implementers may enforce timeouts.  
Timeouts must emit audit events.

---

## 5. Artifact Handling

After flight-plan:

- Scan each artifact folder  
- Ensure required files exist  
- Validate metadata against `artifact.schema.json`  
- Compute integrity hashes  
- Sort artifacts deterministically  
- Prepare them for plan-token generation

Artifacts cannot be modified after this stage.

---

## 6. Plan-Token Handling

The Orchestrator:

1. Computes per-artifact hashes  
2. Computes a composite plan hash  
3. Creates a plan-token  
4. Stores token in workflow state  
5. Emits audit event  

During take-off:

- recompute hashes  
- verify equality  
- refuse execution on mismatch  

Tokens must survive restarts.

---

## 7. Preflight Governance

Governance layers:

### **7.1 OPA Policies**
Evaluate:
- artifact metadata  
- workspace parameters  
- workflow context  
- risk indicators  

### **7.2 ONNX Models**
Evaluate:
- body.data content  
- metadata  
- behavior indicators  

### **7.3 Aggregation**
Decisions must follow priority:

1. deny  
2. require_approval  
3. warn  
4. allow  

### **7.4 Required Behaviors**
- deny → workflow stops  
- require_approval → pause  
- warn → continue, log warning  
- allow → proceed  

---

## 8. Approval System Integration

The Orchestrator must:

- generate ApprovalRequest objects  
- freeze workflow state  
- wait for human decision  
- validate ApprovalResponse binding to plan-token  
- resume workflow after approval  

Approval mismatches must result in workflow termination.

---

## 9. Take-Off Execution

During take-off, the Orchestrator must:

- load plan-token  
- validate artifacts  
- re-launch engine in `take-off` mode  
- ensure workspace is writable  
- ensure no mutation outside workspace occurs except via engine  

After take-off, the Orchestrator must:

- record outputs  
- store logs  
- emit audit events  

---

## 10. Audit Logging

Every step must generate audit events including:

- workflow transitions  
- engine start/stop  
- policy outcomes  
- decisions  
- approvals  
- warnings  
- errors  
- artifacts summary  
- plan-token creation/verification  

Audit logs should be:

- append-only  
- immutable  
- timestamped  
- machine-parseable  

---

## 11. Restart & Failure Handling

Orchestrator state must be persisted so workflows can continue after:

- crashes  
- restarts  
- network failure  
- power loss  

Persisted state should include:

- workflow step  
- plan-token  
- artifacts list  
- approval state  
- audit offsets  

The orchestrator must refuse to restart a workflow if:

- artifacts changed  
- plan-token invalid  
- approval mismatch  

---

## 12. Implementation Tips

### **12.1 Use a Deterministic File Walker**
Sort artifacts by name before hashing.

### **12.2 Use Hashing for Everything**
Reproducibility hinges on integrity.

### **12.3 Run OPA & ONNX in Sandboxes**
Avoid allowing policy engines to access host filesystem.

### **12.4 Keep Metadata Minimal**
Engine and orchestrator should exchange only necessary fields.

### **12.5 Start Small**
Minimum working orchestrator includes:
- engine launch  
- artifact scan  
- OPA allow/deny  
- take-off execution  

Everything else is incremental.

---

## 13. Suggested Architecture (Reference)

- core workflow state machine  
- engine runner  
- artifact validator  
- plan-token subsystem  
- preflight pipeline  
- approval subsystem  
- audit writer  
- workflow persistence layer  
- MCP gateway integration  
- LLM gateway integration  

---

## 14. Summary

A fully compliant CabinCrew Orchestrator is:

- deterministic  
- safety-focused  
- restart-resilient  
- auditable  
- modular  

It enforces the separation between *intent* and *execution*, ensures governance through policies and approvals, and provides the chain-of-custody required for enterprise-grade AI automation.

Refer to the specification in `spec/draft/` for normative rules.

