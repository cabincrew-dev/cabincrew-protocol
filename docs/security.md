# CabinCrew Security Model
Version: draft

This document describes the CabinCrew Protocol security model, the trust boundaries, and the required behaviors for orchestrators, engines, gateways, and external integrations. It supplements (but does not replace) the normative specification files.

CabinCrew’s mission is to provide **deterministic, auditable, and governable automation** in environments where safety and correctness are critical.

---

## 1. Security Goals

CabinCrew is designed to enforce:

### **1.1 Integrity**
Workflows must not execute unless all artifacts match their plan-token.

### **1.2 Determinism**
Given the same inputs and workspace state, execution must produce the same results.

### **1.3 Governance**
All steps must undergo policy evaluation (OPA, ONNX) before execution.

### **1.4 Auditability**
Every meaningful operation must generate structured, immutable audit events.

### **1.5 Replay Protection**
Plan-token binding prevents:
- stale approvals  
- tampering  
- workflow replay with modified artifacts  

### **1.6 Human Oversight**
High-risk operations require explicit human approval.

---

## 2. Threat Model Overview

CabinCrew assumes the following adversaries may exist:

### **2.1 Malicious or Compromised Engine**
An engine may:
- attempt side effects during flight-plan  
- generate harmful artifacts  
- corrupt state  
- hide malicious behavior in binary payloads  

### **2.2 Rogue Agent / LLM Behavior**
Agents or LLMs may:
- produce unsafe code changes  
- attempt privilege escalation  
- leak secrets  
- hallucinate dangerous operations  

### **2.3 Malicious Gateway Bypass Attempts**
Attackers may attempt:
- direct write operations  
- executing LLM calls outside gateway  
- subverting MCP tools  

### **2.4 Supply Chain Tampering**
Includes:
- modified binaries  
- tampered artifacts  
- manipulated model weights  
- compromised dependencies  

### **2.5 Infrastructure-Level Failures**
Such as:
- restarts  
- partial writes  
- system crashes  

---

## 3. Trust Boundaries

CabinCrew defines clear trust boundaries:

### **3.1 Orchestrator = Trusted**
It is the root of authority.

### **3.2 Engines = Untrusted**
They must run inside controlled directories and cannot bypass governance.

### **3.3 Gateways = Semi-Trusted**
Gateways enforce governance but must audit themselves.

### **3.4 LLM Providers = Untrusted**
Outputs must undergo sandboxed evaluation.

### **3.5 MCP Servers = Untrusted**
Any tool invocation may be risky.

---

## 4. Security Enforcement Layers

CabinCrew uses a multilayered defense model:

### **4.1 Isolation via Workspace + Artifacts Directories**
Prevent Engines from:
- touching system files  
- escaping workspace  
- modifying artifacts after plan phase  

### **4.2 Plan-Token Integrity**
Prevents:
- tampering  
- replay attacks  
- reusing approvals  
- modifying plan outputs before take-off  

### **4.3 OPA Policy Enforcement**
Controls:
- file write safety  
- allowed operations  
- model-selection rules  
- compliance constraints  
- workflow context restrictions  

### **4.4 ONNX Model Enforcement**
Detects:
- hallucinations  
- bias  
- unsafe content  
- secret leakage  
- dangerous patches  

### **4.5 Approval Workflow**
Guarantees:
- human oversight  
- deterministic binding to plan-token  
- non-replayable confirmations  

### **4.6 Audit Layer**
Ensures:
- forensics  
- compliance  
- non-repudiation  
- reproducibility  

---

## 5. MCP Gateway Security

The MCP Gateway must enforce:

- strict path whitelisting  
- no `..` traversal  
- patch sanitization  
- redaction of secrets  
- OPA denial for unsafe file operations  
- audit logging for all requests  

It must block:
- raw shell access  
- privileged operations  
- filesystem-level escape attempts  

---

## 6. LLM Gateway Security

LLM Gateway must:

- route unsafe prompts to safer models  
- rewrite prompts to reduce risk  
- detect unsafe outputs  
- require human approval for risky responses  
- audit everything  

It may NOT:
- store raw prompts unless configured  
- bypass model-safety rules  
- allow direct LLM access from Engines or Agents  

---

## 7. Workflow Restart Guarantees

Upon restart, Orchestrator must ensure:

- artifacts hashing matches plan-token  
- approvals remain bound to the same plan  
- state is resumed in a safe, deterministic order  
- no step is replayed unless intended  
- no step is skipped  

If validation fails → workflow must halt.

---

## 8. Supply Chain Security

Implementers should:

### **8.1 Verify Engine Binaries**
Using:
- signatures  
- checksums  
- OCI-based distribution  

### **8.2 Verify Model Integrity**
- ONNX model hashes  
- signed model releases  
- reproducible loading  

### **8.3 Registry & Distribution Controls**
Use private registries when available.

---

## 9. Logging & Secrets Handling

Secrets must:

- never appear in audit logs  
- be redacted in artifacts  
- not be exposed through LLM prompts  
- be bounded to workflow context only  

Audit logs must not contain:
- access tokens  
- private keys  
- raw credentials  

---

## 10. Mandatory Security Behaviors

CabinCrew-compliant orchestrators MUST:

- deny execution when uncertain  
- require approval for ambiguous situations  
- enforce policy deterministically  
- never ignore gateway failures  
- never allow Engines to bypass governance  

CabinCrew-compliant gateways MUST:

- evaluate every request and response  
- produce audit events  
- enforce path boundaries  
- block model-unsafe outputs  

---

## 11. Summary

CabinCrew’s security model is designed to prevent:

- unauthorized modifications  
- unsafe LLM or agent behavior  
- tampering with workflows  
- misuse of tooling  
- unreviewed execution  
- loss of audit trail  

Through the combination of:
- deterministic Engines  
- strong governance  
- human approval  
- plan-token integrity  
- audit logging  
- MCP/LLM safety gateways  

CabinCrew provides an enterprise-grade security layer for AI-driven automation.

