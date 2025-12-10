# CabinCrew Architecture Diagrams
Version: draft

This document provides **Mermaid-based architecture diagrams** illustrating the major components, data flows, and trust boundaries of the CabinCrew Protocol.  
These diagrams are non-normative but help implementers visualize the system.

---

# 1. High-Level System Architecture

```mermaid
flowchart LR
    A[User / Agent] --> B[Orchestrator]

    subgraph G1[Governance Layer]
        C1[OPA Policies]
        C2[ONNX Models]
        C3[Approval Workflow]
    end

    B --> G1

    B --> D1[Engine (flight-plan)]
    D1 --> E[Artifacts]
    E --> B

    B --> D2[Engine (take-off)]
    D2 --> F[Side Effects / System Changes]

    subgraph G2[Gateways]
        G21[MCP Gateway]
        G22[LLM Gateway]
    end

    A --> G2 --> B
```

---

# 2. Workflow Lifecycle

```mermaid
stateDiagram-v2
    [*] --> INIT

    INIT --> PLAN_GENERATED : Run Engine (flight-plan)
    PLAN_GENERATED --> ARTIFACTS_VALIDATED : Validate artifacts
    ARTIFACTS_VALIDATED --> TOKEN_CREATED : Generate plan-token
    TOKEN_CREATED --> PREFLIGHT : Run governance checks

    PREFLIGHT --> AWAITING_APPROVAL : require_approval
    PREFLIGHT --> READY_FOR_TAKEOFF : allow / warn
    PREFLIGHT --> FAILED : deny

    AWAITING_APPROVAL --> APPROVED : Human approves
    APPROVED --> READY_FOR_TAKEOFF

    READY_FOR_TAKEOFF --> EXECUTION_COMPLETE : Run Engine (take-off)
    EXECUTION_COMPLETE --> COMPLETED
    READY_FOR_TAKEOFF --> FAILED : Token mismatch

    FAILED --> [*]
    COMPLETED --> [*]
```

---

# 3. Governance Pipeline

```mermaid
flowchart TD
    A[Input Payload] --> B[OPA Evaluation]
    A --> C[ONNX Evaluation]

    B --> D[Aggregation Engine]
    C --> D

    D -->|deny| E1[Block Execution]
    D -->|require_approval| E2[Trigger Human Approval]
    D -->|warn| E3[Continue with Warning]
    D -->|allow| E4[Proceed Safely]
```

---

# 4. MCP Gateway Architecture

```mermaid
flowchart LR
    Agent --> A[MCP Request Validator]

    A --> B[OPA Policy Checks]
    A --> C[ONNX Risk Models]

    B --> D[Decision Aggregator]
    C --> D

    D -->|deny| X1[Return MCP Error]
    D -->|require_approval| X2[Pause Workflow]
    D -->|warn| X3[Log Warning & Continue]
    D -->|allow| X4[Forward to MCP Server]

    X4 --> S[MCP Server]
    S --> R[Response]

    R --> V[Response OPA/ONNX Evaluation]
    V --> D
```

---

# 5. LLM Gateway Architecture

```mermaid
flowchart LR
    U[User / Agent Prompt] --> P1[Prompt Sanitizer]
    P1 --> P2[Prompt Rewriter]

    P2 --> OPA1[OPA: Prompt Check]
    P2 --> ONNX1[ONNX: Prompt Risk Models]

    OPA1 --> AGG[Decision Aggregator]
    ONNX1 --> AGG

    AGG -->|deny| D1[Block Prompt]
    AGG -->|require_approval| D2[Wait for Human Approval]
    AGG -->|warn| D3[Proceed with Warning]
    AGG -->|allow| ROUTE[Model Router]

    ROUTE --> LLM[Chosen LLM]
    LLM --> O[Raw Output]

    O --> OPA2[OPA: Output Validation]
    O --> ONNX2[ONNX: Output Risk Models]

    OPA2 --> AGG2[Decision Aggregation]
    ONNX2 --> AGG2

    AGG2 -->|deny| F1[Block Output]
    AGG2 -->|require_approval| F2[Wait for Human Approval]
    AGG2 -->|warn| F3[Return Output with Warning]
    AGG2 -->|allow| F4[Return Safe Output]
```

---

# 6. Engine Execution Environment

```mermaid
flowchart TD

    subgraph Inputs
        A1[STDIN JSON Input]
        A2[Workspace: CABINCREW_WORKSPACE]
        A3[Artifacts Dir: CABINCREW_ARTIFACTS_DIR]
        A4[Temp Dir: CABINCREW_TEMP_DIR]
    end

    subgraph Engine
        B1[Run flight-plan]
        B2[Run take-off]
        B3[Generate Receipt]
        B4[Generate Artifacts]
    end

    A1 --> B1
    A2 --> B1
    A3 --> B1

    A1 --> B2
    A2 --> B2
    A3 --> B2

    B4 --> C[Artifacts Returned to Orchestrator]
```

---

# 7. Trust Boundary Diagram

```mermaid
flowchart LR
    subgraph Trusted
        O[Orchestrator]
        AP[Approval System]
    end

    subgraph SemiTrusted
        GW[MCP + LLM Gateways]
    end

    subgraph Untrusted
        AG[Agents]
        LLM[LLM Models]
        MCP[MCP Servers]
        ENG[Engines]
    end

    AG --> GW --> O
    O --> ENG
    GW --> MCP
    GW --> LLM
```

---

# 8. Summary

These diagrams show how CabinCrew:

- isolates untrusted components  
- enforces governance at boundaries  
- validates artifacts before execution  
- ensures deterministic workflow state  
- routes all LLM/MCP traffic through safety firewalls  

They are intended to help implementers understand system responsibilities, trust assumptions, and data flows at a glance.

