# CabinCrew Artifact Specification
Version: draft

Artifacts are the core representation of intent within the CabinCrew Protocol. Engines do not directly apply changes during flight-plan; instead, they emit artifacts describing all intended actions. The Orchestrator validates, governs, and later uses these artifacts during take-off. This document defines the structure, semantics, and behavioral requirements of artifacts.

## 1. Purpose of Artifacts

Artifacts provide a universal, structured way to represent:

- proposed modifications (files, configs, code, infrastructure)
- state passed between flight-plan and take-off
- evidence for governance and audit
- machine-readable descriptions of intent
- immutable inputs to take-off execution

Artifacts ensure reproducibility, auditability, and safe review of intended changes.

---

## 2. Artifact Directory Structure

Each artifact is stored under:

```
CABINCREW_ARTIFACTS_DIR/<artifact_name>/
    artifact.json
    body.data (optional)
```

Rules:
- `<artifact_name>` must be unique within a workflow step.
- `artifact.json` contains structured metadata.
- `body.data` stores raw content when applicable (diff, patch, blob, script, model output, etc.).

Engines must not write artifacts outside this directory.

---

## 3. artifact.json Structure

The artifact.json file must conform to artifact.schema.json. It includes:

- `type`  
  Free-form descriptor identifying the artifact category (e.g., “file_patch”, “git_diff”, “config_change”, “structured_plan”).

- `action`  
  Describes the intended operation (e.g., “create”, “update”, “delete”, “apply”, “execute”).  
  These are not strict enums—implementations may define new actions.

- `metadata`  
  Arbitrary structured metadata describing the artifact (paths, versions, timestamps, user-defined fields).

- `body_file`  
  Points to body.data if present.

- `integrity`  
  Contains hash of body.data (if applicable), enabling plan-token verification.

Artifact types and actions intentionally remain open to allow extensibility.

---

## 4. Artifact Roles

Each artifact must declare a role:

- **evidence**  
  Provides information for decision-making (e.g., diffs, plans, reports).

- **state**  
  Required for restoring or resuming during take-off (e.g., terraform plan.out, git bundle).

- **log**  
  Debugging or tracing information not evaluated by governance rules.

The Orchestrator treats each role differently during workflow transitions.

---

## 5. Artifact Integrity

Engines must compute integrity hashes when body.data exists.  
The Orchestrator must:

- verify integrity before take-off  
- include integrity values in plan-token calculations  
- treat mismatches as critical errors

Artifacts are immutable once written.

---

## 6. Artifact Semantics

Artifacts must describe desired actions abstractly. Examples:

### File modification:
- type: file_patch  
- action: update  
- metadata: path, line ranges  
- body.data: patch content

### Infrastructure change:
- type: infra_plan  
- action: apply  
- metadata: resources, deltas  
- body.data: plan file

### Code transformation:
- type: code_diff  
- action: update  
- metadata: language, formatter  
- body.data: diff or patch

### Execution request:
- type: script  
- action: execute  
- metadata: interpreter, args  
- body.data: command body

These examples do not define strict enums; engines may define their own formats.

---

## 7. Artifact Validation

The Orchestrator must ensure:

- artifact.json is valid JSON
- it conforms to artifact.schema.json
- referenced body.data exists when required
- metadata is complete enough for governance evaluation
- no prohibited fields exist
- no undeclared external state is referenced
- artifact names are unique

Failure to validate causes workflow termination.

---

## 8. Artifacts in Flight-Plan vs Take-Off

### During Flight-Plan:
- artifacts describe proposed changes
- engines must not perform side effects
- artifacts define future actions only

### During Take-Off:
- artifacts serve as the authoritative source of truth
- engines must not modify or regenerate artifacts
- Orchestrator ensures plan-token integrity before execution

Artifacts represent immutable intent.

---

## 9. Artifact Influence on Governance

Governance systems (OPA and ONNX) rely entirely on artifacts.  
Artifacts provide:

- semantic information for policy rules  
- contextual metadata for risk assessment  
- content for ML-based classification  
- consistent inputs for audit analysis

OPA policies may examine:
- metadata fields
- content hashes
- body content (if safe and allowed)
- dependencies between artifacts

ONNX models may evaluate:
- file content
- code patterns
- natural language outputs
- structural properties

Artifacts must be rich enough to enable meaningful governance.

---

## 10. Artifact Lifecycle

1. **Creation**  
   Engine writes artifacts during flight-plan.

2. **Validation**  
   Orchestrator checks structure and integrity.

3. **Plan-Token Binding**  
   Orchestrator includes artifact metadata hashes.

4. **Governance**  
   OPA/ONNX evaluate artifacts.

5. **Approval (optional)**  
   Humans review artifact summaries.

6. **Take-Off Execution**  
   Artifacts are consumed without modification.

7. **Audit Storage**  
   Artifact metadata and hashes recorded in audit logs.

Artifacts must not be changed after step 1.

---

## 11. Prohibited Behaviors

Engines must not:
- mutate artifacts after writing them
- embed undeclared side effects in artifacts
- store secrets in artifact body data
- output different structures across runs

The Orchestrator must not:
- accept modified artifacts during take-off
- skip artifact validation
- allow take-off without matching plan-token

---

## 12. Summary

Artifacts are the foundational unit of intent, evidence, and state in the CabinCrew Protocol. They enable safe automation by separating intent from execution, supporting governance, enforcing integrity, and enabling reproducibility. Engines describe changes; artifacts make them explicit; the Orchestrator validates and applies them safely.

