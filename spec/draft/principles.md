# CabinCrew Protocol Design Principles
Version: draft

This document defines the normative design principles that guide all CabinCrew Protocol implementations. These principles ensure security, auditability, and deterministic behavior across orchestrators, engines, and gateways.

## 1. Immutability

**Principle**: Once created, protocol artifacts (plan-tokens, audit events, artifacts) must never be modified.

**Requirements**:
- Plan-tokens are cryptographically bound to their artifacts
- Audit events are append-only with chain hashes
- Artifacts are identified by content-addressable SHA256 hashes
- Approvals are bound to specific plan-token hashes

**Rationale**: Immutability enables cryptographic verification, prevents tampering, and supports deterministic replay.

## 2. Determinism

**Principle**: Given the same inputs, protocol operations must produce identical outputs.

**Requirements**:
- Engines must be deterministic in flight-plan mode
- Timestamps must be normalized or externally provided
- Random numbers require fixed seeds
- Network responses must be cached or mocked
- Artifact generation must be reproducible

**Rationale**: Determinism enables verification, testing, and multi-orchestrator consensus.

## 3. Least Privilege

**Principle**: Components receive only the minimum permissions necessary for their function.

**Requirements**:
- Engines run in sandboxed environments
- Engines cannot access gateways directly
- Engines receive only explicitly mapped secrets
- Gateways enforce policy before allowing LLM/MCP access
- Orchestrators validate all engine outputs

**Rationale**: Least privilege limits blast radius and prevents privilege escalation.

## 4. Explicit Over Implicit

**Principle**: All behavior must be explicitly declared, not inferred.

**Requirements**:
- Engines declare artifacts in receipts
- Workflows explicitly map secrets
- Policy decisions are recorded with evidence
- Approvals reference specific plan-token hashes
- Gateways log all requests and decisions

**Rationale**: Explicit behavior enables auditability and prevents hidden side effects.

## 5. Separation of Concerns

**Principle**: Policy, execution, and approval are strictly separated.

**Requirements**:
- Engines implement logic, not policy
- Gateways enforce policy, not execution
- Orchestrators coordinate, not decide
- Humans approve, not implement

**Rationale**: Separation enables independent verification and prevents conflation of responsibilities.

## 6. Verifiability

**Principle**: All protocol operations must be cryptographically verifiable.

**Requirements**:
- Plan-tokens bind artifacts with SHA256 hashes
- Audit events chain with cryptographic hashes
- Approvals are signed and timestamped
- Artifacts are content-addressable
- Integrity checks detect tampering

**Rationale**: Verifiability enables trust, compliance, and forensic analysis.

## 7. Auditability

**Principle**: All protocol operations must produce immutable audit trails.

**Requirements**:
- Every decision is logged with evidence
- Policy evaluations record source and aggregation
- Workflow state transitions are recorded in WAL
- Approvals track who, what, when, and why
- Audit events include workflow state context

**Rationale**: Auditability enables compliance, debugging, and accountability.

## 8. Fail-Safe Defaults

**Principle**: In the absence of explicit permission, deny.

**Requirements**:
- Default gateway decision is `deny`
- Missing approvals block execution
- Invalid plan-tokens fail validation
- Unsigned artifacts are rejected
- Unknown policy sources are denied

**Rationale**: Fail-safe defaults prevent accidental authorization.

## 9. Defense in Depth

**Principle**: Multiple independent security layers protect against failures.

**Requirements**:
- Pre-flight checks before execution
- Gateway policies before LLM/MCP access
- Plan-token validation before take-off
- Approval binding to plan-token hashes
- Integrity checks after execution

**Rationale**: Defense in depth ensures no single point of failure.

## 10. Restart Safety

**Principle**: Workflows must resume deterministically after crashes.

**Requirements**:
- WorkflowStateRecord persists all critical state
- WAL entries enable deterministic replay
- Approvals survive orchestrator restarts
- Artifacts are durable and verifiable
- Policy evaluations are idempotent

**Rationale**: Restart safety enables reliability and multi-orchestrator deployments.

## 11. Capability Isolation

**Principle**: Components cannot access capabilities they don't need.

**Requirements**:
- Engines cannot call LLMs directly
- Engines cannot access MCP servers directly
- Gateways mediate all external access
- Orchestrators control all capabilities
- Secrets are explicitly mapped, never ambient

**Rationale**: Capability isolation prevents unauthorized access and lateral movement.

## 12. Chain of Custody

**Principle**: Every decision must be traceable to its source.

**Requirements**:
- Policy evaluations record source (OPA/ONNX/gateway)
- Aggregation methods are documented
- Workflow state is captured in audit events
- Approvals reference specific evidence
- Timestamps establish temporal ordering

**Rationale**: Chain of custody enables forensic analysis and compliance verification.

## Summary

These principles form the foundation of the CabinCrew Protocol. Implementations that violate these principles compromise security, auditability, or determinism. When in doubt, favor explicitness, immutability, and verifiability.
