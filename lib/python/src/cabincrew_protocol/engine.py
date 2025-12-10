from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional, Dict, Union, TypeVar, Callable, Type, cast
import json
from datetime import datetime

from .shared import *

class EngineMeta:
    step_id: str
    workflow_id: str

    def __init__(self, step_id: str, workflow_id: str) -> None:
        self.step_id = step_id
        self.workflow_id = workflow_id

    @staticmethod
    def from_dict(obj: Any) -> 'EngineMeta':
        assert isinstance(obj, dict)
        step_id = from_str(obj.get("step_id"))
        workflow_id = from_str(obj.get("workflow_id"))
        return EngineMeta(step_id, workflow_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["step_id"] = from_str(self.step_id)
        result["workflow_id"] = from_str(self.workflow_id)
        return result



class EngineOrchestrator:
    artifacts_salt: Optional[str]
    run_index: Optional[float]
    workspace_hash: Optional[str]

    def __init__(self, artifacts_salt: Optional[str], run_index: Optional[float], workspace_hash: Optional[str]) -> None:
        self.artifacts_salt = artifacts_salt
        self.run_index = run_index
        self.workspace_hash = workspace_hash

    @staticmethod
    def from_dict(obj: Any) -> 'EngineOrchestrator':
        assert isinstance(obj, dict)
        artifacts_salt = from_union([from_str, from_none], obj.get("artifacts_salt"))
        run_index = from_union([from_float, from_none], obj.get("run_index"))
        workspace_hash = from_union([from_str, from_none], obj.get("workspace_hash"))
        return EngineOrchestrator(artifacts_salt, run_index, workspace_hash)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.artifacts_salt is not None:
            result["artifacts_salt"] = from_union([from_str, from_none], self.artifacts_salt)
        if self.run_index is not None:
            result["run_index"] = from_union([to_float, from_none], self.run_index)
        if self.workspace_hash is not None:
            result["workspace_hash"] = from_union([from_str, from_none], self.workspace_hash)
        return result



class EngineInput:
    """Input delivered via STDIN or CABINCREW_INPUT_FILE.
    Defined in schemas/draft/engine.schema.json
    """
    allowed_secrets: Optional[List[str]]
    config: Optional[Dict[str, Any]]
    context: Optional[Dict[str, Any]]
    expected_plan_token: Optional[str]
    identity_token: Optional[str]
    """Ephemeral identity token (e.g. OIDC, JWT) for the workload.
    Preferred over static secrets.
    """
    meta: EngineMeta
    mode: str
    """Execution mode: 'flight-plan' or 'take-off'."""

    orchestrator: Optional[EngineOrchestrator]
    protocol_version: str
    secrets: Optional[Dict[str, Any]]

    def __init__(self, allowed_secrets: Optional[List[str]], config: Optional[Dict[str, Any]], context: Optional[Dict[str, Any]], expected_plan_token: Optional[str], identity_token: Optional[str], meta: EngineMeta, mode: str, orchestrator: Optional[EngineOrchestrator], protocol_version: str, secrets: Optional[Dict[str, Any]]) -> None:
        self.allowed_secrets = allowed_secrets
        self.config = config
        self.context = context
        self.expected_plan_token = expected_plan_token
        self.identity_token = identity_token
        self.meta = meta
        self.mode = mode
        self.orchestrator = orchestrator
        self.protocol_version = protocol_version
        self.secrets = secrets

    @staticmethod
    def from_dict(obj: Any) -> 'EngineInput':
        assert isinstance(obj, dict)
        allowed_secrets = from_union([lambda x: from_list(from_str, x), from_none], obj.get("allowed_secrets"))
        config = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("config"))
        context = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("context"))
        expected_plan_token = from_union([from_str, from_none], obj.get("expected_plan_token"))
        identity_token = from_union([from_str, from_none], obj.get("identity_token"))
        meta = EngineMeta.from_dict(obj.get("meta"))
        mode = from_str(obj.get("mode"))
        orchestrator = from_union([EngineOrchestrator.from_dict, from_none], obj.get("orchestrator"))
        protocol_version = from_str(obj.get("protocol_version"))
        secrets = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("secrets"))
        return EngineInput(allowed_secrets, config, context, expected_plan_token, identity_token, meta, mode, orchestrator, protocol_version, secrets)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.allowed_secrets is not None:
            result["allowed_secrets"] = from_union([lambda x: from_list(from_str, x), from_none], self.allowed_secrets)
        if self.config is not None:
            result["config"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.config)
        if self.context is not None:
            result["context"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.context)
        if self.expected_plan_token is not None:
            result["expected_plan_token"] = from_union([from_str, from_none], self.expected_plan_token)
        if self.identity_token is not None:
            result["identity_token"] = from_union([from_str, from_none], self.identity_token)
        result["meta"] = to_class(EngineMeta, self.meta)
        result["mode"] = from_str(self.mode)
        if self.orchestrator is not None:
            result["orchestrator"] = from_union([lambda x: to_class(EngineOrchestrator, x), from_none], self.orchestrator)
        result["protocol_version"] = from_str(self.protocol_version)
        if self.secrets is not None:
            result["secrets"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.secrets)
        return result



class EngineArtifact:
    hash: str
    name: str
    path: str
    role: str
    size: Optional[float]

    def __init__(self, hash: str, name: str, path: str, role: str, size: Optional[float]) -> None:
        self.hash = hash
        self.name = name
        self.path = path
        self.role = role
        self.size = size

    @staticmethod
    def from_dict(obj: Any) -> 'EngineArtifact':
        assert isinstance(obj, dict)
        hash = from_str(obj.get("hash"))
        name = from_str(obj.get("name"))
        path = from_str(obj.get("path"))
        role = from_str(obj.get("role"))
        size = from_union([from_float, from_none], obj.get("size"))
        return EngineArtifact(hash, name, path, role, size)

    def to_dict(self) -> dict:
        result: dict = {}
        result["hash"] = from_str(self.hash)
        result["name"] = from_str(self.name)
        result["path"] = from_str(self.path)
        result["role"] = from_str(self.role)
        if self.size is not None:
            result["size"] = from_union([to_float, from_none], self.size)
        return result



class EngineMetric:
    name: str
    tags: Optional[Dict[str, Any]]
    value: float

    def __init__(self, name: str, tags: Optional[Dict[str, Any]], value: float) -> None:
        self.name = name
        self.tags = tags
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'EngineMetric':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        tags = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("tags"))
        value = from_float(obj.get("value"))
        return EngineMetric(name, tags, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        if self.tags is not None:
            result["tags"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.tags)
        result["value"] = to_float(self.value)
        return result



class EngineOutput:
    """Output delivered via STDOUT or CABINCREW_OUTPUT_FILE.
    Defined in schemas/draft/engine.schema.json
    """
    artifacts: Optional[List[EngineArtifact]]
    diagnostics: Any
    engine_id: str
    error: Optional[str]
    metrics: Optional[List[EngineMetric]]
    mode: str
    plan_token: Optional[str]
    """SHA256 hash referencing a plan-token.json file."""

    protocol_version: str
    receipt_id: str
    status: str
    """Execution status: 'success' or 'failure'."""

    warnings: Optional[List[str]]

    def __init__(self, artifacts: Optional[List[EngineArtifact]], diagnostics: Any, engine_id: str, error: Optional[str], metrics: Optional[List[EngineMetric]], mode: str, plan_token: Optional[str], protocol_version: str, receipt_id: str, status: str, warnings: Optional[List[str]]) -> None:
        self.artifacts = artifacts
        self.diagnostics = diagnostics
        self.engine_id = engine_id
        self.error = error
        self.metrics = metrics
        self.mode = mode
        self.plan_token = plan_token
        self.protocol_version = protocol_version
        self.receipt_id = receipt_id
        self.status = status
        self.warnings = warnings

    @staticmethod
    def from_dict(obj: Any) -> 'EngineOutput':
        assert isinstance(obj, dict)
        artifacts = from_union([lambda x: from_list(EngineArtifact.from_dict, x), from_none], obj.get("artifacts"))
        diagnostics = obj.get("diagnostics")
        engine_id = from_str(obj.get("engine_id"))
        error = from_union([from_str, from_none], obj.get("error"))
        metrics = from_union([lambda x: from_list(EngineMetric.from_dict, x), from_none], obj.get("metrics"))
        mode = from_str(obj.get("mode"))
        plan_token = from_union([from_str, from_none], obj.get("plan_token"))
        protocol_version = from_str(obj.get("protocol_version"))
        receipt_id = from_str(obj.get("receipt_id"))
        status = from_str(obj.get("status"))
        warnings = from_union([lambda x: from_list(from_str, x), from_none], obj.get("warnings"))
        return EngineOutput(artifacts, diagnostics, engine_id, error, metrics, mode, plan_token, protocol_version, receipt_id, status, warnings)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.artifacts is not None:
            result["artifacts"] = from_union([lambda x: from_list(lambda x: to_class(EngineArtifact, x), x), from_none], self.artifacts)
        if self.diagnostics is not None:
            result["diagnostics"] = self.diagnostics
        result["engine_id"] = from_str(self.engine_id)
        if self.error is not None:
            result["error"] = from_union([from_str, from_none], self.error)
        if self.metrics is not None:
            result["metrics"] = from_union([lambda x: from_list(lambda x: to_class(EngineMetric, x), x), from_none], self.metrics)
        result["mode"] = from_str(self.mode)
        if self.plan_token is not None:
            result["plan_token"] = from_union([from_str, from_none], self.plan_token)
        result["protocol_version"] = from_str(self.protocol_version)
        result["receipt_id"] = from_str(self.receipt_id)
        result["status"] = from_str(self.status)
        if self.warnings is not None:
            result["warnings"] = from_union([lambda x: from_list(from_str, x), from_none], self.warnings)
        return result



class EngineOutputClass:
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'EngineOutputClass':
        assert isinstance(obj, dict)
        return EngineOutputClass()

    def to_dict(self) -> dict:
        result: dict = {}
        return result



class Mode(Enum):
    FLIGHT_PLAN = "flight-plan"
    TAKE_OFF = "take-off"


