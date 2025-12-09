# Pre-Flight Specification (Draft)

Pre-Flight is the **governance checkpoint** of the CabinCrew Protocol.  
It validates whether a workflow is safe to continue from:

- `flight-plan → take-off`, or  
- direct → `take-off` (when no plan exists).

Pre-Flight combines **deterministic rule evaluation** (OPA) with **semantic inspection** (ONNX models) to produce a **unified decision**:

```
ALLOW | WARN | REQUIRE_APPROVAL | DENY
```

The Orchestrator MUST run Pre-Flight **after every flight-plan** and **before every take-off** unless explicitly disabled in configuration.

---

# 1. Inputs to Pre-Flight

The Orchestrator constructs a **PreflightInput** packet containing:

### 1.1 Metadata
- `workflow_id`
- `step_id`
- `mode` (`flight-plan` or `take-off`)
- execution context (opaque, engine-dependent)

### 1.2 Engine Output (Raw Receipt)
The full `EngineOutput` object emitted to STDOUT.

### 1.3 Evidence Artifacts
A filtered subset of artifacts where:

```
artifact.role == "evidence"
```

Each must include:

- `name`
- `path`
- `hash` (SHA256)
- MIME type (optional)

### 1.4 Context
Derived from previous workflow steps.

### 1.5 Policy Configuration
Includes:
- enabled OPA modules  
- enabled ONNX models  
- threshold values  
- stage-specific rules (plan vs takeoff)

**No secrets** may be included in Pre-Flight input.

---

# 2. Pre-Flight Processing Pipeline

Pre-Flight is split into three phases:

```
Normalize → Evaluate Policies → Merge Decisions
```

## 2.1 Normalize Inputs

The Orchestrator MUST validate:

### A. Artifact violations
- Evidence artifacts must not exceed size limits.
- Evidence hashes must match files in `ARTIFACTS_DIR`.
- Only evidence artifacts may be passed to policy engines.

### B. Sandbox invariants
- Engine must not modify workspace during `flight-plan`.
- Engine may modify workspace during `take-off`, but only inside workspace root.
- Engine must only write artifacts inside `ARTIFACTS_DIR`.

### C. Structural validation
- `EngineOutput` must conform to schema.
- Artifact roles must be one of: `evidence | state | log`.

If normalization fails → decision = `DENY`.

---

## 2.2 Evaluate OPA Policies

OPA receives:

- metadata  
- evidence artifacts  
- selected engine-output fields  

OPA **must not** receive:

- secrets  
- logs  
- state artifacts  

OPA outputs:

```
allow: bool
warnings: [string]
violations: [string]
require_approval: bool
```

OPA is **deterministic** and must not depend on external network calls.

---

## 2.3 Evaluate ONNX Models

ONNX models receive:

- textual evidence  
- structured evidence (JSON) when safe  

ONNX MUST NOT receive:

- secrets  
- binary state artifacts  
- log files containing stack traces  

ONNX outputs:

```
scores: {
    "<model_name>": float
}
classes: {
    "<model_name>": "<label>"
}
```

The Orchestrator interprets scores according to configuration thresholds.

---

# 3. Policy Decision Merging

The Orchestrator merges OPA and ONNX results into a single canonical structure:

```
decision: ALLOW | WARN | REQUIRE_APPROVAL | DENY
warnings: [...]
violations: [...]
requires: { role, reason } (optional)
```

### Priority Rules

1. **DENY dominates everything**  
2. **REQUIRE_APPROVAL dominates WARN/ALLOW**  
3. **WARN dominates ALLOW**

### Merging Algorithm (Simplified)

```
if violations.nonempty → DENY
if require_approval == true → REQUIRE_APPROVAL
if warnings.nonempty → WARN
else → ALLOW
```

Custom merger logic MAY be defined in future versions.

---

# 4. Pre-Flight Output

Pre-Flight produces a `PreflightOutput` containing:

- `decision`
- `warnings`
- `violations`
- `requires` (if decision = REQUIRE_APPROVAL)

This is recorded in audit logs.

Decision → workflow transitions:

| Decision | Next State |
|----------|------------|
| ALLOW | TAKEOFF_RUNNING |
| WARN | TAKEOFF_RUNNING |
| REQUIRE_APPROVAL | WAITING_APPROVAL |
| DENY | FAILED |

---

# 5. Invariants

The Orchestrator MUST enforce:

### 5.1 Workspace Purity During Flight-Plan
Engines MUST NOT mutate workspace during flight-plan.

### 5.2 Evidence-Only Governance
Only artifacts with `role = evidence` may affect governance.

### 5.3 No Hidden Inputs
Pre-Flight must only consume inputs declared in schema.

### 5.4 Model Safety Boundary
ONNX models MUST operate without backchannels or embedded external calls.

### 5.5 Reproducibility
Given:
- the same engine input  
- the same evidence artifacts  

Pre-Flight MUST produce the same decision (OPA only; ONNX scores may vary but must remain within acceptable bounds).

---

# 6. Failure Conditions

Pre-Flight MUST produce a `DENY` decision if:

- Evidence hashes mismatch.
- Workspace mutation is detected during flight-plan.
- Engine output fails schema validation.
- Policy evaluation fails to execute.
- ONNX scores exceed configured safety thresholds.
- OPA violations are returned.
- Artifact roles are invalid.

---

# 7. Security Model

- No secrets may enter Pre-Flight.
- No logs may influence decisions.
- Pre-Flight must not write to disk except temporary evaluation state.
- All policy code is untrusted → must run in a secure sandbox.
- All Pre-Flight results must be included in the audit log.

---

# 8. Compatibility Requirements

The orchestrator MUST embed:

```
protocol_version = "2025-02-01-draft"
```

Pre-Flight MUST reject incompatible EngineOutput versions.

---

# End of Pre-Flight Specification (Draft)
