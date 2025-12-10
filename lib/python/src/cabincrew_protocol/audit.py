from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional, Dict, Union, TypeVar, Callable, Type, cast
import json
from datetime import datetime

from .shared import *

from .plantoken import PlanArtifactHash

class AuditApproval:
    approval_id: Optional[str]
    approved: Optional[bool]
    approver: Optional[str]
    reason: Optional[str]
    required_role: Optional[str]

    def __init__(self, approval_id: Optional[str], approved: Optional[bool], approver: Optional[str], reason: Optional[str], required_role: Optional[str]) -> None:
        self.approval_id = approval_id
        self.approved = approved
        self.approver = approver
        self.reason = reason
        self.required_role = required_role

    @staticmethod
    def from_dict(obj: Any) -> 'AuditApproval':
        assert isinstance(obj, dict)
        approval_id = from_union([from_str, from_none], obj.get("approval_id"))
        approved = from_union([from_bool, from_none], obj.get("approved"))
        approver = from_union([from_str, from_none], obj.get("approver"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        required_role = from_union([from_str, from_none], obj.get("required_role"))
        return AuditApproval(approval_id, approved, approver, reason, required_role)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.approval_id is not None:
            result["approval_id"] = from_union([from_str, from_none], self.approval_id)
        if self.approved is not None:
            result["approved"] = from_union([from_bool, from_none], self.approved)
        if self.approver is not None:
            result["approver"] = from_union([from_str, from_none], self.approver)
        if self.reason is not None:
            result["reason"] = from_union([from_str, from_none], self.reason)
        if self.required_role is not None:
            result["required_role"] = from_union([from_str, from_none], self.required_role)
        return result



class AuditArtifact:
    hash: Optional[str]
    name: Optional[str]
    path: Optional[str]
    role: Optional[str]
    size: Optional[float]

    def __init__(self, hash: Optional[str], name: Optional[str], path: Optional[str], role: Optional[str], size: Optional[float]) -> None:
        self.hash = hash
        self.name = name
        self.path = path
        self.role = role
        self.size = size

    @staticmethod
    def from_dict(obj: Any) -> 'AuditArtifact':
        assert isinstance(obj, dict)
        hash = from_union([from_str, from_none], obj.get("hash"))
        name = from_union([from_str, from_none], obj.get("name"))
        path = from_union([from_str, from_none], obj.get("path"))
        role = from_union([from_str, from_none], obj.get("role"))
        size = from_union([from_float, from_none], obj.get("size"))
        return AuditArtifact(hash, name, path, role, size)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.hash is not None:
            result["hash"] = from_union([from_str, from_none], self.hash)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.path is not None:
            result["path"] = from_union([from_str, from_none], self.path)
        if self.role is not None:
            result["role"] = from_union([from_str, from_none], self.role)
        if self.size is not None:
            result["size"] = from_union([to_float, from_none], self.size)
        return result



class AuditEngine:
    engine_id: Optional[str]
    error: Optional[str]
    receipt_id: Optional[str]
    status: Optional[str]

    def __init__(self, engine_id: Optional[str], error: Optional[str], receipt_id: Optional[str], status: Optional[str]) -> None:
        self.engine_id = engine_id
        self.error = error
        self.receipt_id = receipt_id
        self.status = status

    @staticmethod
    def from_dict(obj: Any) -> 'AuditEngine':
        assert isinstance(obj, dict)
        engine_id = from_union([from_str, from_none], obj.get("engine_id"))
        error = from_union([from_str, from_none], obj.get("error"))
        receipt_id = from_union([from_str, from_none], obj.get("receipt_id"))
        status = from_union([from_str, from_none], obj.get("status"))
        return AuditEngine(engine_id, error, receipt_id, status)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.engine_id is not None:
            result["engine_id"] = from_union([from_str, from_none], self.engine_id)
        if self.error is not None:
            result["error"] = from_union([from_str, from_none], self.error)
        if self.receipt_id is not None:
            result["receipt_id"] = from_union([from_str, from_none], self.receipt_id)
        if self.status is not None:
            result["status"] = from_union([from_str, from_none], self.status)
        return result



class AuditGateway:
    gateway_type: Optional[str]
    model: Optional[str]
    policy_decision: Optional[str]
    request_id: Optional[str]
    tool: Optional[str]

    def __init__(self, gateway_type: Optional[str], model: Optional[str], policy_decision: Optional[str], request_id: Optional[str], tool: Optional[str]) -> None:
        self.gateway_type = gateway_type
        self.model = model
        self.policy_decision = policy_decision
        self.request_id = request_id
        self.tool = tool

    @staticmethod
    def from_dict(obj: Any) -> 'AuditGateway':
        assert isinstance(obj, dict)
        gateway_type = from_union([from_str, from_none], obj.get("gateway_type"))
        model = from_union([from_str, from_none], obj.get("model"))
        policy_decision = from_union([from_str, from_none], obj.get("policy_decision"))
        request_id = from_union([from_str, from_none], obj.get("request_id"))
        tool = from_union([from_str, from_none], obj.get("tool"))
        return AuditGateway(gateway_type, model, policy_decision, request_id, tool)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.gateway_type is not None:
            result["gateway_type"] = from_union([from_str, from_none], self.gateway_type)
        if self.model is not None:
            result["model"] = from_union([from_str, from_none], self.model)
        if self.policy_decision is not None:
            result["policy_decision"] = from_union([from_str, from_none], self.policy_decision)
        if self.request_id is not None:
            result["request_id"] = from_union([from_str, from_none], self.request_id)
        if self.tool is not None:
            result["tool"] = from_union([from_str, from_none], self.tool)
        return result



class AuditIntegrity:
    actual_plan_token: Optional[str]
    artifacts_match: Optional[bool]
    differences: Optional[List[str]]
    expected_plan_token: Optional[str]
    plan_token_match: Optional[bool]

    def __init__(self, actual_plan_token: Optional[str], artifacts_match: Optional[bool], differences: Optional[List[str]], expected_plan_token: Optional[str], plan_token_match: Optional[bool]) -> None:
        self.actual_plan_token = actual_plan_token
        self.artifacts_match = artifacts_match
        self.differences = differences
        self.expected_plan_token = expected_plan_token
        self.plan_token_match = plan_token_match

    @staticmethod
    def from_dict(obj: Any) -> 'AuditIntegrity':
        assert isinstance(obj, dict)
        actual_plan_token = from_union([from_str, from_none], obj.get("actual_plan_token"))
        artifacts_match = from_union([from_bool, from_none], obj.get("artifacts_match"))
        differences = from_union([lambda x: from_list(from_str, x), from_none], obj.get("differences"))
        expected_plan_token = from_union([from_str, from_none], obj.get("expected_plan_token"))
        plan_token_match = from_union([from_bool, from_none], obj.get("plan_token_match"))
        return AuditIntegrity(actual_plan_token, artifacts_match, differences, expected_plan_token, plan_token_match)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.actual_plan_token is not None:
            result["actual_plan_token"] = from_union([from_str, from_none], self.actual_plan_token)
        if self.artifacts_match is not None:
            result["artifacts_match"] = from_union([from_bool, from_none], self.artifacts_match)
        if self.differences is not None:
            result["differences"] = from_union([lambda x: from_list(from_str, x), from_none], self.differences)
        if self.expected_plan_token is not None:
            result["expected_plan_token"] = from_union([from_str, from_none], self.expected_plan_token)
        if self.plan_token_match is not None:
            result["plan_token_match"] = from_union([from_bool, from_none], self.plan_token_match)
        return result



class AuditEventPlanToken:
    """Cryptographic binding between a flight-plan and its subsequent take-off.
    Defined in schemas/draft/plan-token.schema.json
    """
    artifacts: List[PlanArtifactHash]
    """Per-artifact hashes that contributed to this plan token."""

    created_at: str
    """Timestamp when the plan was created (RFC3339)."""

    engine_id: str
    """Engine identity that produced this plan."""

    model: str
    """AI Model identifier used to generate this plan (e.g. 'gpt-4', 'claude-3').
    Required for provenance.
    """
    protocol_version: str
    """Engine protocol version used when this plan was produced."""

    token: str
    """Primary plan token identifier, e.g. SHA256 over all plan artifacts + context."""

    workspace_hash: str
    """Hash of the workspace state when the plan was created."""

    def __init__(self, artifacts: List[PlanArtifactHash], created_at: str, engine_id: str, model: str, protocol_version: str, token: str, workspace_hash: str) -> None:
        self.artifacts = artifacts
        self.created_at = created_at
        self.engine_id = engine_id
        self.model = model
        self.protocol_version = protocol_version
        self.token = token
        self.workspace_hash = workspace_hash

    @staticmethod
    def from_dict(obj: Any) -> 'AuditEventPlanToken':
        assert isinstance(obj, dict)
        artifacts = from_list(PlanArtifactHash.from_dict, obj.get("artifacts"))
        created_at = from_str(obj.get("created_at"))
        engine_id = from_str(obj.get("engine_id"))
        model = from_str(obj.get("model"))
        protocol_version = from_str(obj.get("protocol_version"))
        token = from_str(obj.get("token"))
        workspace_hash = from_str(obj.get("workspace_hash"))
        return AuditEventPlanToken(artifacts, created_at, engine_id, model, protocol_version, token, workspace_hash)

    def to_dict(self) -> dict:
        result: dict = {}
        result["artifacts"] = from_list(lambda x: to_class(PlanArtifactHash, x), self.artifacts)
        result["created_at"] = from_str(self.created_at)
        result["engine_id"] = from_str(self.engine_id)
        result["model"] = from_str(self.model)
        result["protocol_version"] = from_str(self.protocol_version)
        result["token"] = from_str(self.token)
        result["workspace_hash"] = from_str(self.workspace_hash)
        return result



class AuditPolicy:
    decision: Optional[str]
    engine: Optional[str]
    violations: Optional[List[str]]
    warnings: Optional[List[str]]

    def __init__(self, decision: Optional[str], engine: Optional[str], violations: Optional[List[str]], warnings: Optional[List[str]]) -> None:
        self.decision = decision
        self.engine = engine
        self.violations = violations
        self.warnings = warnings

    @staticmethod
    def from_dict(obj: Any) -> 'AuditPolicy':
        assert isinstance(obj, dict)
        decision = from_union([from_str, from_none], obj.get("decision"))
        engine = from_union([from_str, from_none], obj.get("engine"))
        violations = from_union([lambda x: from_list(from_str, x), from_none], obj.get("violations"))
        warnings = from_union([lambda x: from_list(from_str, x), from_none], obj.get("warnings"))
        return AuditPolicy(decision, engine, violations, warnings)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.decision is not None:
            result["decision"] = from_union([from_str, from_none], self.decision)
        if self.engine is not None:
            result["engine"] = from_union([from_str, from_none], self.engine)
        if self.violations is not None:
            result["violations"] = from_union([lambda x: from_list(from_str, x), from_none], self.violations)
        if self.warnings is not None:
            result["warnings"] = from_union([lambda x: from_list(from_str, x), from_none], self.warnings)
        return result



class Severity(Enum):
    CRITICAL = "critical"
    DEBUG = "debug"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"



class AuditWorkflow:
    mode: Optional[str]
    step_id: Optional[str]
    workflow_id: Optional[str]

    def __init__(self, mode: Optional[str], step_id: Optional[str], workflow_id: Optional[str]) -> None:
        self.mode = mode
        self.step_id = step_id
        self.workflow_id = workflow_id

    @staticmethod
    def from_dict(obj: Any) -> 'AuditWorkflow':
        assert isinstance(obj, dict)
        mode = from_union([from_str, from_none], obj.get("mode"))
        step_id = from_union([from_str, from_none], obj.get("step_id"))
        workflow_id = from_union([from_str, from_none], obj.get("workflow_id"))
        return AuditWorkflow(mode, step_id, workflow_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.mode is not None:
            result["mode"] = from_union([from_str, from_none], self.mode)
        if self.step_id is not None:
            result["step_id"] = from_union([from_str, from_none], self.step_id)
        if self.workflow_id is not None:
            result["workflow_id"] = from_union([from_str, from_none], self.workflow_id)
        return result



class AuditEvent:
    """Canonical schema for all audit log events.
    Defined in schemas/draft/audit-event.schema.json
    """
    approval: Optional[AuditApproval]
    artifacts: Optional[List[AuditArtifact]]
    chain_hash: Optional[str]
    """Hash of the previous event in the chain. Allows for ledger-style verification."""

    engine: Optional[AuditEngine]
    event_id: str
    """Unique identifier for this audit event."""

    event_type: str
    """Free-form event category."""

    gateway: Optional[AuditGateway]
    integrity_check: Optional[AuditIntegrity]
    message: Optional[str]
    plan_token: Optional[AuditEventPlanToken]
    """Cryptographic binding between a flight-plan and its subsequent take-off.
    Defined in schemas/draft/plan-token.schema.json
    """
    policy: Optional[AuditPolicy]
    severity: Optional[Severity]
    signature: Optional[str]
    """Cryptographic signature of this event hash."""

    signature_key_ref: Optional[str]
    """Reference to the key used for signing (e.g. 'engine-key-1', 'orchestrator-key-prod')."""

    timestamp: str
    """RFC3339 timestamp of when the event occurred."""

    workflow: Optional[AuditWorkflow]

    def __init__(self, approval: Optional[AuditApproval], artifacts: Optional[List[AuditArtifact]], chain_hash: Optional[str], engine: Optional[AuditEngine], event_id: str, event_type: str, gateway: Optional[AuditGateway], integrity_check: Optional[AuditIntegrity], message: Optional[str], plan_token: Optional[AuditEventPlanToken], policy: Optional[AuditPolicy], severity: Optional[Severity], signature: Optional[str], signature_key_ref: Optional[str], timestamp: str, workflow: Optional[AuditWorkflow]) -> None:
        self.approval = approval
        self.artifacts = artifacts
        self.chain_hash = chain_hash
        self.engine = engine
        self.event_id = event_id
        self.event_type = event_type
        self.gateway = gateway
        self.integrity_check = integrity_check
        self.message = message
        self.plan_token = plan_token
        self.policy = policy
        self.severity = severity
        self.signature = signature
        self.signature_key_ref = signature_key_ref
        self.timestamp = timestamp
        self.workflow = workflow

    @staticmethod
    def from_dict(obj: Any) -> 'AuditEvent':
        assert isinstance(obj, dict)
        approval = from_union([AuditApproval.from_dict, from_none], obj.get("approval"))
        artifacts = from_union([lambda x: from_list(AuditArtifact.from_dict, x), from_none], obj.get("artifacts"))
        chain_hash = from_union([from_str, from_none], obj.get("chain_hash"))
        engine = from_union([AuditEngine.from_dict, from_none], obj.get("engine"))
        event_id = from_str(obj.get("event_id"))
        event_type = from_str(obj.get("event_type"))
        gateway = from_union([AuditGateway.from_dict, from_none], obj.get("gateway"))
        integrity_check = from_union([AuditIntegrity.from_dict, from_none], obj.get("integrity_check"))
        message = from_union([from_str, from_none], obj.get("message"))
        plan_token = from_union([AuditEventPlanToken.from_dict, from_none], obj.get("plan_token"))
        policy = from_union([AuditPolicy.from_dict, from_none], obj.get("policy"))
        severity = from_union([Severity, from_none], obj.get("severity"))
        signature = from_union([from_str, from_none], obj.get("signature"))
        signature_key_ref = from_union([from_str, from_none], obj.get("signature_key_ref"))
        timestamp = from_str(obj.get("timestamp"))
        workflow = from_union([AuditWorkflow.from_dict, from_none], obj.get("workflow"))
        return AuditEvent(approval, artifacts, chain_hash, engine, event_id, event_type, gateway, integrity_check, message, plan_token, policy, severity, signature, signature_key_ref, timestamp, workflow)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.approval is not None:
            result["approval"] = from_union([lambda x: to_class(AuditApproval, x), from_none], self.approval)
        if self.artifacts is not None:
            result["artifacts"] = from_union([lambda x: from_list(lambda x: to_class(AuditArtifact, x), x), from_none], self.artifacts)
        if self.chain_hash is not None:
            result["chain_hash"] = from_union([from_str, from_none], self.chain_hash)
        if self.engine is not None:
            result["engine"] = from_union([lambda x: to_class(AuditEngine, x), from_none], self.engine)
        result["event_id"] = from_str(self.event_id)
        result["event_type"] = from_str(self.event_type)
        if self.gateway is not None:
            result["gateway"] = from_union([lambda x: to_class(AuditGateway, x), from_none], self.gateway)
        if self.integrity_check is not None:
            result["integrity_check"] = from_union([lambda x: to_class(AuditIntegrity, x), from_none], self.integrity_check)
        if self.message is not None:
            result["message"] = from_union([from_str, from_none], self.message)
        if self.plan_token is not None:
            result["plan_token"] = from_union([lambda x: to_class(AuditEventPlanToken, x), from_none], self.plan_token)
        if self.policy is not None:
            result["policy"] = from_union([lambda x: to_class(AuditPolicy, x), from_none], self.policy)
        if self.severity is not None:
            result["severity"] = from_union([lambda x: to_enum(Severity, x), from_none], self.severity)
        if self.signature is not None:
            result["signature"] = from_union([from_str, from_none], self.signature)
        if self.signature_key_ref is not None:
            result["signature_key_ref"] = from_union([from_str, from_none], self.signature_key_ref)
        result["timestamp"] = from_str(self.timestamp)
        if self.workflow is not None:
            result["workflow"] = from_union([lambda x: to_class(AuditWorkflow, x), from_none], self.workflow)
        return result



def audit_event_from_dict(s: Any) -> AuditEvent:
    return AuditEvent.from_dict(s)



def audit_event_to_dict(x: AuditEvent) -> Any:
    return to_class(AuditEvent, x)


