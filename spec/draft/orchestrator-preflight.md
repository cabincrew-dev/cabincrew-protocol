# CabinCrew Orchestrator Preflight Specification
Version: draft

This document defines the normative behavior of the CabinCrew Orchestrator during the Preflight phase. Preflight is the governance and validation stage that occurs after an Engine completes flight-plan but before take-off is permitted. It is the checkpoint where intent is verified, risks are assessed, and human approval may be required.

## 1. Purpose of Preflight

Preflight ensures that:

- the Engine's flight-plan is valid  
- artifacts are structurally correct  
- changes are safe and governed  
- risks are identified and mitigated  
- human approval is requested when required  
- take-off cannot proceed without explicit authorization  

Preflight is mandatory for all workflows.

---

## 2. Inputs to Preflight

Preflight operates on:

- the Engine's artifacts  
- the Engine receipt  
- the plan-token generated from artifacts  
- workflow configuration  
- OPA and ONNX policy definitions  
- orchestrator context (workflow state, metadata)  

Preflight has no side effects and must be deterministic.

---

## 3. Stages of Preflight

Preflight consists of four major stages:

### **3.1 Artifact Validation**

The Orchestrator must verify:

- correct directory structure  
- valid artifact.json schema  
- presence of body files when referenced  
- correct artifact roles (evidence, state, log)  
- consistent hashing and declared metadata  

Invalid artifacts must cause preflight failure.

---

### **3.2 Policy Evaluation (OPA)**

OPA policies evaluate:

- changes represented in artifacts  
- workflow metadata  
- repository or environment conditions  
- security implications  
- compliance requirements  

Each OPA rule may produce:

- allow  
- warn  
- deny  
- require_approval  

OPA evaluations must be included in audit events.

---

### **3.3 Model Evaluation (ONNX)**

ONNX models are used for ML-based safety checks, such as:

- detecting bias  
- identifying toxic or disallowed content  
- flagging insecure patterns  
- identifying hallucinations or deviations  
- detecting secrets or sensitive data  

Model outputs must be interpreted by the Orchestrator according to workflow policy.

Possible outcomes:

- allow  
- warn  
- deny  
- require_approval  

All decisions must be auditable.

---

### **3.4 Decision Aggregation**

OPA and ONNX results must be combined. The aggregator must follow this precedence:

1. **deny** — workflow stops immediately  
2. **require_approval** — workflow pauses  
3. **warn** — workflow continues but logs warning  
4. **allow** — workflow continues  

If multiple rules trigger, the most severe outcome takes priority.

The aggregated decision becomes the preflight result.

---

## 4. Human Approval Trigger

If the aggregated result is require_approval:

- Orchestrator generates an ApprovalRequest  
- Request includes:  
  - plan-token  
  - artifacts summary  
  - reason for escalation  
  - list of triggered policies  
- Workflow pauses  
- ApprovalResponse must match the plan-token  

If approved → continue to take-off  
If rejected → fail workflow

---

## 5. Plan-Token Verification

Before approving or continuing:

- The Orchestrator must re-hash artifacts  
- The computed token must match the stored token  
- If mismatched → workflow is denied with a critical audit event

This prevents modification or tampering between Flight-Plan and Preflight.

---

## 6. Audit Logging Requirements

Preflight must generate audit events for:

- artifact validation results  
- OPA evaluation results  
- ONNX evaluation results  
- aggregated decision  
- approval escalation  
- approval outcomes  
- plan-token verification status  

These events must conform to audit-event.schema.json.

---

## 7. Error Handling

Preflight must fail when:

- artifacts are invalid  
- policies cannot be evaluated  
- ML models fail to load  
- risk classification fails  
- plan-token verification fails  
- approval is rejected  
- any deny rule triggers  

All failures must produce audit events and halt the workflow.

---

## 8. Preconditions for Take-Off

Take-off may proceed only when:

- artifacts are valid  
- plan-token matches  
- aggregated decision = allow or warn  
- all approvals (if any) are completed successfully  

If any condition is unmet, take-off is forbidden.

---

## 9. Summary

Preflight is the governance checkpoint that protects users, systems, and data from unsafe or unintended automation. It validates intent, assesses risk using both policy rules and ML classifiers, ensures human oversight when needed, and enforces artifact integrity. The Orchestrator must implement all described behavior to ensure safe and deterministic workflows.
