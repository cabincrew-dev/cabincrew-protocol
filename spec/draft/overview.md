# CabinCrew Protocol Overview  
*Version: draft*

The CabinCrew Protocol defines a secure, deterministic, and governable automation model for AI-driven workflows. It introduces a set of components — **Engines**, **Orchestrators**, and **Gateways** — that collaborate to safely evaluate, approve, and execute high-impact operations such as writing files, modifying infrastructure, updating repositories, generating code, or invoking external APIs.

CabinCrew places **governance, auditability, and safety** as first-class concerns.  
Every meaningful action is recorded, validated, and optionally approved before execution.

---

## 1. Goals of the Protocol

CabinCrew is designed to:

### **1.1 Ensure deterministic, reproducible automation**
Automation must produce predictable results.  
Engines do not perform side effects during planning and must operate in controlled environments.

### **1.2 Provide strong governance and guardrails**
Before execution, all intent is evaluated using:

- OPA (policy rules)  
- ONNX models (ML classifiers or detectors)  
- Human approvals (for risky changes)

### **1.3 Establish a chain of custody**
A **plan-token** binds intent (flight-plan) and execution (take-off).  
Any modification invalidates the chain and prevents unsafe execution.

### **1.4 Support multi-agent AI workflows**
The protocol is compatible with:

- AI code agents (Aider, GitHub Copilot Workspace)
- AI inference systems
- Multi-stage automated pipelines
- MCP tool servers and function-calling models

CabinCrew acts as the controlling layer ensuring all agent actions are:

- logged  
- validated  
- reproducible  
- reversible  
- permissible  

### **1.5 Enable secure orchestration across heterogeneous systems**
Each component (engine, orchestrator, gateway) can run:

- locally  
- remotely  
- over air-gapped networks  
- inside containers / OCI bundles  

The protocol defines their interaction strictly through structured inputs/outputs and artifact directories.

---

## 2. High-Level Architecture

CabinCrew defines three primary classes of components:

### **2.1 Engines**
Engines are deterministic executables that:

- read structured input  
- operate inside a controlled workspace  
- emit artifacts  
- never perform side effects during `flight-plan`  
- perform side effects only during `take-off`

Examples:

- A Git engine producing diffs (plan) and applying commits (take-off)
- A Kubernetes engine producing manifests and applying changes
- A Terraform engine producing plans and applying infrastructure updates
- A code-mod engine generating patches and applying them

Engines output **artifacts**, not actions, and never directly mutate systems during planning.

---

### **2.2 Orchestrator**

The orchestrator coordinates workflow execution by:

- launching engines  
- managing artifact directories  
- validating output  
- enforcing preflight checks  
- pausing for approvals  
- verifying plan tokens  
- driving take-off execution

It is the **source of truth** for the workflow's state machine.

Orchestrator responsibilities include:

- Ensuring correct mode (flight-plan vs take-off)
- Guaranteeing determinism rules  
- Storing artifacts and state  
- Running governance layers  
- Generating audit events  
- Ensuring chain-of-custody integrity  
- Resuming workflows safely after interruptions  

---

### **2.3 Gateways (MCP + LLM)**

Gateways act as **policy-controlled firewalls** between AI agents and external interfaces.

Two standard gateway classes exist:

#### **• MCP Gateway**
Controls:

- file writes  
- file reads  
- tool invocations  
- API operations implemented as MCP servers  

#### **• LLM Gateway**
Controls:

- prompts  
- model access  
- routing to different LLMs  
- prompt rewriting  
- output classification  
- hallucination or safety checks  

Both gateways enforce:

- Allow  
- Warn  
- Deny  
- Require Approval  

And both emit audit events, but do not define their own audit schema — they use the global model.

---

## 3. Governance Layer

CabinCrew introduces multiple layers of governance:

### **3.1 OPA Policies**
Used for:

- access control  
- safety rules  
- workflow approval logic  
- content validation  
- risk scoring  

OPA outputs one of four decisions:

- allow  
- warn  
- deny  
- require_approval  

### **3.2 ONNX Policies**
ML-based detectors for:

- bias  
- toxicity  
- secrets  
- hallucinations  
- unsafe content  
- model-specific risk  

ONNX outputs become part of preflight or gateway evaluation.

### **3.3 Human Approval**
If either governance layer escalates, the orchestrator:

- stops the workflow  
- generates an ApprovalRequest  
- resumes only after ApprovalResponse  

This ensures sensitive operations (e.g., deleting databases, rewriting production configs) cannot occur without review.

---

## 4. Artifacts and Chain of Custody

Engines do not output raw content directly into EngineOutput.  
Instead, they populate a directory:

```
CABINCREW_ARTIFACTS_DIR/<name>/
    artifact.json
    body.data (optional)
```

Artifacts:

- define **what changed**  
- contain structured metadata  
- describe patches, diffs, or operations  
- support custom formats  
- are governed by `artifact.schema.json`

A **plan-token** binds the set of artifacts to the flight-plan.  
Take-off is only permitted if the token remains valid.

This establishes strict integrity guarantees.

---

## 5. Workflow Overview

A typical CabinCrew workflow:

### **Step 1: Flight-Plan**
Engine runs in read-only mode and produces:

- evidence artifacts  
- state artifacts  
- a plan-token  

### **Step 2: Preflight Checks**
OPA + ONNX evaluate the plan:

- allow  
- warn  
- deny  
- require_approval  

### **Step 3: Approval (optional)**
Human approves or denies.

### **Step 4: Take-Off**
Engine applies side effects:

- writing files  
- applying patches  
- committing changes  
- modifying infrastructure  

Only allowed if plan-token remains valid.

### **Step 5: Audit**
Every step emits an audit event with:

- inputs  
- outputs  
- decisions  
- gateway evaluations  
- token verification  
- artifact integrity results  

---

## 6. Design Philosophy

CabinCrew exists to enable:

- **AI automation without blind trust**
- **Reproducible and safe agent workflows**
- **Deterministic infrastructure and code operations**
- **Unified governance across all AI actions**
- **Deep auditability and forensic traceability**

It is neither a runtime nor a framework —  
It is a **protocol** that standardizes how intelligent systems can safely produce and apply changes.

---

## 7. Next Steps

For detailed specifications, refer to:

- `engine.md`  
- `orchestrator.md`  
- `artifact.md`  
- `plan-token.md`  
- `mcp-gateway.md`  
- `llm-gateway.md`  
- `audit-event.md`
