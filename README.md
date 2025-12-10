# Cabin Crew Protocol

This repository defines the core data structures and protocols for the Cabin Crew ecosystem.

## 🚨 Source of Truth

The contents of the `src/` directory are the **single source of truth** for all protocol definitions. All other libraries (`lib/`) and schemas (`schemas/`) are auto-generated from these TypeScript files.

**DO NOT edit files in `lib/` or `schemas/` manually.** They will be overwritten.

## Development

This repository includes tools to generate language-specific libraries and documentation.

### Prerequisites

- Node.js 20+
- Go 1.21+ (for verifying Go output)
- Python 3.10+ (for verifying Python output)

### Generating Code

Run the following commands to update all generated artifacts:

```bash
# 1. Install dependencies
npm install

# 2. Generate everything
npm run generate        # Generates JSON Schemas and MDX Docs
npm run generate:go     # Generates Go Library
npm run generate:nodejs # Generates Node.js Library
npm run generate:python # Generates Python Library
```

### Tools

Generation scripts are located in `tools/`.
- `tools/generate-schemas.ts`: Uses `typescript-json-schema` to create JSON Schemas and MDX.
- `tools/generate-*.ts`: Uses `quicktype` to create language bindings.

## CI/CD

The `.github/workflows/ci.yml` pipeline ensures that all generated code is up-to-date with `src/`. If you change `src/` but fail to run the generators and commit the results, the build will fail.
Version: draft

CabinCrew is an open, deterministic, and governable workflow protocol designed for AI-assisted automation.  
It provides a safe and auditable framework for orchestrating engines, enforcing policy, routing LLM interactions, and recording chain-of-custody events.

This repository contains the *formal specification*, *schemas*, and *examples* for implementers.

---

## 🚀 What Is CabinCrew?

CabinCrew is a protocol for secure automation in both developer and production environments.  
It ensures that AI agents, engines, and LLMs interact with systems *safely, deterministically, and with complete auditability*.

Key capabilities:

- **Flight-plan & take-off model** for safe intent separation  
- **Preflight governance** using OPA and ONNX  
- **Human approval workflows**  
- **MCP Gateway** to control agent tool access  
- **LLM Gateway** for safe prompt handling and model routing  
- **Artifact-based workflow governance**  
- **Plan-token integrity validation**  
- **Tamper-evident audit event system**  
- **Air-gapped compatible**  

CabinCrew is vendor-neutral and language-agnostic. Engines and orchestrators can be implemented in any environment.

---

## 📁 Repository Structure

```
cabincrew-protocol/
  spec/
    draft/
      overview.md
      architecture.md
      principles.md
      engine.md
      orchestrator.md
      orchestrator-preflight.md
      orchestrator-approval.md
      artifact.md
      plan-token.md
      mcp-gateway.md
      llm-gateway.md
      audit-event.md
      glossary.md

  schema/
    draft/
      engine.schema.json
      orchestrator.schema.json
      artifact.schema.json
      plan-token.schema.json
      mcp-gateway.schema.json
      llm-gateway.schema.json
      audit-event.schema.json

  examples/
    (to be populated)

  docs/
    overview.md
    architecture.md
    principles.md

  LICENSE
  CONTRIBUTING.md
  README.md
```

Specifications describe **behavior and semantics**.  
Schemas describe **structure and validation**.

Both are needed for interoperability.

---

## 📘 Specification Overview

The protocol specification is in `spec/draft/`:

- **overview.md** — High-level introduction  
- **architecture.md** — Component model and interactions  
- **principles.md** — Normative design rules  
- **engine.md** — Engine execution model  
- **orchestrator.md** — Core workflow state machine  
- **orchestrator-preflight.md** — Governance logic  
- **orchestrator-approval.md** — Human-in-the-loop workflow  
- **artifact.md** — Intent and evidence representation  
- **plan-token.md** — Chain-of-custody guarantees  
- **mcp-gateway.md** — Governance for agent tool calls  
- **llm-gateway.md** — Governance for LLM interactions  
- **audit-event.md** — Structured audit format  
- **glossary.md** — Shared terminology  

---

## 🧩 Schemas

Schemas conform to JSON Schema Draft-07.  
They define the interface shapes for:

- Engines  
- Orchestrator  
- Gateways  
- Artifacts  
- Plan-tokens  
- Audit events  

Schemas are versioned separately from specifications.

---

## 🛠️ Implementations

Reference implementations (coming soon):

- **Go Engine SDK**
- **Go Orchestrator**
- **MCP Gateway Proxy**
- **LLM Gateway Proxy**
- **CLI Tools**
- **Test Harness**

If you want to help implement these, see **CONTRIBUTING.md**.

---

## ✔️ Goals of CabinCrew

- Deterministic automation  
- Human safety guarantees  
- Full auditability  
- Seamless AI governance  
- Extensibility for any industry  
- Air-gapped and offline workflows  
- Multi-agent and LLM-native compatibility  

CabinCrew is designed to be the *secure foundation* for AI-driven automation systems.

---

## 📄 License

Licensed under the Apache License 2.0.  
See `LICENSE` for more details.

---

## 🙌 Contributing

We welcome specification updates, schema improvements, examples, and tooling contributions.  
See **CONTRIBUTING.md** for the complete process.

---

## 📬 Contact

For questions, ideas, or proposals, open an Issue or Pull Request.  
Formal proposals can be submitted via a *CabinCrew Design Proposal (CDP)*.

---

Thank you for helping build the CabinCrew Protocol —  
**the safe, deterministic automation layer for the AI era.**
