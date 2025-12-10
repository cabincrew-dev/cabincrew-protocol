from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional, Dict, Union, TypeVar, Callable, Type, cast
import json
from datetime import datetime

from .shared import *

class PlanArtifactHash:
    hash: str
    name: str
    size: Optional[float]

    def __init__(self, hash: str, name: str, size: Optional[float]) -> None:
        self.hash = hash
        self.name = name
        self.size = size

    @staticmethod
    def from_dict(obj: Any) -> 'PlanArtifactHash':
        assert isinstance(obj, dict)
        hash = from_str(obj.get("hash"))
        name = from_str(obj.get("name"))
        size = from_union([from_float, from_none], obj.get("size"))
        return PlanArtifactHash(hash, name, size)

    def to_dict(self) -> dict:
        result: dict = {}
        result["hash"] = from_str(self.hash)
        result["name"] = from_str(self.name)
        if self.size is not None:
            result["size"] = from_union([to_float, from_none], self.size)
        return result



class PlanToken:
    """Cryptographic binding between a flight-plan and its subsequent take-off.
    Defined in schemas/draft/plan-token.schema.json
    """
    artifacts: List[PlanArtifactHash]
    """Per-artifact hashes that contributed to this plan token."""

    created_at: str
    """Timestamp when the plan was created (RFC3339)."""

    engine_id: str
    """Engine identity that produced this plan."""

    protocol_version: str
    """Engine protocol version used when this plan was produced."""

    token: str
    """Primary plan token identifier, e.g. SHA256 over all plan artifacts + context."""

    workspace_hash: str
    """Hash of the workspace state when the plan was created."""

    def __init__(self, artifacts: List[PlanArtifactHash], created_at: str, engine_id: str, protocol_version: str, token: str, workspace_hash: str) -> None:
        self.artifacts = artifacts
        self.created_at = created_at
        self.engine_id = engine_id
        self.protocol_version = protocol_version
        self.token = token
        self.workspace_hash = workspace_hash

    @staticmethod
    def from_dict(obj: Any) -> 'PlanToken':
        assert isinstance(obj, dict)
        artifacts = from_list(PlanArtifactHash.from_dict, obj.get("artifacts"))
        created_at = from_str(obj.get("created_at"))
        engine_id = from_str(obj.get("engine_id"))
        protocol_version = from_str(obj.get("protocol_version"))
        token = from_str(obj.get("token"))
        workspace_hash = from_str(obj.get("workspace_hash"))
        return PlanToken(artifacts, created_at, engine_id, protocol_version, token, workspace_hash)

    def to_dict(self) -> dict:
        result: dict = {}
        result["artifacts"] = from_list(lambda x: to_class(PlanArtifactHash, x), self.artifacts)
        result["created_at"] = from_str(self.created_at)
        result["engine_id"] = from_str(self.engine_id)
        result["protocol_version"] = from_str(self.protocol_version)
        result["token"] = from_str(self.token)
        result["workspace_hash"] = from_str(self.workspace_hash)
        return result



def plan_token_from_dict(s: Any) -> PlanToken:
    return PlanToken.from_dict(s)



def plan_token_to_dict(x: PlanToken) -> Any:
    return to_class(PlanToken, x)

