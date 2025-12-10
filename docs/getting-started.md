# Getting Started with CabinCrew Protocol
Version: draft

This document provides a high-level, non-normative introduction for new users who want to understand how CabinCrew works in practice. It complements the `overview.md`, `architecture.md`, and `principles.md` files by showing how the pieces fit together in a real workflow.

## 1. What Is CabinCrew?

CabinCrew is an open protocol for **safe, deterministic, auditable AI-assisted automation**. It provides:

- flight-plan (intent) and take-off (execution) phases  
- governance using policy rules (OPA) and safety models (ONNX)  
- human approval workflows  
- MCP Gateway for safe tool access  
- LLM Gateway for safe model interaction  
- audit trails and chain-of-custody via plan-tokens  

CabinCrew helps organizations automate confidently without losing safety or control.

---

## 2. Core Components

### **Engine**
A deterministic binary that:
- generates intent during flight-plan
- applies changes during take-off
- emits structured artifacts

### **Orchestrator**
Controls the workflow:
- runs engines in isolation  
- validates artifacts  
- performs governance checks  
- handles approvals  
- executes take-off  

### **Gateways** (MCP + LLM)
Firewalls that inspect:
- file writes / patches  
- tool invocations  
- prompts and LLM outputs  

Gateways enforce governance at the boundary where AI interacts with systems.

### **Audit Layer**
Records every meaningful event immutably.

---

## 3. Basic Workflow

A typical CabinCrew workflow looks like:

1. **Engine → flight-plan**
   - engine produces artifacts describing intent  
   - orchestrator saves and validates them  

2. **Orchestrator → Preflight**
   - OPA policies evaluate artifact metadata  
   - ONNX models evaluate content  
   - aggregated decision = allow, warn, deny, require_approval  

3. **Human Approval (optional)**
   - if escalated, workflow pauses  
   - human approves or rejects  

4. **Engine → take-off**
   - orchestrator verifies plan-token  
   - engine applies changes deterministically  

5. **Audit**
   - every step logged securely  

---

## 4. Example Use Cases

### **AI Code Editing (Aider-like workflows)**
- Engine generates git diffs  
- Preflight checks for secrets, risky code, or unsafe operations  
- Gateway blocks dangerous file writes  
- Human can approve or reject before commit/push  

### **Infrastructure-as-Code**
- Engine produces a deployment plan  
- OPA applies compliance rules  
- Human approves production changes  
- Take-off executes apply safely  

### **Enterprise LLM Usage**
- LLM Gateway routes prompts through safety models  
- Blocks insecure or toxic outputs  
- Ensures prompts do not leak secrets  
- Provides audit trail for compliance  

---

## 5. Building Your First Engine

A minimal engine needs to:

- accept JSON input via STDIN  
- operate inside `CABINCREW_WORKSPACE`  
- write artifacts to `CABINCREW_ARTIFACTS_DIR`  
- emit a JSON receipt on STDOUT  

Example structure:
```
/tmp/workspace/
  (your project files)

CABINCREW_ARTIFACTS_DIR/
  my_patch/
    artifact.json
    body.data
```

Your engine does not deal with:
- policy logic  
- approvals  
- tokens  
- gateways  

The orchestrator handles all governance.

---

## 6. Governance & Safety

CabinCrew provides layered protection:

### Layer 1 — OPA Policies
Rules like:
- “no writes outside workspace”
- “patch cannot modify credentials”
- “production deploys require human approval”

### Layer 2 — ONNX Models
ML-based checks:
- bias detection  
- toxic content  
- secret detection  
- hallucination risk  

### Layer 3 — Human Approval
For high-risk scenarios.

### Layer 4 — Gateways
Runtime firewalls for MCP and LLM operations.

---

## 7. Implementation Roadmap (Simplified)

To integrate CabinCrew:

1. Write or adopt an engine.  
2. Configure orchestrator workflow steps.  
3. Enable preflight policies.  
4. Run MCP Gateway around agent tools.  
5. Wrap LLM calls via LLM Gateway.  
6. Collect audit logs.  

You can start small and add safety layers gradually.

---

## 8. Learning More

For detailed specifications:
- `spec/draft/overview.md`
- `spec/draft/architecture.md`
- `spec/draft/principles.md`
- `spec/draft/engine.md`
- `spec/draft/orchestrator.md`
- `spec/draft/mcp-gateway.md`
- `spec/draft/llm-gateway.md`

Schemas for implementers:
- `schema/draft/*.json`

---

## 9. Summary

CabinCrew bridges the gap between intelligent automation and the safety, auditability, and determinism required by real-world systems. This document introduces the concepts; more detailed behavior is defined in the specification files.

