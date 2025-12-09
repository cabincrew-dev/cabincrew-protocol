# CabinCrew LLM Gateway Specification
Version: draft

The LLM Gateway is a governance and safety firewall that mediates all interactions with Large Language Models. It enforces deterministic control, policy evaluation, auditing, optional approval workflows, and model routing. This ensures that LLM-generated content—whether used by agents, engines, or orchestrators—remains safe, compliant, and predictable.

## 1. Purpose of the LLM Gateway

The LLM Gateway provides:

- **Safety filtering** using OPA and ONNX
- **Model routing** for load-balancing, fallback, or safety tiers
- **Prompt rewriting** (optional)
- **Guardrails for high-risk outputs**
- **Audit logging for all requests and responses**
- **Human approval for escalated risk scenarios**

The Gateway sits between callers and any LLM provider (local or remote).

---

## 2. Position in the CabinCrew Architecture

The LLM Gateway sits between:

- **Upstream caller** (agent, orchestrator, or engine wrapper)
- **Downstream LLM provider** (API or local model)

Every LLM request must pass through the Gateway.

Requests may include:
- prompt completions
- chat interactions
- embeddings
- code generation
- structured tool call suggestions
- multi-model ensemble decisions

The Gateway must never be bypassed.

---

## 3. Intercepted Operations

At minimum, the Gateway governs:

1. `generate` (text/chat generation)
2. `embed` (embedding creation)
3. `rerank` (if supported)
4. `tool_selection` or `tool_suggestion` (if exposed)
5. `multi_model_route` (optional routing system)

All requests follow the same governance pipeline.

---

## 4. Model Routing

The Gateway may route requests to different models based on:

- safety classification
- model availability or rate limits
- latency constraints
- confidence scoring
- organizational rules

Routing strategies may include:

- **round-robin**
- **weighted routing**
- **safety-tier routing** (primary → fallback → safe-mode model)
- **cost-optimized routing**
- **context-sensitive routing** (e.g., dangerous prompts → safer models)

Routing decisions must be auditable.

---

## 5. Policy Evaluation Pipeline

Each LLM request passes through the following steps:

### 5.1 OPA Policy Evaluation

OPA rules may inspect:

- prompt content
- user metadata and roles
- workflow context
- model selection
- generated intermediate reasoning (if visible)
- rate-limit or compliance rules

OPA results:
- allow  
- warn  
- deny  
- require_approval  

### 5.2 ONNX Model Evaluation

Common ML-based checks include:

- bias detection  
- toxicity / hate speech  
- self-harm indicators  
- hallucination risk  
- insecure code patterns  
- leakage of secrets or credentials  

Models may evaluate:
- the prompt  
- the generated output  
- both  

Results follow the same four decision classes.

### 5.3 Aggregation of Decisions

Final outcome priority:
1. deny  
2. require_approval  
3. warn  
4. allow  

The Gateway must apply this to both request and response evaluation.

---

## 6. Human Approval Integration

If a request or response requires approval:

- An **ApprovalRequest** is generated (bound to request payload).
- The Gateway enters paused state.
- A human reviewer inspects the prompt and/or generated text.
- An **ApprovalResponse** resumes or terminates the workflow.

Approval must:
- reference the unique request id  
- include the LLM content snapshot  
- be bound to the same request hash  

Replays or mismatches must be rejected.

---

## 7. Optional Prompt Rewriting

The Gateway may rewrite prompts to:

- insert safety instructions
- remove sensitive content
- enforce deterministic formatting
- constrain output structure
- add trace metadata

Rewriting must be:
- explicitly configurable
- auditable
- included in governance logs

Callers must receive both the original and rewritten prompt in the audit event.

---

## 8. Response Handling and Post-Generation Governance

The Gateway should evaluate responses using:

- OPA policy rules  
- ONNX classifiers  
- output transformations (optional)  

If unsafe content is detected, the Gateway may:

- block the response  
- require approval  
- regenerate with a safer model  
- redact unsafe segments  

All decisions must be captured in audit logs.

---

## 9. Audit Requirements

Every LLM request and response must produce an audit event including:

- request id  
- upstream identity  
- original prompt  
- rewritten prompt (if any)  
- selected model  
- OPA evaluation results  
- ONNX evaluation results  
- aggregated decision  
- approval id (if used)  
- response snapshots  
- timestamps  

Audit-event format must conform to audit-event.schema.json.

---

## 10. Workspace and Data Handling Rules

The LLM Gateway must:

- redact secrets before logging or forwarding prompts  
- avoid storing full prompts unless allowed by configuration  
- ensure sensitive embeddings are not logged  
- prevent cross-workflow data leakage  

Compliance with organizational data-handling policies is mandatory.

---

## 11. Error and Failure Modes

The Gateway must fail safely when:

- OPA evaluations cannot execute  
- ONNX models fail to load  
- routing cannot determine a model  
- the LLM provider is unreachable  
- redaction fails  
- approval mechanisms are unavailable  
- audit storage is unavailable (configurable behavior)

Default action on error: **deny**, unless configured differently.

---

## 12. Restart and Resume Behavior

The Gateway must:

- persist pending approvals  
- resume workflows in paused state  
- never repeat a request without explicit instruction  
- guarantee deterministic re-evaluation after restart  

No model requests may leak through during restart windows.

---

## 13. Prohibited Behaviors

The Gateway must not:

- bypass policy checks  
- silently alter model outputs  
- store sensitive content without explicit configuration  
- ignore OPA or ONNX failures  
- reuse approvals  
- omit audit logs  
- allow nondeterministic routing unless configured

---

## 14. Summary

The LLM Gateway is a safety and governance firewall that ensures:

- deterministic and auditable interactions with LLMs  
- policy-driven control of prompts and responses  
- human approval for risky content  
- safety-tier routing and prompt rewriting  
- comprehensive auditing of every LLM interaction  

It is a critical component of the CabinCrew Protocol’s end-to-end governance model.

