# Engine Implementer's Guide
Version: draft

This guide explains how to implement an Engine compatible with the CabinCrew Protocol.  
It is a practical, non-normative manual for developers building engines in any language (Go, Rust, Python, etc.).  
All normative behavior is defined in `spec/draft/engine.md` and validated by `schema/draft/engine.schema.json`.

---

## 1. What Is an Engine?

An Engine is a deterministic executable that:

- runs in **flight-plan** mode to compute intent  
- runs in **take-off** mode to apply validated intent  
- operates only inside the directories provided via environment variables  
- emits artifacts describing the results of its operations  
- returns a structured JSON “receipt” to STDOUT  

An Engine **does not** perform governance, approvals, or policy evaluation.  
Those are performed upstream in the Orchestrator and Gateways.

---

## 2. Execution Environment

The Orchestrator launches an Engine with these environment variables:

### **CABINCREW_WORKSPACE**
A directory representing the project root (e.g., a Git repo or workspace).

### **CABINCREW_ARTIFACTS_DIR**
A secure, empty directory where the Engine must write output artifacts.

### **CABINCREW_TEMP_DIR**
Ephemeral scratch space for temporary files.

The Engine must treat all other directories as out of bounds unless explicitly allowed.

---

## 3. Input Format

The Engine receives a structured JSON object via STDIN or an input file (same structure):

```
{
  "meta": {
    "workflow_id": "...",
    "step_id": "...",
    "mode": "flight-plan" | "take-off"
  },
  "config": { ... },
  "secrets": { ... },
  "context": { ... }
}
```

Important notes:

- `mode` determines execution behavior.
- `secrets` are only those mapped by the user; engines must not request additional secrets.
- Engines must remain deterministic given the same input and workspace state.

---

## 4. Output Format (Receipt)

All Engines write a JSON receipt to STDOUT:

```
{
  "status": "success" | "failure",
  "error": "...",
  "artifacts": [ ... ],
  "metrics": [ ... ]
}
```

### Status rules:
- In `flight-plan`, failures stop the workflow immediately.
- In `take-off`, failures produce audit events and halt the workflow.

Engines should keep receipts minimal and machine-readable.

---

## 5. Artifact Structure

Artifacts represent the results of an Engine step.

Each artifact has:

- **metadata** in `artifact.json`  
- optional **body file** (e.g., diff, binary blob, rendered manifest)

Artifacts reside in:

```
CABINCREW_ARTIFACTS_DIR/<artifact-name>/
    artifact.json
    body.data   (optional)
```

The metadata.json must include:

- `name`
- `type`
- `action`
- `parameters`
- integrity `hashes`

The Orchestrator will later validate these fields.

---

## 6. Flight-Plan Mode

### Responsibilities:
- Inspect workspace state  
- Generate intent artifacts  
- Produce diffs, manifests, plans, summaries, metadata  

### Required behaviors:
- **No side effects outside artifacts directory**
- **Workspace must remain unchanged (“Clean Campsite Rule”)**
- **Artifacts must be reproducible**

Examples of flight-plan outputs:
- Terraform plan  
- Git diff  
- Rendered Kubernetes manifests  
- JSON describing actions to take  
- Safety hints for reviewers  

Artifacts from this phase become the basis of the `plan-token`.

---

## 7. Take-Off Mode

### Responsibilities:
- Read artifacts produced during flight-plan  
- Execute side effects deterministically  
- Honor parameters and intent exactly as planned  

Take-off must refuse to execute if:
- required state artifacts are missing  
- parameters are invalid  
- integrity hashes do not match  
- body files are missing or corrupted  

The Orchestrator will perform its own validation before launching take-off.

---

## 8. Design Requirements for Engines

### **Determinism**
Same input = same output.

### **Isolation**
Do not write outside workspace or artifact directories.

### **Reproducibility**
Do not generate nondeterministic data unless required (timestamps must be avoided in artifacts).

### **Transparency**
Keep artifacts human-auditable when possible (diff, manifest, structured metadata).

### **Idempotence**
Take-off should not perform destructive or repeated side-effects unless explicitly part of intended behavior.

---

## 9. Best Practices

### 9.1 Keep artifacts small and readable
Prefer textual artifacts (JSON, diff, YAML) unless binary formats are required.

### 9.2 Separate logic clearly
- Planning = analysis + artifact creation  
- Execution = applying planned state  

### 9.3 Emit helpful metrics
Examples:
- number of files changed  
- number of resources modified  
- risk indicators  
- timing data  

### 9.4 Fail loudly and clearly
Do not hide partial failures.

---

## 10. Testing Engines

### Recommended approach:
- snapshot-based tests for artifact outputs  
- golden files for receipts  
- workspace fixtures  
- integrity hash verification tests  
- compatibility tests against schemas  

### CI Recommendations:
- JSON schema validation  
- reproducibility checks  
- deterministic sorting tests  

---

## 11. Engine Examples (Coming Soon)

This repository will provide:
- a minimal “Hello World” engine
- an engine that renders diffs
- a Terraform-like engine example
- an engine that generates structured API actions
- language-specific templates (Go, Rust, Python)

---

## 12. Summary

This guide provides practical steps for implementing Engines that comply with the CabinCrew Protocol. Engines are intentionally simple: they compute intent, generate structured artifacts, and execute validated actions. Governance and safety are handled elsewhere.

For complete normative details, refer to:

- `spec/draft/engine.md`
- `schema/draft/engine.schema.json`

