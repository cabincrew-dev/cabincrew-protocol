# Contributing to CabinCrew Protocol
Version: draft

Thank you for your interest in contributing to the CabinCrew Protocol!  
This document describes the contribution process, development conventions, and the rules that ensure consistency and quality across the specification, schemas, and reference implementations.

---

## 1. Code of Conduct

All contributors must adhere to respectful, professional, and inclusive behavior.  
Harassment or discrimination of any kind is not tolerated.

If you experience or observe unacceptable behavior, please contact the maintainers.

---

## 2. Types of Contributions

We welcome contributions in several areas:

### **2.1 Specification Contributions**
- Improving clarity of spec documents
- Proposing new sections or refinements
- Fixing inconsistencies or normative ambiguity
- Aligning spec language with schemas

### **2.2 Schema Contributions**
- Adding fields (with justification)
- Improving validation coverage
- Maintaining backward compatibility
- Creating new versioned releases under `schema/YYYY-MM-DD/`

### **2.3 Examples**
- Workflow examples
- Engine examples
- Gateway configurations
- Policy (OPA) and ONNX model integration examples

### **2.4 Tooling and SDKs**
- Orchestrator tooling
- Engine SDKs (Go, Rust, Python)
- Gateway integrations

### **2.5 Documentation**
- Tutorials
- Architecture diagrams
- Explanatory guides for implementers

---

## 3. Repository Structure Expectations

Contributions must follow the established layout:

```
cabincrew-protocol/
  spec/
    draft/
  schema/
    draft/
  examples/
  docs/
  LICENSE
  CONTRIBUTING.md
```

Do not introduce new folders without discussion.

---

## 4. Versioning Rules

### **4.1 Specification Versioning**
- Draft specifications reside under `spec/draft/`
- Released specifications are dated: `spec/YYYY-MM-DD/`
- Draft changes may be made via PRs at any time
- Release versions require maintainer approval

### **4.2 Schema Versioning**
- Schemas follow the same versioning pattern
- Breaking changes MUST result in a new version directory
- Schema compatibility must be preserved whenever possible

---

## 5. Contribution Workflow

### Step 1 — Fork the Repository
Create your own fork and clone it locally.

### Step 2 — Create a Feature Branch
```
git checkout -b feature/my-improvement
```

### Step 3 — Make Changes
- Follow the writing and style guidelines below.
- Update related documentation or schemas if relevant.
- Add examples if the feature needs illustration.

### Step 4 — Run Validation (if applicable)
If working with schemas:
- Validate JSON syntax
- Validate references
- Ensure draft versions remain consistent

### Step 5 — Submit a Pull Request
Your PR should include:
- A clear description of the change
- The reasoning behind it
- Any related issues
- Whether the change is normative or editorial
- Whether backward compatibility is affected

### Step 6 — Review Process
Maintainers will:
- Review for clarity and correctness
- Verify consistency with architectural principles
- Request changes when needed
- Approve and merge when ready

The review process may involve technical discussion—this is expected and encouraged.

---

## 6. Style Guidelines

### **6.1 Specification Writing**
- Use clear, precise, and normative language.
- Avoid ambiguous phrasing.
- Prefer *must*, *should*, *may* according to RFC 2119 conventions.
- Avoid implementation-specific language unless required.

### **6.2 JSON Schema**
- Use draft-07 format only.
- Include `$schema` at the top.
- Favor `type: object` with defined `properties`.
- Avoid arbitrary restrictions that prevent extensibility.
- Include descriptive `description` fields.

### **6.3 Examples**
- Keep examples realistic but minimal.
- Ensure they reflect the latest spec behavior.
- Avoid embedding secrets or personal data.

---

## 7. Backward Compatibility

Normative changes to the protocol must consider:

- orchestrator safety
- engine interoperability
- gateway behavior
- audit requirements
- plan-token semantics

Breaking changes must be:
- explicitly documented
- versioned
- communicated to implementers

---

## 8. How to Propose a Major Change

For large additions or changes, open a **CAB Design Proposal (CDP)**:

A CDP must contain:
- problem statement
- motivation
- alternatives considered
- proposed solution
- normative impact
- backward compatibility notes
- example use cases

Maintainers will review CDPs during specification planning cycles.

---

## 9. Security and Governance

Any change that affects:
- sandboxing
- artifact integrity
- gateway policy semantics
- plan-token logic
- approval workflows  
MUST undergo a security review.

---

## 10. Questions and Discussion

For ongoing discussion, contributors may use:
- Issues
- Pull Requests
- Discussion threads (if enabled)

Please avoid requesting major normative changes in PR descriptions.  
Use issues or CDP proposals for that.

---

## 11. Summary

CabinCrew thrives on clear, safe, and interoperable specifications.  
Your contributions—whether editorial, technical, or conceptual—help strengthen the protocol and expand its ecosystem.

Thank you for contributing to the CabinCrew Protocol!

