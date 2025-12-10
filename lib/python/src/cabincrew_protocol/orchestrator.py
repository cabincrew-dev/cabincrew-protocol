from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional, Dict, Union, TypeVar, Callable, Type, cast
import json
from datetime import datetime

from .shared import *

from .engine import EngineOutputClass
from .engine import Mode
from .plantoken import PlanToken

class PreflightEvidence:
    hash: str
    name: str
    path: str

    def __init__(self, hash: str, name: str, path: str) -> None:
        self.hash = hash
        self.name = name
        self.path = path

    @staticmethod
    def from_dict(obj: Any) -> 'PreflightEvidence':
        assert isinstance(obj, dict)
        hash = from_str(obj.get("hash"))
        name = from_str(obj.get("name"))
        path = from_str(obj.get("path"))
        return PreflightEvidence(hash, name, path)

    def to_dict(self) -> dict:
        result: dict = {}
        result["hash"] = from_str(self.hash)
        result["name"] = from_str(self.name)
        result["path"] = from_str(self.path)
        return result



class ApprovalRequest:
    approval_id: str
    engine_output: Optional[EngineOutputClass]
    evidence: Optional[List[PreflightEvidence]]
    plan_token_hash: Optional[str]
    reason: str
    required_role: str
    step_id: str
    workflow_id: str

    def __init__(self, approval_id: str, engine_output: Optional[EngineOutputClass], evidence: Optional[List[PreflightEvidence]], plan_token_hash: Optional[str], reason: str, required_role: str, step_id: str, workflow_id: str) -> None:
        self.approval_id = approval_id
        self.engine_output = engine_output
        self.evidence = evidence
        self.plan_token_hash = plan_token_hash
        self.reason = reason
        self.required_role = required_role
        self.step_id = step_id
        self.workflow_id = workflow_id

    @staticmethod
    def from_dict(obj: Any) -> 'ApprovalRequest':
        assert isinstance(obj, dict)
        approval_id = from_str(obj.get("approval_id"))
        engine_output = from_union([EngineOutputClass.from_dict, from_none], obj.get("engine_output"))
        evidence = from_union([lambda x: from_list(PreflightEvidence.from_dict, x), from_none], obj.get("evidence"))
        plan_token_hash = from_union([from_str, from_none], obj.get("plan_token_hash"))
        reason = from_str(obj.get("reason"))
        required_role = from_str(obj.get("required_role"))
        step_id = from_str(obj.get("step_id"))
        workflow_id = from_str(obj.get("workflow_id"))
        return ApprovalRequest(approval_id, engine_output, evidence, plan_token_hash, reason, required_role, step_id, workflow_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approval_id"] = from_str(self.approval_id)
        if self.engine_output is not None:
            result["engine_output"] = from_union([lambda x: to_class(EngineOutputClass, x), from_none], self.engine_output)
        if self.evidence is not None:
            result["evidence"] = from_union([lambda x: from_list(lambda x: to_class(PreflightEvidence, x), x), from_none], self.evidence)
        if self.plan_token_hash is not None:
            result["plan_token_hash"] = from_union([from_str, from_none], self.plan_token_hash)
        result["reason"] = from_str(self.reason)
        result["required_role"] = from_str(self.required_role)
        result["step_id"] = from_str(self.step_id)
        result["workflow_id"] = from_str(self.workflow_id)
        return result



class ApprovalResponse:
    approval_id: str
    approved: bool
    approver: Optional[str]
    reason: Optional[str]
    timestamp: Optional[str]

    def __init__(self, approval_id: str, approved: bool, approver: Optional[str], reason: Optional[str], timestamp: Optional[str]) -> None:
        self.approval_id = approval_id
        self.approved = approved
        self.approver = approver
        self.reason = reason
        self.timestamp = timestamp

    @staticmethod
    def from_dict(obj: Any) -> 'ApprovalResponse':
        assert isinstance(obj, dict)
        approval_id = from_str(obj.get("approval_id"))
        approved = from_bool(obj.get("approved"))
        approver = from_union([from_str, from_none], obj.get("approver"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        timestamp = from_union([from_str, from_none], obj.get("timestamp"))
        return ApprovalResponse(approval_id, approved, approver, reason, timestamp)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approval_id"] = from_str(self.approval_id)
        result["approved"] = from_bool(self.approved)
        if self.approver is not None:
            result["approver"] = from_union([from_str, from_none], self.approver)
        if self.reason is not None:
            result["reason"] = from_union([from_str, from_none], self.reason)
        if self.timestamp is not None:
            result["timestamp"] = from_union([from_str, from_none], self.timestamp)
        return result



class PreflightInput:
    context: Optional[EngineOutputClass]
    engine_output: EngineOutputClass
    evidence: Optional[List[PreflightEvidence]]
    mode: Mode
    plan_token: Optional[PlanToken]
    """Cryptographic binding between a flight-plan and its subsequent take-off.
    Defined in schemas/draft/plan-token.schema.json
    """
    step_id: str
    workflow_id: str

    def __init__(self, context: Optional[EngineOutputClass], engine_output: EngineOutputClass, evidence: Optional[List[PreflightEvidence]], mode: Mode, plan_token: Optional[PlanToken], step_id: str, workflow_id: str) -> None:
        self.context = context
        self.engine_output = engine_output
        self.evidence = evidence
        self.mode = mode
        self.plan_token = plan_token
        self.step_id = step_id
        self.workflow_id = workflow_id

    @staticmethod
    def from_dict(obj: Any) -> 'PreflightInput':
        assert isinstance(obj, dict)
        context = from_union([EngineOutputClass.from_dict, from_none], obj.get("context"))
        engine_output = EngineOutputClass.from_dict(obj.get("engine_output"))
        evidence = from_union([lambda x: from_list(PreflightEvidence.from_dict, x), from_none], obj.get("evidence"))
        mode = Mode(obj.get("mode"))
        plan_token = from_union([PlanToken.from_dict, from_none], obj.get("plan_token"))
        step_id = from_str(obj.get("step_id"))
        workflow_id = from_str(obj.get("workflow_id"))
        return PreflightInput(context, engine_output, evidence, mode, plan_token, step_id, workflow_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.context is not None:
            result["context"] = from_union([lambda x: to_class(EngineOutputClass, x), from_none], self.context)
        result["engine_output"] = to_class(EngineOutputClass, self.engine_output)
        if self.evidence is not None:
            result["evidence"] = from_union([lambda x: from_list(lambda x: to_class(PreflightEvidence, x), x), from_none], self.evidence)
        result["mode"] = to_enum(Mode, self.mode)
        if self.plan_token is not None:
            result["plan_token"] = from_union([lambda x: to_class(PlanToken, x), from_none], self.plan_token)
        result["step_id"] = from_str(self.step_id)
        result["workflow_id"] = from_str(self.workflow_id)
        return result



class PreflightOutputDecision(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    WARN = "WARN"



class PreflightRequires:
    reason: Optional[str]
    role: Optional[str]

    def __init__(self, reason: Optional[str], role: Optional[str]) -> None:
        self.reason = reason
        self.role = role

    @staticmethod
    def from_dict(obj: Any) -> 'PreflightRequires':
        assert isinstance(obj, dict)
        reason = from_union([from_str, from_none], obj.get("reason"))
        role = from_union([from_str, from_none], obj.get("role"))
        return PreflightRequires(reason, role)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.reason is not None:
            result["reason"] = from_union([from_str, from_none], self.reason)
        if self.role is not None:
            result["role"] = from_union([from_str, from_none], self.role)
        return result



class PreflightOutput:
    decision: PreflightOutputDecision
    requires: Optional[PreflightRequires]
    violations: Optional[List[str]]
    warnings: Optional[List[str]]

    def __init__(self, decision: PreflightOutputDecision, requires: Optional[PreflightRequires], violations: Optional[List[str]], warnings: Optional[List[str]]) -> None:
        self.decision = decision
        self.requires = requires
        self.violations = violations
        self.warnings = warnings

    @staticmethod
    def from_dict(obj: Any) -> 'PreflightOutput':
        assert isinstance(obj, dict)
        decision = PreflightOutputDecision(obj.get("decision"))
        requires = from_union([PreflightRequires.from_dict, from_none], obj.get("requires"))
        violations = from_union([lambda x: from_list(from_str, x), from_none], obj.get("violations"))
        warnings = from_union([lambda x: from_list(from_str, x), from_none], obj.get("warnings"))
        return PreflightOutput(decision, requires, violations, warnings)

    def to_dict(self) -> dict:
        result: dict = {}
        result["decision"] = to_enum(PreflightOutputDecision, self.decision)
        if self.requires is not None:
            result["requires"] = from_union([lambda x: to_class(PreflightRequires, x), from_none], self.requires)
        if self.violations is not None:
            result["violations"] = from_union([lambda x: from_list(from_str, x), from_none], self.violations)
        if self.warnings is not None:
            result["warnings"] = from_union([lambda x: from_list(from_str, x), from_none], self.warnings)
        return result



class State(Enum):
    APPROVED = "APPROVED"
    ARTIFACTS_VALIDATED = "ARTIFACTS_VALIDATED"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    EXECUTION_COMPLETE = "EXECUTION_COMPLETE"
    FAILED = "FAILED"
    INIT = "INIT"
    PLAN_GENERATED = "PLAN_GENERATED"
    PLAN_RUNNING = "PLAN_RUNNING"
    PREFLIGHT_COMPLETE = "PREFLIGHT_COMPLETE"
    PRE_FLIGHT_RUNNING = "PRE_FLIGHT_RUNNING"
    READY_FOR_TAKEOFF = "READY_FOR_TAKEOFF"
    TAKEOFF_RUNNING = "TAKEOFF_RUNNING"
    TOKEN_CREATED = "TOKEN_CREATED"



class WorkflowState:
    last_decision: Optional[str]
    plan_token_hash: Optional[str]
    state: State
    step_id: Optional[str]
    workflow_id: Optional[str]

    def __init__(self, last_decision: Optional[str], plan_token_hash: Optional[str], state: State, step_id: Optional[str], workflow_id: Optional[str]) -> None:
        self.last_decision = last_decision
        self.plan_token_hash = plan_token_hash
        self.state = state
        self.step_id = step_id
        self.workflow_id = workflow_id

    @staticmethod
    def from_dict(obj: Any) -> 'WorkflowState':
        assert isinstance(obj, dict)
        last_decision = from_union([from_str, from_none], obj.get("last_decision"))
        plan_token_hash = from_union([from_str, from_none], obj.get("plan_token_hash"))
        state = State(obj.get("state"))
        step_id = from_union([from_str, from_none], obj.get("step_id"))
        workflow_id = from_union([from_str, from_none], obj.get("workflow_id"))
        return WorkflowState(last_decision, plan_token_hash, state, step_id, workflow_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.last_decision is not None:
            result["last_decision"] = from_union([from_str, from_none], self.last_decision)
        if self.plan_token_hash is not None:
            result["plan_token_hash"] = from_union([from_str, from_none], self.plan_token_hash)
        result["state"] = to_enum(State, self.state)
        if self.step_id is not None:
            result["step_id"] = from_union([from_str, from_none], self.step_id)
        if self.workflow_id is not None:
            result["workflow_id"] = from_union([from_str, from_none], self.workflow_id)
        return result


