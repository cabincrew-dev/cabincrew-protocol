# MCP Integration Guide
Version: draft

This document explains how to integrate **CabinCrew** with **Model Context Protocol (MCP) servers**, including local, remote, authenticated, and proxied setups. CabinCrew provides an **MCP Gateway** that acts as a governance firewall between agents and MCP servers, enforcing policy, controlling file operations, and generating audit logs.

This guide is non‑normative and supplements:
- `spec/draft/mcp-gateway.md`
- `schema/draft/mcp-gateway.schema.json`
- `docs/governance.md`
- `docs/security.md`

---

# 1. What MCP Integration Enables

CabinCrew’s MCP Gateway allows you to:

- Safely expose **file systems**, **retrieval tools**, **API wrappers**, and **custom agent tools**.
- Enforce **OPA policies**, **ONNX model checks**, and **human approvals** on every tool call.
- Prevent unsafe operations (e.g., modifying `.env`, writing outside workspace).
- Filter, normalize, or rewrite requests before they reach MCP servers.
- Produce **audit logs** for every request/response pair.
- Provide **deterministic behavior** around inherently nondeterministic agent ecosystems.

CabinCrew treats MCP servers as **untrusted compute** behind a safety firewall.

---

# 2. Architecture Overview

```
Agent → MCP Client → MCP Gateway → MCP Server
                          ↓
                   Governance Layer
              (OPA + ONNX + Approvals)
```

The Gateway:
- terminates incoming MCP protocol traffic
- evaluates requests against policies
- enforces allow/deny/approval
- forwards safe requests to configured MCP servers
- evaluates responses similarly
- emits audit events

Gateways must run locally or near the orchestrator to maintain strong safety guarantees.

---

# 3. Supported MCP Server Deployment Models

## 3.1 Local MCP Servers
Examples:
- `mcp-file-server`
- `mcp-retrieval-server`
- local git or documentation tools

Gateway launches them as subprocesses or connects via local sockets.

## 3.2 Remote MCP Servers
Examples:
- self-hosted MCP servers
- SaaS MCP services

The Gateway uses secure mTLS or HTTPS endpoints and handles token-based authentication.

## 3.3 Internal Enterprise MCP Servers
Company‑specific MCP tools such as:
- HR data tools
- finance APIs
- internal retrieval indexes

These require stronger policy enforcement and typically require approval workflows.

---

# 4. MCP Gateway Configuration

A minimal MCP Gateway configuration includes:

```
servers:
  files:
    type: file
    root: /workspace
  retrieval:
    type: retrieval
    endpoint: https://example.com/mcp
  custom:
    type: exec
    command: ["./my-mcp-tool"]

governance:
  opa_policies: ./policies/
  onnx_models: ./models/
  decision_priority: strict
```

Important configuration fields:

- **servers**: mapping of labels → MCP server backends  
- **allowed_ops**: whitelist of operations (`readFile`, `writeFile`, `applyPatch`, etc.)  
- **safe_paths**: paths allowed for file operations  
- **patch_rules**: controls for patch size, file types, behaviors  
- **approval_rules**: thresholds that trigger human approval  

---

# 5. Governance Enforcement for MCP

Every MCP request is evaluated via:

### 1. Request Validation
- must match MCP schema  
- must not contain invalid paths or operations  

### 2. OPA Policy Evaluation
OPA receives:
```
{
  "op": "writeFile",
  "path": "/workspace/app/app.py",
  "content": "...",
  "user": "...",
  "workflow": {...},
  "config": {...}
}
```

### 3. ONNX Evaluation (Optional)
Models may detect:
- secrets  
- PII  
- dangerous code patterns  
- high-risk operations  
- file deletions or sensitive modifications  

### 4. Decision Aggregation
`deny` > `require_approval` > `warn` > `allow`

### 5. Enforcement
- **deny** → MCP error to client  
- **require_approval** → workflow pause  
- **warn** → request allowed with audit  
- **allow** → request proceeds  

### 6. Response Validation
Responses go through the same governance pipeline.

---

# 6. File Safety Rules

MCP Gateway enforces strict workspace boundaries:

### Forbidden by Default
- absolute paths outside root  
- relative paths escaping root (`../`)  
- symlink traversal  
- writes to protected files (`.env`, secrets, system files)  

### Patch Validation
Patch metadata is checked for:
- added or deleted line count  
- binary file modification  
- sensitive file types  
- excessive diff size  
- dangerous patterns (e.g., `chmod 777`)  

---

# 7. Local MCP Server Launching

Gateways may launch MCP servers directly:

```
servers:
  file:
    type: exec
    command: ["mcp-file-server", "--root", "/workspace"]
```

The Gateway:
- manages lifecycle  
- restarts crashed servers  
- isolates file operations  
- ensures consistent environment  

This is essential for embedding CabinCrew into agent development flows.

---

# 8. Remote MCP Server Routing

Gateways can proxy to remote MCP servers over HTTP(S):

```
servers:
  api:
    type: remote
    url: https://acme.com/mcp
    headers:
      Authorization: Bearer $TOKEN
```

Remote routing supports:
- request/response transformation  
- authentication injection  
- tenant separation  
- audit isolation  

---

# 9. Authentication & Authorization

The Gateway enforces optional auth between client and gateway:

- API keys  
- JWT/OIDC tokens  
- mTLS client certs  
- per-user RBAC  

Policies can apply different rules per role:

- developers  
- operators  
- agents  
- CI systems  

---

# 10. Approval Integration for MCP Calls

When OPA or ONNX returns `require_approval`:

1. Gateway creates ApprovalRequest  
2. Workflow pauses  
3. Reviewer inspects the MCP request (e.g., patch diff)  
4. Reviewer approves or rejects  
5. Gateway resumes or blocks request  

Approval includes OPA/ONNX reasoning + diff previews.

---

# 11. Audit Events

Every MCP request generates audit trails:

- request payload  
- sanitized diff or content  
- OPA rule outputs  
- ONNX model scores  
- aggregated decision  
- server routing decision  
- response snapshot  

Audit logs must be immutable and timestamped.

---

# 12. Best Practices

### 12.1 Use absolute workspace paths
Avoid ambiguous or relative paths.

### 12.2 Explicitly deny high-risk files
Especially credentials, infra configuration, and build scripts.

### 12.3 Require approvals for production environments
Use `environment` tags in policies.

### 12.4 Enforce diff-size thresholds
Protect against large or unreviewable changes.

### 12.5 Keep ONNX models small
Load time and inference time can impact latency.

### 12.6 Always redact secrets
Both in audit logs and forwarded requests.

---

# 13. Minimal Example: Safe File Workflow

User edits a file using an MCP-aware agent:

```
Agent → modify file
    ↓
MCP Gateway (OPA checks path)
    ↓ allow
File Server returns updated content
    ↓
Agent applies patch
    ↓
MCP Gateway (ONNX scans diff)
    ↓ require_approval
Approval workflow triggers
    ↓
Reviewer approves
    ↓
Patch applied safely
```

---

# 14. Summary

CabinCrew’s MCP Gateway enables:

- safe file operations  
- deterministic agent behavior  
- policy-governed external tool usage  
- full auditability  
- human oversight when needed  

It is the **security firewall** for agent-driven MCP tools, ensuring enterprise-grade safety.

