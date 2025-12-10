# CabinCrew Governance Model
Version: draft

This document describes the **governance subsystem** of CabinCrew — the rules, mechanisms, and evaluation pipeline that ensure all automation driven by AI, agents, or engines remains safe, auditable, and compliant.

Governance in CabinCrew is based on three pillars:

1. **OPA Policies** (deterministic rule evaluation)  
2. **ONNX Models** (ML-based risk classification)  
3. **Human Approval Workflow** (structured oversight)

These layers work together to enforce safe behavior before any real-world side effects occur.

---

# 1. Governance Overview

Governance occurs primarily during **preflight**, but may also occur:

- before forwarding MCP operations  
- before forwarding LLM requests  
- after receiving LLM responses  
- before running take-off  
- during post-execution audits  

CabinCrew governance answers the question:

> *“Is it safe to continue?”*

The answer is one of:

- **allow**  
- **warn**  
- **deny**  
- **require_approval**  

---

# 2. Governance Pipeline

Governance follows a strict sequence:

1. **Collect governance inputs**
2. **Run OPA evaluation**
3. **Run ONNX evaluation**
4. **Normalize results**
5. **Aggregate to final decision**
6. **Apply enforcement action**
7. **Generate audit event**

This pipeline is identical across:

- Preflight governance  
- MCP Gateway  
- LLM Gateway  
- Optional post-takeoff governance  

---

# 3. Governance Inputs

OPA and ONNX receive structured inputs including:

### **Artifact Metadata**
- type  
- action  
- parameters  
- file paths  
- hash values  

### **Artifact Body**
- diffs  
- manifests  
- plans  
- prompts  
- code blocks  

### **Workflow Context**
- workflow_id  
- step_id  
- mode: flight-plan | take-off  
- approval state  

### **Caller Context**
- user identity  
- agent identity  
- tool identity  
- model identity  

### **Orchestrator Configuration**
- safety level  
- policy bundle versions  
- enabled ONNX models  

### **Environmental Constraints**
- workspace boundaries  
- safe path lists  
- forbidden operations  

---

# 4. OPA Governance

OPA is used for *deterministic, rule-based governance*.  
It is ideal for:

- compliance rules  
- access control  
- file safety checks  
- patch validation  
- model selection rules  
- required approvals  
- runtime restrictions  

OPA output must include:

```
{
  "decision": "allow" | "warn" | "deny" | "require_approval",
  "annotations": {...optional...}
}
```

OPA failures must default to **deny** unless explicitly configured otherwise.

---

# 5. ONNX Governance

ONNX models provide *probabilistic, ML-driven governance signals* such as:

### **Risk Classification**
- code vulnerability detection  
- secret leakage prediction  
- hallucination detection  
- bias and toxicity classification  
- sensitive content detection  

### **Safety Routing Decisions**
- “use safe-mode LLM”  
- “fallback to lower-temperature model”  

### **Output Validation**
- blocking unsafe patches  
- blocking unsafe generated text  
- scanning code for insecure patterns  

ONNX output is normalized to:

```
"allow" | "warn" | "deny" | "require_approval"
```

Thresholds are defined in gateway/orchestrator config.

If ONNX models fail to load → system must fallback safely or deny.

---

# 6. Decision Aggregation

OPA and ONNX produce separate decisions.

The Orchestrator/Gateway must aggregate them with strict precedence:

### **1. deny**  
### **2. require_approval**  
### **3. warn**  
### **4. allow**  

This means:

| OPA | ONNX | Final |
|-----|------|--------|
| allow | deny | deny |
| warn | allow | warn |
| require_approval | allow | require_approval |
| allow | warn | warn |
| require_approval | warn | require_approval |
| allow | allow | allow |

Aggregation guarantees conservative behavior.

---

# 7. Enforcement Behaviors

Depending on the final aggregated decision:

## **allow**
- Continue execution normally  
- Log an audit event  

## **warn**
- Continue execution  
- Attach warning annotations  
- Emit audit warning  

## **deny**
- Stop workflow  
- Mark as FAILED  
- Emit critical audit event  

## **require_approval**
- Pause workflow  
- Generate ApprovalRequest  
- Wait for human reviewer  
- Enforce binding to plan-token  

---

# 8. Human Governance

Human oversight is integrated directly into the governance system.

Approvals are required when:

- OPA or ONNX indicates risk  
- Patch or file changes exceed thresholds  
- LLM text contains sensitive content  
- Critical infrastructure changes occur  
- Policies explicitly mandate approval  

Human reviewers receive:

- artifact metadata  
- diffs or code changes  
- policy rule explanations  
- classifier outputs  
- workflow context  

ApprovalResponse must bind to the plan-token to prevent replay.

---

# 9. Governance Across Components

Governance is enforced at multiple boundaries:

## **9.1 Orchestrator Preflight**
Evaluates flight-plan artifacts before take-off.

## **9.2 MCP Gateway**
Evaluates:
- file writes  
- patch operations  
- external tool invocations  

## **9.3 LLM Gateway**
Evaluates:
- prompts  
- completions  
- embeddings  
- reranking requests  

## **9.4 Post-Takeoff**
Optional validation after execution.

Governance is consistently applied everywhere.

---

# 10. Recommended Governance Rules (Examples)

## **File Safety**
- deny writes outside workspace  
- require approval for modifying more than N lines  
- deny patching sensitive files (e.g., `.env`, credentials)  

## **LLM Safety**
- deny prompts containing secrets  
- require approval for production deployment suggestions  
- warn on hallucination risk > threshold  

## **Infrastructure Governance**
- require approval for modifying production resources  
- deny deletion operations without explicit override  

## **Agent Behavior**
- deny recursive tool calls  
- warn on excessive tool usage patterns  

---

# 11. Governance Bundle Structure

Governance rules should be packaged as a **bundle** including:

```
policies/
    *.rego
models/
    *.onnx
config/
    thresholds.json
```

Bundles may be versioned and distributed via:

- Git repo  
- OCI registry  
- Archive file  

Orchestrators and Gateways must validate bundle integrity.

---

# 12. Governance Philosophy

Governance in CabinCrew is designed to:

- assume non-trust in Engines, LLMs, and Agents  
- prioritize safety over convenience  
- guarantee deterministic, explainable outcomes  
- integrate human judgment when needed  
- be extensible without weakening security  

Governance is not optional — it is the defining feature of CabinCrew.

---

# 13. Summary

The CabinCrew governance model creates a layered defense system combining:

- deterministic rules (OPA)  
- machine learning risk detection (ONNX)  
- cryptographically enforced state (plan-token)  
- human oversight (approvals)  
- full auditability  

Together, these mechanisms ensure automation remains **safe**, **transparent**, and **enterprise-ready**, even when driven by powerful AI agents or LLMs.

