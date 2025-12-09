# CabinCrew Glossary
Version: draft

This glossary defines the terminology used across all CabinCrew Protocol specifications. These definitions are normative unless stated otherwise. All components (engines, orchestrators, gateways, external tools) must interpret these terms consistently.

---

## A

### **Action**
A declared intent inside an artifact describing what operation should occur during take-off (e.g., create, update, delete, apply, execute). Actions are free-form strings and not restricted to enums.

### **Aggregated Decision**
The final result of combining OPA and ONNX policy evaluations. Precedence:  
1. deny  
2. require_approval  
3. warn  
4. allow

### **Approval**
A human decision authorizing continuation of a workflow when risk is detected.

### **ApprovalRequest**
A structured object created by the orchestrator or a gateway when a human decision is required.

### **ApprovalResponse**
A structured object that records the human decision and allows workflow continuation or termination.

---

## B

### **Body File**
Optional binary or textual content associated with an artifact, stored as body.data.

---

## C

### **Chain of Custody**
Formal guarantee that workflow intent has not been modified between flight-plan and take-off. Enforced via plan-tokens and audit logs.

### **Composite Hash**
A deterministic hash of all artifact metadata used to form the plan-token.

### **Config**
User-supplied configuration passed to an engine through workflow definitions.

---

## E

### **Engine**
A deterministic execution unit that produces artifacts in flight-plan mode and executes validated actions in take-off mode.

### **EngineInput**
Structured input passed to the engine via STDIN or input file.

### **EngineOutput**
Structured output emitted by the engine via STDOUT.

---

## F

### **Flight-Plan**
The planning phase where the engine computes intent without performing side effects.

---

## G

### **Gateway**
A policy enforcement proxy (MCP Gateway or LLM Gateway) that mediates external operations.

---

## H

### **Hash**
A cryptographic digest (typically SHA-256) used for integrity verification.

---

## I

### **Integrity**
Property ensuring that artifacts and workflow state have not been tampered with.

---

## L

### **LLM Gateway**
Governance firewall for all interactions with large language models, including safety routing and prompt evaluation.

---

## M

### **MCP Gateway**
Governance firewall for MCP-based tool invocations such as file operations and API-like tools.

### **Metadata (Artifact Metadata)**
Structured information describing an artifact’s type, action, parameters, and body file reference.

---

## O

### **OPA (Open Policy Agent)**
Rule engine used for deterministic governance evaluation.

### **ONNX**
Portable model format used for ML-based risk classification.

### **Orchestrator**
Authoritative state machine controlling workflow execution, governance, approvals, and artifact validation.

---

## P

### **Plan-Token**
Cryptographic binding between flight-plan artifacts and take-off execution path.

### **Preflight**
Governance stage that evaluates artifacts using OPA and ONNX before permitting take-off.

### **Prompt Rewriting**
Optional transformation of LLM prompts performed by the LLM Gateway for safety or standardization.

---

## R

### **Receipt**
Structured output from an engine describing execution results, artifacts produced, and diagnostic metadata.

### **Restart-Safe Behavior**
Orchestrator requirement ensuring workflows can resume deterministically after system restart.

---

## S

### **State Artifact**
Artifact role providing data required for take-off, such as terraform plans or git bundles.

### **Structured Artifact**
Any artifact represented with artifact.json and optional body.data.

---

## T

### **Take-Off**
The execution phase where validated side effects occur based on plan-token–verified artifacts.

### **Tool Call (MCP Tool Call)**
A request from an agent or engine to perform file or structured operations via MCP.

---

## U

### **Upstream Caller**
The engine, agent, or orchestrator issuing a request to a gateway.

---

## W

### **Warn Decision**
A governance decision that permits workflow continuation while generating an audit warning.

### **Workflow**
A sequence of steps executed by the orchestrator, involving planning, governance, approval, and execution.

---

## Summary

The glossary provides unified terminology across the CabinCrew Protocol. All components must interpret definitions consistently to ensure interoperability, determinism, and correct behavior across orchestrator, engines, gateways, and audit systems.

