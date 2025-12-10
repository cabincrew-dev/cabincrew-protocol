# LLM Safety & Routing Guide
Version: draft

This document explains how CabinCrew implements **safe, policy-driven, deterministic LLM usage** through the LLM Gateway.  
It describes prompt rewriting, output validation, model routing, ONNX risk scoring, and governance workflows.

This is a non-normative guide that supplements:

- `spec/draft/llm-gateway.md`
- `schema/draft/llm-gateway.schema.json`
- `docs/governance.md`
- `docs/security.md`

---

# 1. Purpose of the LLM Gateway

LLMs are nondeterministic and can be unpredictable.  
The LLM Gateway acts as a **safety firewall**, ensuring that:

- unsafe prompts are rewritten or blocked  
- unsafe completions are rejected or require approval  
- model routing is deterministic  
- governance rules are always enforced  
- secrets are never leaked  
- hallucinations are caught early  
- audit logs capture the entire chain of reasoning  

CabinCrew treats LLMs as **untrusted assistants**, not autonomous decision-makers.

---

# 2. LLM Gateway Responsibilities

The Gateway must:

### **2.1 Enforce Safety Policies**
- OPA evaluation on prompts and outputs  
- ONNX model scoring  
- policy aggregation (allow / warn / deny / require_approval)

### **2.2 Enforce Data Loss Prevention**
- secret detection  
- PII detection  
- regulated content blocking  
- preventing model exfiltration

### **2.3 Provide Deterministic Routing**
- select model based on tier, risk, cost, or rules  
- ensure predictable behavior across runs

### **2.4 Rewriting & Normalization**
- adding system safety instructions  
- rewriting unsafe user prompts  
- sanitizing model output

### **2.5 Auditability**
Produce audit logs for:
- prompt  
- model selection  
- governance results  
- safety metrics  
- response  
- warnings or blocks  

---

# 3. Request Lifecycle

```
Prompt → Gateway → Governance (OPA/ONNX) → Model Routing → LLM → Governance → Response
```

Every part must be deterministic except the LLM itself.

---

# 4. Prompt Preparation

Before sending a prompt to the model, Gateway may:

### **4.1 Rewrite System Prompt**
Inject governance instructions such as:

- “Do not generate unsafe actions.”  
- “Do not hallucinate unknown APIs.”  
- “Never expose secrets.”  
- “Use deterministic formatting.”  

### **4.2 Sanitize User Input**
- remove embedded tokens  
- remove secrets  
- remove malicious directives  
- collapse dangerous patterns  

### **4.3 Apply Content Policies**
OPA rules may block prompts containing:
- personally identifiable info  
- confidential content  
- production configuration  
- dangerous command patterns  

LLM Gateway preserves an audit record of both:
- original prompt  
- rewritten prompt  

---

# 5. Model Routing

Routing can be controlled by:

### **Static Rules**
- “All infra-related queries use Claude Sonnet.”
- “All summarization uses GPT-X.”
- “Sensitive content requires safe-tier models.”

### **Risk-Based Routing**
ONNX classification → choose safer model if:
- hallucination risk exceeds threshold  
- toxicity predicted  
- elevated security context  

### **Fallback Routing**
If primary model fails:
- fallback to alternate  
- retry with different parameters  
- evaluate second model for safety  

Routing decisions must be deterministic and audited.

---

# 6. ONNX Safety Models

ONNX is used to classify prompts and outputs.  
Examples:

### Prompt Models:
- secret detection  
- jailbreak detection  
- toxicity  
- bias  
- hallucination-risk predictor  

### Output Models:
- unsafe content scoring  
- code vulnerability models  
- secret leakage  
- hallucination recognition  

### Normalization
ONNX output is normalized to:

```
allow | warn | deny | require_approval
```

Thresholds are configurable in LLM Gateway.

---

# 7. OPA Policy Evaluation

OPA receives:

```
{
  "model": "claude-3-opus",
  "prompt_original": "...",
  "prompt_rewritten": "...",
  "context": {...},
  "workflow": {...},
  "safety": {... ONNX scores ...}
}
```

OPA is used for:

- compliance  
- regulated content  
- domain-specific rules  
- model selection constraints  
- approval requirements  

OPA may produce:
- allow  
- warn  
- deny  
- require_approval  

OPA failures → deny (unless configured otherwise).

---

# 8. Response Validation

After the LLM produces an output:

### 8.1 The Gateway validates the raw output
- scan for unsafe content  
- detect hallucinations  
- ensure structure matches requested format  

### 8.2 ONNX classification runs again
e.g. generating:
- hallucination score  
- toxicity score  
- bias classification  

### 8.3 OPA analysis runs against:
- content  
- metadata  
- safety metrics  

### 8.4 Aggregation rules applied
`deny > require_approval > warn > allow`

### 8.5 Enforcement
- **deny** → error to caller  
- **require_approval** → pause workflow  
- **warn** → continue with audit  
- **allow** → deliver response  

---

# 9. Output Sanitization

Before returning LLM output, Gateway may:

- redact secrets  
- sanitize file paths  
- remove harmful instructions  
- enforce structure (e.g., “must return JSON”)  

Sanitization must be logged.

---

# 10. Example Safety Flow

### Prompt:
```
"Write a script to delete all files in /etc."
```

### Gateway Flow:

1. **Rewrite** → add safety constraints  
2. **OPA** → deny (unsafe intent)  
3. **ONNX** → high-risk command classification  
4. **Decision** → deny  
5. **Audit** → record attempted unsafe action  
6. Response → error message  

---

# 11. Approval Workflow for LLM Responses

If risk is ambiguous, Gateway can request approval:

Examples:
- code changes needing review  
- multi-step instructions affecting prod systems  
- approval-required task category  

Human reviews:
- rewritten prompt  
- LLM output  
- ONNX risk scores  
- OPA rule metadata  

If approved → LLM response forwarded.  
If rejected → workflow fails.

---

# 12. Key Safety Design Principles

### **12.1 LLMs never directly access systems**
They must pass through MCP Gateway or Engine.

### **12.2 No direct file writes**
LLM-generated patches must go through MCP with governance.

### **12.3 All decisions are auditable**
Every routing, risk score, and block is recorded.

### **12.4 LLM output cannot modify workflow state**
Unless explicitly approved and consistent.

### **12.5 Deterministic routing**
Ensures reproducibility despite LLM nondeterminism.

---

# 13. Recommended Best Practices

- Keep ONNX models small and fast  
- Use separate safety-tier and productivity-tier models  
- Always rewrite prompts for safety  
- Restrict agent-driven LLM calls  
- Never allow “free-form execution” responses  
- Use JSON schema for structured outputs  

---

# 14. Minimal Configuration Example

```
models:
  primary: claude-3-sonnet
  fallback: gpt-4o-mini
  safety_model: ./models/toxicity.onnx

governance:
  policies: ./policies/llm/
  onnx_thresholds:
    hallucination: 0.6
    toxicity: 0.4
```

---

# 15. Summary

The LLM Gateway ensures that all LLM activity is:

- safe  
- governed  
- deterministic  
- auditable  
- non-leaking  
- human-reviewable  

It prevents dangerous instructions, blocks bad outputs, rewrites prompts safely, selects appropriate models, and enforces policy-driven automation.

CabinCrew treats LLMs with caution —  
**powerful, but untrusted.**

