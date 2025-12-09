# CabinCrew Plan-Token Specification
Version: draft

The plan-token is a cryptographic binding between the intent generated during flight-plan and the actions executed during take-off. It ensures that take-off cannot occur unless the artifacts being applied are exactly those that were reviewed, governed, and approved. This document defines the semantics, structure, and lifecycle of the plan-token.

## 1. Purpose of the Plan-Token

The plan-token guarantees:

- **Integrity**: artifacts cannot be modified between flight-plan and take-off.
- **Authenticity**: the orchestrator can validate that the plan is genuine.
- **Reproducibility**: approved plans are cryptographically tied to take-off.
- **Chain of Custody**: governance and approvals apply to a specific set of artifacts.

Without a valid plan-token, take-off is forbidden.

---

## 2. Plan-Token Structure

The plan-token is a structured JSON document defined in `plan-token.schema.json`.  
It contains:

- token_id  
- workflow_id and step_id  
- a list of artifact hashes  
- a composite hash representing the entire plan  
- timestamp  
- orchestrator identity or signature metadata  
- optional fields for future extensions  

Fields must be explicitly defined; engines cannot generate their own tokens.

---

## 3. Artifact Binding

The token binds to artifacts via:

- artifact metadata hashes  
- integrity hashes of body.data (if present)  
- artifact names and roles  

The orchestrator computes these values in a deterministic order.

Any change to:
- file content  
- metadata fields  
- artifact names  
- roles  
- ordering  

invalidates the token.

---

## 4. Token Generation Rules

Plan-token creation occurs immediately after flight-plan completes.

The Orchestrator must:

1. Collect all artifacts from CABINCREW_ARTIFACTS_DIR.
2. Validate artifact.json files.
3. Compute individual artifact integrity hashes.
4. Build a fixed-order list of artifact descriptors.
5. Compute a composite plan hash.
6. Store the token in persistent workflow state.
7. Emit an audit event.

Engines never generate or modify plan-tokens.

---

## 5. Token Verification Rules

Before take-off:

1. The Orchestrator recomputes all artifact integrity data.
2. It compares computed values with those stored in the token.
3. If mismatched → take-off denied.
4. If matching → workflow continues.

Verification is mandatory.

---

## 6. Interaction With Approvals

The approval workflow binds decisions to a specific plan-token.  
Thus:

- Approval must reference the plan-token hash.
- Orchestrator must verify equality.
- After approval, artifacts cannot change.
- Any artifact modification invalidates approval.

This prevents “approval reuse” attacks.

---

## 7. Restart and Recovery Behavior

After a restart, the orchestrator must:

- reload the saved plan-token  
- re-validate artifacts  
- confirm approval state (if applicable)  
- restart workflow safely  

If plan-token or artifacts are missing or modified, workflow must halt.

---

## 8. Prohibited Behaviors

- Engines must not compute or influence plan-tokens.
- Gateways cannot modify tokens.
- Orchestrator must not regenerate tokens after preflight.
- Artifacts must not be modified after token creation.
- Take-off cannot proceed without matching token.

---

## 9. Token Expiration (Optional Feature)

If implemented by a vendor:

- tokens may optionally expire after a configured duration
- expiration must trigger workflow failure
- expiration events must be logged via the audit system

Expiration is not required by the protocol but may be used for compliance.

---

## 10. Summary

The plan-token enforces a secure chain of custody between intent and execution. By binding artifact integrity to workflow approval and validating it before take-off, CabinCrew ensures deterministic, auditable, and safe automation even in the presence of restarts, partial failures, or malicious engines. It is a cornerstone of the protocol’s safety guarantees.

