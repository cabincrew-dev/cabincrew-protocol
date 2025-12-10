# AI Agent Manifesto Compliance

The **Cabin Crew Protocol** is the Reference Implementation for the [AI Agent Manifesto](https://aiagentmanifesto.org).

This document details how the protocol strictly adheres to the 5 Immutable Laws + the Capability Isolation principle.

## 1. The Principle of Separation
> "Reasoning must be separate from action. Intent must be decoupled from Execution."

**Implementation**:
- **Flight Plan Mode**: Engines generate a plan (`PlanToken`) in `flight-plan` mode. No state changes occur.
- **Take-Off Mode**: Execution happens only in `take-off` mode, which mandates a valid `PlanToken`.
- **Preflight Check**: The Orchestrator validates the plan before authorizing execution.

## 2. The Principle of Provenance
> "Every output must carry its creation story... cryptographic link between the agent's identity, the input context, the model used, and the final output."

**Implementation**:
- **PlanToken**: Contains `workspace_hash`, `model` (e.g. `gpt-4`), `engine_id`, and `protocol_version`.
- **Binding**: This token is cryptographically bound to the artifacts it produced.

## 3. The Principle of External Sovereignty
> "No agent can be its own authority. Safety guardrails must exist outside the agent's cognitive loop."

**Implementation**:
- **Gateways**: `LLMGateway` and `MCPGateway` wrap all external calls, enforcing policy (rate limits, DLP) outside the engine logic.
- **Orchestrator Veto**: The Orchestrator can deny a `PreflightOutput` regardless of the Engine's confidence.

## 4. The Principle of Immutable Evidence
> "Logs must be proofs, not just text."

**Implementation**:
- **Signatures**: `AuditEvent` includes a cryptographic `signature` field.
- **Hash Chain**: `AuditEvent` supports `chain_hash` for ledger-style non-repudiation.

## 5. The Principle of Ephemeral Identity
> "Static keys are a failure of architecture."

**Implementation**:
- **Identity Tokens**: The protocol supports `identity_token` (OIDC/JWT) in `EngineInput` for short-lived, verifiable workload identity.

## 6. The Principle of Capability Isolation (Draft)
> "Agents must not simultaneously process untrusted input, access sensitive systems, and perform state-changing operations... external supervision is mandatory."

**Implementation**:
- **Human-in-the-Loop**: Explicit support via:
    - `PreflightOutput.decision: 'REQUIRE_APPROVAL'`
    - `WorkflowState: 'WAITING_APPROVAL'`
    - `ApprovalRequest` / `ApprovalResponse` structures.
