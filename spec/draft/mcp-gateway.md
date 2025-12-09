# CabinCrew MCP Gateway Specification
Version: draft

The MCP Gateway is a policy-controlled firewall that sits between AI agents, engines, or orchestrators and any MCP-compatible tool server. It ensures that all file operations, tool invocations, and resource accesses are governed, auditable, and optionally subject to human approval. This document defines the required behavior of the MCP Gateway.

## 1. Purpose of the MCP Gateway

The MCP Gateway enforces governance on:
- file reads and writes
- directory creation and deletion
- patch applications
- structured tool invocations
- network-like MCP tools
- any side-effect–producing operation exposed through MCP

Its key responsibilities are:
- enforcing OPA / ONNX rules
- routing requests to the downstream MCP server
- preventing unsafe or unauthorized actions
- generating audit events for all requests and responses
- supporting allow / warn / deny / require_approval decisions

---

## 2. Gateway Position in the Architecture

The MCP Gateway sits between:
- **Upstream caller** (agent, orchestrator, engine wrapper)
- **Downstream MCP server**

It must intercept all MCP messages:
- requests  
- responses  
- notifications  

and apply governance on the request path (mandatory) and optionally on the response path.

The Gateway must never be bypassed.

---

## 3. Intercepted MCP Actions

The Gateway must intercept and evaluate at minimum:

1. **file.read**
2. **file.write**
3. **file.append**
4. **file.delete**
5. **file.list**
6. **file.apply_patch**
7. **any tool invocation** (e.g., database query, API call, git operation)

Actions are treated generically:
- Each request is structured data.
- Policies evaluate the request body.
- Decisions apply uniformly regardless of tool type.

The Gateway must support extensible actions and tool namespaces.

---

## 4. Policy Evaluation

Every MCP request must be evaluated by:

### 4.1 OPA Policies
OPA may define rules regarding:
- file paths
- allowed extensions
- workspace boundaries
- maximum write size
- allowed deletion patterns
- tool-level permissions
- environment or workflow context

OPA result options:
- allow  
- warn  
- deny  
- require_approval  

### 4.2 ONNX Models
ML-based classification may analyze:
- file content
- patches
- secrets or credentials
- toxicity or unsafe language
- intent inference for dangerous commands

ML evaluation must be optional per request type.

### 4.3 Decision Aggregation
Rules follow this precedence:

1. deny  
2. require_approval  
3. warn  
4. allow  

The Gateway must not forward a request downstream until all policy checks complete.

---

## 5. Human Approval Integration

If aggregated decision = require_approval:

- Gateway must generate an ApprovalRequest.
- Workflow must pause until ApprovalResponse is received.
- Approval is bound to the unique request payload.
- Approvals cannot be reused across requests.
- Approval outcomes must be included in audit logs.

If approval is rejected → request is denied.

---

## 6. Request Routing

### 6.1 Allowed Requests
Forward request to downstream MCP server.
Record downstream response.
Return response to upstream caller.

### 6.2 Warn Requests
Same as allowed, but with mandatory audit annotation.

### 6.3 Denied Requests
Do not forward request.
Return structured MCP error to caller.
Emit audit event.

### 6.4 Approval Requests
Pause, await approval, then either:
- forward (if approved)  
- deny (if rejected)  

Routing logic must be deterministic and auditable.

---

## 7. Response Handling

The Gateway should optionally evaluate responses for:
- hallucination detection (ONNX)
- unsafe content
- violations of policy rules

If configured, a response may also trigger:
- warn  
- block  
- require approval (rare, but possible)  

All response evaluations must be captured in audit logs.

---

## 8. Path Security and Workspace Enforcement

The Gateway must enforce:
- absolute path normalization  
- workspace root restriction  
- prevention of directory traversal  
- prevention of writes outside allowed regions  
- optional read restrictions  

Illegal paths must trigger deny decisions.

Example forbidden paths:
- /etc/passwd  
- ~/.ssh  
- ../../ outside workspace  

Workspaces must be explicitly configured.

---

## 9. Audit Requirements

Each intercepted request must generate an audit event containing:
- request id  
- upstream caller identity  
- action (file.write, tool.invoke, etc.)  
- request payload  
- OPA policy results  
- ONNX evaluation results  
- aggregated decision  
- approval id (if any)  
- downstream response status  
- timestamps  

Audit events must conform to audit-event.schema.json.

---

## 10. Restart Behavior

The Gateway must support restart-safe behavior:

- in-flight approvals must be persisted  
- partially evaluated requests must not slip through  
- cached decisions may be restored (optional)  
- workflow must resume in a safe paused or completed state  

Under no circumstances may the Gateway automatically allow a previously pending operation.

---

## 11. Performance and Scalability Requirements

- Gateway must process requests with minimal latency.
- Parallel requests must be supported (MCP allows concurrency).
- Policy and model evaluation may be cached per request type.
- Downstream MCP server failures must not bypass governance.

---

## 12. Prohibited Behaviors

The Gateway must not:
- allow ungoverned passthrough
- mutate requests silently (except when rewriting is explicitly enabled)
- suppress audit events
- bypass approval flows
- retain secret content in logs
- rely on nondeterministic evaluation logic

---

## 13. Summary

The MCP Gateway is a foundational safety layer in the CabinCrew Protocol. It provides consistent governance, auditing, approval enforcement, and deterministic behavior for all MCP tool interactions. Through its policy-driven and ML-augmented decision engine, it ensures all agent actions remain safe, controlled, and observable.

