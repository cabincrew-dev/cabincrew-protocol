# CabinCrew Protocol Architecture
Version: draft

This document describes the architectural model of the CabinCrew Protocol. It provides a system-level view of the components, their responsibilities, and the contracts that govern interactions. It complements the JSON schemas by defining behavior, sequencing, and invariants that schemas alone cannot express.

## 1. Architectural Overview

CabinCrew defines a deterministic, auditable workflow system composed of four major layers:

1. Engines (execution units)
2. Orchestrator (workflow controller)
3. Gateways (policy firewalls)
4. Audit Layer (chain-of-custody recorder)

Each layer is independently deployable and interchangeable, enabling secure and reproducible automation across local, remote, and air‑gapped environments.

## 2. Component Model

### 2.1 Engines
Engines are pure execution units. They accept structured input, operate inside a controlled workspace, and emit artifacts. They never directly interface with users or external systems except through the orchestrator and gateways.

Engine characteristics:
- IO-pure for planning
- Deterministic output
- Explicit artifact generation
- No network write access during flight-plan
- No workspace mutation during flight-plan
- Controlled side effects during take-off only

Engines know nothing about:
- approvals
- policies
- gateways
- tokens
- audit logs

This keeps engines simple, portable, and testable.

---

### 2.2 Orchestrator
The orchestrator is the core state machine of CabinCrew. It is responsible for:

- launching engines in correct modes
- preparing the execution environment
- validating and storing artifacts
- generating and verifying plan-tokens
- running preflight policies
- pausing for human approval when required
- executing take-off operations
- generating audit events for every meaningful transition

Key invariants:
- take-off may only proceed if plan-token integrity is verified
- artifacts may not be modified between plan and apply
- orchestrator must be restart‑safe and deterministic
- all state transitions must produce audit events

---

### 2.3 Gateways

Gateways act as policy‑controlled intermediaries between automation and external systems.

Two gateway types exist:

MCP Gateway:
- intercepts tool calls such as file writes, reads, patches, searches, API tools
- performs OPA and ONNX evaluation
- may warn, deny, allow, or escalate to approval
- can rewrite or sanitize requests before forwarding
- must emit audit events

LLM Gateway:
- intercepts all interactions with LLMs
- may perform prompt rewriting
- may re-route models (load balancing, safety routing)
- performs classification (bias, toxicity, hallucination)
- supports approval flow for high-risk outputs
- must emit audit events

Gateways never bypass governance. Even “allow” decisions must still be auditable.

---

### 2.4 Audit Layer

All components emit structured audit events following audit-event.schema.json.

Audit events provide:
- chain of custody
- forensic traceability
- reproducibility
- evidence for approvals
- risk analysis sources
- debugging and observability

Audit storage is implementation-defined (files, streams, append-only logs, databases).

---

### 3. Dataflow Overview

The high-level dataflow of a workflow looks like this:

1. Orchestrator launches engine in flight-plan mode.
2. Engine emits artifacts into CABINCREW_ARTIFACTS_DIR.
3. Orchestrator generates plan-token from artifacts.
4. Orchestrator performs preflight (OPA, ONNX).
5. Gateway audits all agent or engine tool access.
6. If required, approval flow pauses the workflow.
7. Orchestrator launches engine in take-off mode.
8. Gateways validate all external operations invoked by the engine.
9. Audit layer records events for every step.

This ensures deterministic, governed automation.

---

### 4. Deployment Architecture

CabinCrew components may run in the following configurations:

Local Single-Process:
- orchestrator, engines, gateways run in a single binary
- simplest model for developer workflows

Hybrid:
- orchestrator local
- engines remote (OCI bundles)
- gateways local or distributed

Enterprise:
- orchestrator as a service
- gateways deployed as sidecars, proxies, or network firewalls
- audit logs streamed to centralized storage

Air-Gapped:
- all components offline
- model routing uses only local LLMs
- no external push or writes allowed without approval

---

### 5. Security Architecture

Security principles include:

Separation of Duties:
- engines generate intent
- orchestrator enforces policy
- gateways inspect external calls
- humans approve high-risk operations

Zero Trust:
- no component assumes correctness of another
- every transition is validated by rules or signatures

Integrity Enforcement:
- plan-token binds flight-plan and take-off
- orchestrator ensures immutability of artifacts
- drift detection prevents unsafe execution

Governance Everywhere:
- every action is policy-checked
- every decision is auditable
- every unsafe scenario is escalated

---

### 6. Interoperability

CabinCrew is designed to interoperate with:

- AI code agents
- LLM orchestration frameworks
- MCP servers
- containerized infrastructure tools
- CI/CD systems
- developer workstations
- standalone CLIs

All communication is through defined schemas and artifact formats, ensuring engines and orchestrators from different vendors remain compatible.

---

## Summary

The CabinCrew architecture enforces:

- deterministic automation
- strong governance
- complete auditability
- safe AI-assisted operations
- strict separation of plan and apply
- chain-of-custody guarantees
- extensible enforcement through gateways

This document provides the conceptual foundation. Behavioral rules and detailed contracts appear in the component specifications:

- engine.md
- orchestrator.md
- orchestrator-preflight.md
- orchestrator-approval.md
- artifact.md
- plan-token.md
- mcp-gateway.md
- llm-gateway.md
- audit-event.md
