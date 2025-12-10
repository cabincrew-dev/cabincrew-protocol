from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional, Dict, Union, TypeVar, Callable, Type, cast
import json
from datetime import datetime

from .shared import *

class ArtifactMetadata:
    """Arbitrary metadata. Optional."""

    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'ArtifactMetadata':
        assert isinstance(obj, dict)
        return ArtifactMetadata()

    def to_dict(self) -> dict:
        result: dict = {}
        return result



class Artifact:
    """Canonical artifact interface.
    Defined in schemas/draft/artifact.schema.json
    """
    action: str
    """Operation to perform with this artifact (create, update, delete, apply, execute, etc).
    Free-form and engine-defined.
    """
    artifact_type: str
    """Type of artifact (file, diff, patch, action, message, etc). Free-form and engine-defined."""

    body: Optional[Union[Dict[str, Any], List[Any], str]]
    """Inline content for small artifacts.
    Can be string, object, array, or null.
    """
    body_file: Optional[str]
    """Indicates an external data file within the artifact directory."""

    metadata: Optional[ArtifactMetadata]
    """Arbitrary metadata. Optional."""

    mime: str
    """MIME type describing content."""

    target: Optional[str]
    """Path, resource, or identifier this artifact applies to. Optional."""

    def __init__(self, action: str, artifact_type: str, body: Optional[Union[Dict[str, Any], List[Any], str]], body_file: Optional[str], metadata: Optional[ArtifactMetadata], mime: str, target: Optional[str]) -> None:
        self.action = action
        self.artifact_type = artifact_type
        self.body = body
        self.body_file = body_file
        self.metadata = metadata
        self.mime = mime
        self.target = target

    @staticmethod
    def from_dict(obj: Any) -> 'Artifact':
        assert isinstance(obj, dict)
        action = from_str(obj.get("action"))
        artifact_type = from_str(obj.get("artifact_type"))
        body = from_union([lambda x: from_dict(lambda x: x, x), lambda x: from_list(lambda x: x, x), from_none, from_str], obj.get("body"))
        body_file = from_union([from_str, from_none], obj.get("body_file"))
        metadata = from_union([ArtifactMetadata.from_dict, from_none], obj.get("metadata"))
        mime = from_str(obj.get("mime"))
        target = from_union([from_str, from_none], obj.get("target"))
        return Artifact(action, artifact_type, body, body_file, metadata, mime, target)

    def to_dict(self) -> dict:
        result: dict = {}
        result["action"] = from_str(self.action)
        result["artifact_type"] = from_str(self.artifact_type)
        if self.body is not None:
            result["body"] = from_union([lambda x: from_dict(lambda x: x, x), lambda x: from_list(lambda x: x, x), from_none, from_str], self.body)
        if self.body_file is not None:
            result["body_file"] = from_union([from_str, from_none], self.body_file)
        if self.metadata is not None:
            result["metadata"] = from_union([lambda x: to_class(ArtifactMetadata, x), from_none], self.metadata)
        result["mime"] = from_str(self.mime)
        if self.target is not None:
            result["target"] = from_union([from_str, from_none], self.target)
        return result



def artifact_from_dict(s: Any) -> Artifact:
    return Artifact.from_dict(s)



def artifact_to_dict(x: Artifact) -> Any:
    return to_class(Artifact, x)


