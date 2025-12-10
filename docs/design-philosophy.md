# CabinCrew Design Philosophy
Version: draft

This document explains the foundational principles and mental models that shaped the CabinCrew Protocol.  
It supplements (but does not replace) the normative specifications by describing *why* the protocol is designed the way it is, and *how* implementers should think when extending or integrating with CabinCrew.

---

# 1. Philosophy Overview

Modern AI systems are powerful but unpredictable.  
Traditional automation is predictable but rigid.

CabinCrew’s mission is to **bridge these two worlds**:

> **Allow AI to assist in automation, while ensuring the final execution is deterministic, auditable, and governed.**

This requires the combination of:
- strict safety guarantees  
- reproducible execution  
- agent and LLM safety firewalls  
- human oversight  
- structured artifacts  
- chain-of-custody enforcement  

CabinCrew is designed as a **governance-first protocol**, not an agent framework.

---

# 2. Determinism as the Foundation

CabinCrew prioritizes determinism over convenience.

This means:
- Engines must behave deterministically.  
- Flight-plan calculations must be reproducible.  
- Artifacts must be stable, ordered, and hashable.  
- Take-off must apply exactly what was planned.  

AI introduces nondeterminism, so the protocol introduces deterministic boundaries:

- AI can propose changes  
- but **cannot execute them without governance**  
- and **cannot modify artifacts after planning**  
- and **cannot bypass gateways**  

This preserves safety without limiting creativity.

---

# 3. Separation of Intent and Execution

At the core of CabinCrew is a simple principle:

> **Think before you act.**

This principle takes the form of:
- **flight-plan** (intent)  
- **take-off** (execution)  

No changes may occur during flight-plan.  
No changes may occur outside planned artifacts during take-off.

This prevents:
- accidental or malicious code execution  
- unsafe file modifications  
- out-of-band side effects  
- manipulation of artifact content after approval  

It is the equivalent of Terraform’s plan/apply, generalized to agents and LLM-driven workflows.

---

# 4. Chain-of-Custody and Trust

CabinCrew assumes all components except the orchestrator may be untrusted.

This includes:
- engines  
- agents  
- LLMs  
- gateway downstream services  
- MCP servers  
- tools  

To ensure correctness in an untrusted environment:

### The plan-token binds:
- artifacts  
- metadata  
- workspace state  
- governance decisions  
- approvals  

If anything changes → the workflow must stop.

---

# 5. Human Governance as a First-Class Mechanism

Unlike many automation frameworks, CabinCrew explicitly integrates human oversight.

Because automation involving AI may be high-risk, the protocol ensures that:

- policies can promote actions to **require_approval**  
- reviewers see full artifact context  
- approvals bind cryptographically to plan-token  
- approvals cannot be reused or replayed  

Human-in-the-loop is not a bolt-on feature —  
it is part of the **protocol contract**.

---

# 6. Gateways as Firewalls

CabinCrew introduces two firewalls:

### **MCP Gateway**
For deterministic control of:
- file operations  
- patches  
- external tool calls  

### **LLM Gateway**
For safety control of:
- prompts  
- completions  
- model routing  

These gateways enforce:
- policy  
- ONNX-based safety checks  
- audit logging  

Gateways exist because LLMs and agents:
- are nondeterministic  
- may behave adversarially  
- may hallucinate unsafe commands  
- must not be trusted with direct access to systems  

CabinCrew treats them as:
> **powerful assistants, not autonomous actors.**

---

# 7. Auditability: Every Action Must Be Traceable

Automation without auditability is unsafe.

CabinCrew’s design ensures that every meaningful action is logged:
- engine start/stop  
- artifact generation  
- plan-token creation  
- policy evaluation  
- gateway decisions  
- approval flows  
- take-off execution  

Audit logs serve as:
- forensics  
- compliance artifacts  
- replay tools  
- debugging assets  

No action should be “magic.”

---

# 8. Restart Safety

A resilient system must survive restarts, crashes, or partial execution.

CabinCrew is designed for:
- resumable workflows  
- state recovery  
- deterministic resumption  
- immutable plan-token restoration  

Workflow state must always be:
- persisted  
- consistent  
- validated upon recovery  

This allows CabinCrew workflows to run in:
- CI/CD systems  
- orchestrators like Kubernetes  
- ephemeral runners  
- air-gapped environments

---

# 9. Extensibility Without Fragmentation

The protocol is designed to be:
- minimal  
- decoupled  
- language-agnostic  
- modular  

But must avoid fragmentation.  
This is accomplished by:

- versioned schemas  
- stable interfaces  
- deterministic artifact models  
- clear normative requirements  
- freedom in internal engine implementation  

Implementers can build:
- custom engines  
- custom gateways  
- orchestration variants  
- extended governance plugins  

…without breaking compatibility.

---

# 10. Philosophy Summary

CabinCrew is built on the following pillars:

### **1. Deterministic execution**
Automation must be predictable.

### **2. Reproducible planning**
Intent must be computed without side effects.

### **3. Governance-first automation**
Policies and safety models have priority.

### **4. Human oversight**
Approval is part of the system design.

### **5. Cryptographic chain-of-custody**
Integrity is always verifiable.

### **6. Safety firewalls**
LLMs and MCP tools operate behind strict boundaries.

### **7. Full auditability**
No hidden behavior.

### **8. Extensibility without risk**
Components are replaceable but interoperable.

CabinCrew exists to make AI-assisted automation **trustworthy**, **safe**, and **enterprise-ready** — without sacrificing flexibility or developer experience.

