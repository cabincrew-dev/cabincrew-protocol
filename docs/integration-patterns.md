# CabinCrew Integration Patterns
Version: draft

This document provides practical patterns for integrating CabinCrew into real systems, including CI/CD, Git workflows, multi-agent pipelines, enterprise environments, and air‑gapped deployments.  
It is non‑normative and supplements the orchestration, gateway, and governance specifications.

---

# 1. Overview

CabinCrew integrates into environments where deterministic, safe, governed automation is required.  
These patterns show how to combine Engines, Gateways, LLMs, and governance to build reliable AI‑assisted workflows.

Integration patterns covered:

1. CI/CD Integration  
2. Git Push / PR Automation  
3. Agent Workflow Integration  
4. Multi‑Agent Pipelines  
5. Infrastructure Automation  
6. Enterprise Environments  
7. Air‑Gapped Deployments  
8. Event‑Driven Triggering  
9. Multi‑Model LLM Routing  
10. Secrets & Credential Boundaries  

---

# 2. CI/CD Integration Pattern

CI/CD is the simplest and most common integration target.

## 2.1 Setup
- Orchestrator runs inside CI pipeline  
- Engine binaries installed or pulled from OCI  
- Gateways run locally via sidecar containers  

## 2.2 Flow
1. Checkout repo  
2. Trigger CabinCrew workflow  
3. Engine runs `flight-plan` to compute intent  
4. Preflight policies evaluate diffs/manifests  
5. Approval requested if required  
6. Upon approval, `take-off` applies changes  
7. Audit logs exported  
8. CI marks job success/failure  

## 2.3 Benefits
- deterministic builds  
- compliance‑ready change pipelines  
- safety enforced before deployment  

---

# 3. Git Push / Pull Request Automation

CabinCrew can act as a **code‑change gatekeeper**.

## Pattern: PR Auto‑Review
1. Developer pushes branch  
2. CabinCrew runs Engine to compute diffs  
3. LLM Gateway summarizes intent safely  
4. Approval triggered if changes large or risky  
5. Approved flow updates PR or runs CI test suite  

## Pattern: Safe Auto‑Merge
Only allow merges when:
- plan-token matches  
- all approvals completed  
- policies allow execution  

---

# 4. Agent Workflow Integration

CabinCrew acts as a safety layer for autonomous or semi‑autonomous agents.

## 4.1 Agent Editing Files
```
Agent → MCP Gateway → Safe file operations
```

## 4.2 Agent Planning Changes
Agent produces:
- plan proposals  
- manifest updates  
- transformation suggestions  

All must be approved via workflows.

## 4.3 Agent Writing Code
CabinCrew blocks:
- unsafe patches  
- secrets in patches  
- mass deletions  
- rewriting critical infra files  

---

# 5. Multi‑Agent Pipelines

Multiple agents may collaborate (planner / executor / reviewer).  
CabinCrew ensures coordination via:

- workflow context  
- plan-token locking  
- agent identity in audit events  
- deterministic sequencing  

## Example:
```
Planner Agent → flight-plan stage  
Reviewer Agent → governance stage  
Executor Agent → take-off stage  
```

Each step is governed and audited.

---

# 6. Infrastructure Automation Pattern

CabinCrew is ideal for Terraform / Kubernetes / IaC flows.

## 6.1 Terraform‑Like Flow
1. Engine generates plan artifacts  
2. Preflight checks for drift, risk, blast radius  
3. Approval for prod changes  
4. Engine applies via take-off  
5. Audit logs stored  

## 6.2 Kubernetes Automation
- LLM proposes manifest changes  
- MCP Gateway validates file edits  
- Engine builds diffs  
- Approvals required for pod/security changes  

---

# 7. Enterprise Integration Pattern

Enterprises require:

- multi‑tenant isolation  
- RBAC approval routing  
- central policy bundles  
- unified audit sinks  
- identity propagation  

## Pattern: Enterprise Gateway Mesh
CabinCrew Gateways run:
- per-department  
- per-environment  
- per-service boundary  

Audit events flow to central SIEM.

---

# 8. Air‑Gapped Deployment Pattern

CabinCrew supports fully offline use.

## Requirements:
- local LLM models (ONNX or GGUF)  
- internal MCP servers  
- internal policy bundles  
- Engines packaged via OCI  

## Flow:
1. Local Orchestrator  
2. Local gateways  
3. Offline LLM router  
4. Offline approval tooling  
5. Local-only audit logs  

Perfect for security‑critical environments.

---

# 9. Event‑Driven Triggering

CabinCrew workflows can be triggered via:

- Webhooks  
- Git events  
- Cron schedules  
- Ops alerts  
- ChatOps commands  
- External automation platforms  

Example:
```
New dependency vulnerability → trigger engine to propose fix → approval → apply
```

---

# 10. Multi‑Model LLM Routing Pattern

CabinCrew supports advanced routing use cases.

## Examples:
- “Unsafe prompts go to safe-tier model”  
- “Large completions use cheaper model”  
- “Summaries → small model; planning → high‑accuracy model”  
- “Fallback if primary fails or unsafe”  

All decisions must be auditable.

---

# 11. Secret & Credential Boundaries

CabinCrew ensures:
- LLMs never receive secrets  
- Agents cannot write secrets to files  
- MCP Gateway blocks unsafe file writes  
- Orchestrator redacts secrets before audit  
- ONNX models detect leakage risks  

Secrets must only exist in `secrets` section of engine input.

---

# 12. Combined Pattern: Full AI DevOps Pipeline

```
LLM Agent proposes code → MCP Gateway validates → Engine computes diff → 
Preflight governance → Approval → Engine take-off → CI tests → Deployment
```

This pattern is ideal for:
- automated refactoring  
- dependency upgrades  
- config editing  
- orchestrated infra changes  

---

# 13. Summary

CabinCrew integrates well into:

- CI/CD  
- GitOps  
- multi-agent pipelines  
- enterprise automation  
- infra-as-code flows  
- air‑gapped environments  

Integration patterns emphasize:
- determinism  
- governance  
- safety  
- auditability  
- structured automation  

Use these patterns as blueprints to embed CabinCrew into any modern automated workflow.

