# Gateway Implementer’s Guide (MCP & LLM Gateways)
Version: draft

This guide explains how to implement the **MCP Gateway** and **LLM Gateway** components of the CabinCrew Protocol. These gateways act as governance firewalls for agent tool calls and LLM interactions. They enforce policy, provide safety guarantees, and generate audit events.

Normative rules exist in:
- `spec/draft/mcp-gateway.md`
- `spec/draft/llm-gateway.md`
- `spec/draft/audit-event.md`
- `schema/draft/mcp-gateway.schema.json`
- `schema/draft/llm-gateway.schema.json`

This guide provides practical steps and architectural recommendations.

---

## 1. Purpose of Gateways

Gateways sit between an **upstream caller** (agent, orchestrator, engine) and a **downstream service** (MCP server or LLM API).

They enforce:

- OPA policy checks  
- ONNX safety checks  
- audit-event generation  
- deterministic routing (for LLMs)  
- controlled access to files, tooling, and model behavior  
- optional human-approval workflows  

Gateways **must never be bypassed** once deployed.

---

## 2. High-Level Responsibilities

### **MCP Gateway**
- Intercepts MCP tool calls (file operations, API tools, retrievals)  
- Applies policy rules to each request and response  
- Blocks, warns, modifies, or allows requests  
- Ensures safe file paths and patch application  
- Generates audit events for each request  

### **LLM Gateway**
- Intercepts prompt completion, embeddings, reranking  
- Applies safety routing and model selection  
- Runs OPA + ONNX safety checks  
- Handles approval-required outputs  
- Optionally rewrites prompts  
- Logs all events via audit system  

Both gateways share the same enforcement pipeline.

---

## 3. The Gateway Enforcement Pipeline

For every request:

1. **Receive Request** from caller  
2. **Validate structure** against schema  
3. **Run OPA evaluation** on the request  
4. **Run ONNX evaluation** (optional or configured)  
5. **Aggregate decisions**:  
   - deny  
   - require_approval  
   - warn  
   - allow  
6. **If require_approval → pause workflow**  
7. **If deny → reject request**  
8. **If allow or warn → forward request**  
9. **Receive downstream response**  
10. **Run response OPA/ONNX evaluations**  
11. **Aggregate again**  
12. **Required actions:**  
    - deny response  
    - sanitize/redact  
    - request approval  
    - forward response  
13. **Generate audit event**  

This pipeline must be deterministic.

---

## 4. OPA Integration

### **OPA Input Structure**
OPA must receive:

- request or response payload  
- user identity or workflow context  
- file paths (MCP)  
- prompt or model selection (LLM)  
- gateway config  
- previous decisions (optional)  

OPA should be loaded once and reused per request for performance.

### **Policy Result Format**
OPA output should include:

- decision (allow, warn, deny, require_approval)  
- optional annotations  
- optional rule-level explanations  

OPA failure must default to **deny**, unless configured differently.

---

## 5. ONNX Model Integration

ONNX models may classify:

### **For MCP**
- secret presence  
- dangerous file paths  
- sensitive data  
- policy-violating patterns  

### **For LLM**
- toxicity  
- hallucination risk  
- bias  
- prompt sensitivity  
- leakage of secrets  

The gateway must:

- load models at startup  
- run inference on relevant content  
- map scores to governance decisions  

If ONNX fails to load:
- default to "deny" or "fallback-only" model modes based on config.

---

## 6. Human Approval Integration

When either OPA or ONNX yields `require_approval`, the gateway must:

1. Create an **ApprovalRequest**  
2. Record it in the audit system  
3. Suspend the request (async or blocking)  
4. Wait for human decision  
5. Validate **ApprovalResponse**  
6. Continue or deny accordingly  

Approval must include hashes of:

- request payload  
- model selection (LLM)  
- file paths or patch metadata (MCP)  

No replay attacks must be possible.

---

## 7. MCP Gateway Implementation Details

### **7.1 Allowed Operations**
Typical MCP operations:

- read file  
- write file  
- apply patch  
- ls / stat  
- structured tools (API-like)  

### **7.2 Path Safety**
MCP Gateway must enforce:

- workspace root boundaries  
- no `..` traversal  
- restricted file action types  
- controlled patch operations  

### **7.3 Request Mutation**
Gateway may modify request only if configured, for example:

- patch sanitization  
- path normalization  
- removal of unsafe fields  

### **7.4 Response Handling**
Gateway must check:

- patch results  
- file content diffs  
- metadata operations  

Unsafe outputs must be blocked or sanitized.

---

## 8. LLM Gateway Implementation Details

### **8.1 Model Routing Logic**
Routing strategies may include:

- primary → fallback  
- safety-tier routing  
- cost-based routing  
- model-specific constraints  
- randomization for load balancing  

Routing decisions must be logged.

### **8.2 Prompt Rewriting**
Allowed rewriting includes:

- inserting system safety directives  
- removing unsafe user input  
- enforcing structured response format  

Rewriting must be auditable.

### **8.3 Response Validation**
LLM responses must be checked with:

- OPA  
- ONNX  
- redaction rules  

Unsafe content must trigger:

- block  
- regenerate (fallback)  
- require_approval  

---

## 9. Audit Requirements

Each gateway action must produce an audit event containing:

- request id  
- caller identity  
- request payload  
- sanitized content references  
- policy evaluations  
- final decision  
- response snapshot  
- model selection or tool name  
- timestamps  

Audit events must follow `audit-event.schema.json`.

---

## 10. Restart & Failure Behavior

Gateway must:

- reload configuration safely  
- preserve pending approval states  
- never forward a request without evaluation  
- treat policy or model failures as deny (configurable)  

Requests must not be duplicated without explicit instruction.

---

## 11. Recommended Architecture

### **Subsystems**
- request validator  
- policy engine (OPA)  
- model inference engine (ONNX)  
- router (LLM)  
- patch sanitizer (MCP)  
- approval subsystem  
- audit writer  
- metrics + health checks  

### **Concurrency**
Gateways should use:

- worker pools  
- async approval handlers  
- circuit breakers for downstream APIs  

---

## 12. Minimal MVP

To build a functional Gateway:

### **MCP Gateway MVP**
- intercept read/write/apply_patch  
- run OPA allow/deny  
- block writes outside workspace  
- log requests  

### **LLM Gateway MVP**
- rewrite prompt with safety system message  
- run simple OPA rule  
- forward to a single model  
- log request/response  

This MVP demonstrates the protocol and enables adoption.

---

## 13. Summary

Gateways enforce governance for AI-driven automation.  
They ensure:

- safe tooling  
- safe LLM outputs  
- deterministic policy evaluation  
- auditable behavior  
- optional human approvals  
- integration with CabinCrew’s chain-of-custody model  

This guide provides practical instructions; implementers must also follow the normative spec files.

