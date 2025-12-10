# CabinCrew Engine Specification
Version: draft

This document defines the normative behavior of Engines within the CabinCrew Protocol. Engines are deterministic execution units responsible for producing intent (flight-plan) and applying changes (take-off). They operate in controlled environments and communicate exclusively through structured inputs, outputs, and artifacts.

## 1. Engine Purpose

Engines implement domain-specific logic for computing and applying changes. Examples include:
- git operations
- code modifications
- infrastructure provisioning
- configuration updates
- analysis and transformation tools

Engines must not embed policy, approval logic, gateway behavior, or governance rules.

## 2. Engine Execution Modes

Engines support two mandatory execution modes:

### 2.1 Flight-Plan Mode
Purpose: compute intent without performing side effects.

Requirements:
- no workspace mutation
- no external system mutation
- operations must be deterministic
- read-only network allowed if applicable
- emits artifacts and optional state
- produces a receipt on stdout
- must exit non-zero on validation failure

### 2.2 Take-Off Mode
Purpose: apply validated side effects.

Requirements:
- may modify workspace
- may perform external operations (e.g., git push)
- must restore state from state artifacts if needed
- must not regenerate artifacts
- must rely on orchestrator for plan-token validation
- must produce a receipt on stdout

## 3. Engine Environment

Environment variables set by Orchestrator:

- CABINCREW_WORKSPACE  
- CABINCREW_ARTIFACTS_DIR  
- CABINCREW_TEMP_DIR  
- CABINCREW_MODE  

Engines must not depend on any undocumented environment variable or implicit runtime state.

## 4. Engine Input Format

Engines accept input via:
- STDIN (primary method)
- or a file specified via CABINCREW_INPUT_FILE

Input includes:
- meta information (workflow step, mode)
- config from workflow definition
- explicitly mapped secrets
- context passed from previous steps

## 5. Engine Output Format

Engine output is written to:
- STDOUT (receipt)
- CABINCREW_ARTIFACTS_DIR (artifacts and metadata)

The receipt contains:
- status (success or failure)
- error message (if any)
- list of produced artifacts
- diagnostic metrics

## 6. Artifact Generation Rules

Engines must generate artifacts in the following directory structure:

```
CABINCREW_ARTIFACTS_DIR/<artifact_name>/
    artifact.json
    body.data (optional)
```

Artifacts represent:
- what changed
- how it changed
- metadata for reproducing or applying the change

## 7. Determinism Requirements

Forbidden nondeterminism:
- timestamps without normalization
- random numbers without fixed seeds
- unpredictable network responses
- OS entropy leaks

## 8. Security Requirements

The engine is not trusted. The orchestrator enforces:
- sandboxing
- workspace immutability
- network restrictions
- artifact validation
- plan-token validation

Engines must avoid:
- unsafe shell execution
- unvalidated external input
- leaking secrets

## 9. Exit Codes

0 — successful execution  
1 — engine-level failure  
2 — validation failure  
>2 — reserved for future protocol use  

## 10. Logging

STDOUT: structured EngineOutput JSON only  
STDERR: human-readable logs  

## 11. Resume and Restart Semantics

Engines must not assume:
- state persistence
- temp dir persistence
- workflow execution continuity

Take-off mode may rely on restored state artifacts.

## 12. Prohibited Behaviors

Engines must not:
- talk to gateways directly
- mutate workspace during flight-plan
- produce undeclared side effects
- embed approval logic
- leak secrets

## 13. Summary

Engines are deterministic, stateless, verifiable executables that generate intent and apply validated changes. All behavior must be explicit, auditable, and artifact-driven.
