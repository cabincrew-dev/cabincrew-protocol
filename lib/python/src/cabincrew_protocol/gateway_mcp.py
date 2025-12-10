from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional, Dict, Union, TypeVar, Callable, Type, cast
import json
from datetime import datetime

from .shared import *

from .gateway_llm import LLMGatewayResponseDecision

class ParamsClass:
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'ParamsClass':
        assert isinstance(obj, dict)
        return ParamsClass()

    def to_dict(self) -> dict:
        result: dict = {}
        return result



class MCPGatewayRule:
    action: str
    match: ParamsClass
    metadata: Optional[ParamsClass]

    def __init__(self, action: str, match: ParamsClass, metadata: Optional[ParamsClass]) -> None:
        self.action = action
        self.match = match
        self.metadata = metadata

    @staticmethod
    def from_dict(obj: Any) -> 'MCPGatewayRule':
        assert isinstance(obj, dict)
        action = from_str(obj.get("action"))
        match = ParamsClass.from_dict(obj.get("match"))
        metadata = from_union([ParamsClass.from_dict, from_none], obj.get("metadata"))
        return MCPGatewayRule(action, match, metadata)

    def to_dict(self) -> dict:
        result: dict = {}
        result["action"] = from_str(self.action)
        result["match"] = to_class(ParamsClass, self.match)
        if self.metadata is not None:
            result["metadata"] = from_union([lambda x: to_class(ParamsClass, x), from_none], self.metadata)
        return result



class MCPGatewayPolicyConfig:
    onnx_models: Optional[List[str]]
    opa_policies: Optional[List[str]]
    rules: Optional[List[MCPGatewayRule]]

    def __init__(self, onnx_models: Optional[List[str]], opa_policies: Optional[List[str]], rules: Optional[List[MCPGatewayRule]]) -> None:
        self.onnx_models = onnx_models
        self.opa_policies = opa_policies
        self.rules = rules

    @staticmethod
    def from_dict(obj: Any) -> 'MCPGatewayPolicyConfig':
        assert isinstance(obj, dict)
        onnx_models = from_union([lambda x: from_list(from_str, x), from_none], obj.get("onnx_models"))
        opa_policies = from_union([lambda x: from_list(from_str, x), from_none], obj.get("opa_policies"))
        rules = from_union([lambda x: from_list(MCPGatewayRule.from_dict, x), from_none], obj.get("rules"))
        return MCPGatewayPolicyConfig(onnx_models, opa_policies, rules)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.onnx_models is not None:
            result["onnx_models"] = from_union([lambda x: from_list(from_str, x), from_none], self.onnx_models)
        if self.opa_policies is not None:
            result["opa_policies"] = from_union([lambda x: from_list(from_str, x), from_none], self.opa_policies)
        if self.rules is not None:
            result["rules"] = from_union([lambda x: from_list(lambda x: to_class(MCPGatewayRule, x), x), from_none], self.rules)
        return result



class MCPGatewayRequest:
    context: Optional[ParamsClass]
    method: str
    params: Optional[ParamsClass]
    request_id: str
    server_id: str
    source: Optional[str]
    timestamp: str

    def __init__(self, context: Optional[ParamsClass], method: str, params: Optional[ParamsClass], request_id: str, server_id: str, source: Optional[str], timestamp: str) -> None:
        self.context = context
        self.method = method
        self.params = params
        self.request_id = request_id
        self.server_id = server_id
        self.source = source
        self.timestamp = timestamp

    @staticmethod
    def from_dict(obj: Any) -> 'MCPGatewayRequest':
        assert isinstance(obj, dict)
        context = from_union([ParamsClass.from_dict, from_none], obj.get("context"))
        method = from_str(obj.get("method"))
        params = from_union([ParamsClass.from_dict, from_none], obj.get("params"))
        request_id = from_str(obj.get("request_id"))
        server_id = from_str(obj.get("server_id"))
        source = from_union([from_str, from_none], obj.get("source"))
        timestamp = from_str(obj.get("timestamp"))
        return MCPGatewayRequest(context, method, params, request_id, server_id, source, timestamp)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.context is not None:
            result["context"] = from_union([lambda x: to_class(ParamsClass, x), from_none], self.context)
        result["method"] = from_str(self.method)
        if self.params is not None:
            result["params"] = from_union([lambda x: to_class(ParamsClass, x), from_none], self.params)
        result["request_id"] = from_str(self.request_id)
        result["server_id"] = from_str(self.server_id)
        if self.source is not None:
            result["source"] = from_union([from_str, from_none], self.source)
        result["timestamp"] = from_str(self.timestamp)
        return result



class MCPGatewayResponseApproval:
    approval_id: Optional[str]
    reason: Optional[str]
    required_role: Optional[str]

    def __init__(self, approval_id: Optional[str], reason: Optional[str], required_role: Optional[str]) -> None:
        self.approval_id = approval_id
        self.reason = reason
        self.required_role = required_role

    @staticmethod
    def from_dict(obj: Any) -> 'MCPGatewayResponseApproval':
        assert isinstance(obj, dict)
        approval_id = from_union([from_str, from_none], obj.get("approval_id"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        required_role = from_union([from_str, from_none], obj.get("required_role"))
        return MCPGatewayResponseApproval(approval_id, reason, required_role)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.approval_id is not None:
            result["approval_id"] = from_union([from_str, from_none], self.approval_id)
        if self.reason is not None:
            result["reason"] = from_union([from_str, from_none], self.reason)
        if self.required_role is not None:
            result["required_role"] = from_union([from_str, from_none], self.required_role)
        return result



class MCPGatewayResponse:
    approval: Optional[MCPGatewayResponseApproval]
    decision: LLMGatewayResponseDecision
    request_id: str
    rewritten_request: Optional[ParamsClass]
    timestamp: str
    violations: Optional[List[str]]
    warnings: Optional[List[str]]

    def __init__(self, approval: Optional[MCPGatewayResponseApproval], decision: LLMGatewayResponseDecision, request_id: str, rewritten_request: Optional[ParamsClass], timestamp: str, violations: Optional[List[str]], warnings: Optional[List[str]]) -> None:
        self.approval = approval
        self.decision = decision
        self.request_id = request_id
        self.rewritten_request = rewritten_request
        self.timestamp = timestamp
        self.violations = violations
        self.warnings = warnings

    @staticmethod
    def from_dict(obj: Any) -> 'MCPGatewayResponse':
        assert isinstance(obj, dict)
        approval = from_union([MCPGatewayResponseApproval.from_dict, from_none], obj.get("approval"))
        decision = LLMGatewayResponseDecision(obj.get("decision"))
        request_id = from_str(obj.get("request_id"))
        rewritten_request = from_union([ParamsClass.from_dict, from_none], obj.get("rewritten_request"))
        timestamp = from_str(obj.get("timestamp"))
        violations = from_union([lambda x: from_list(from_str, x), from_none], obj.get("violations"))
        warnings = from_union([lambda x: from_list(from_str, x), from_none], obj.get("warnings"))
        return MCPGatewayResponse(approval, decision, request_id, rewritten_request, timestamp, violations, warnings)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.approval is not None:
            result["approval"] = from_union([lambda x: to_class(MCPGatewayResponseApproval, x), from_none], self.approval)
        result["decision"] = to_enum(LLMGatewayResponseDecision, self.decision)
        result["request_id"] = from_str(self.request_id)
        if self.rewritten_request is not None:
            result["rewritten_request"] = from_union([lambda x: to_class(ParamsClass, x), from_none], self.rewritten_request)
        result["timestamp"] = from_str(self.timestamp)
        if self.violations is not None:
            result["violations"] = from_union([lambda x: from_list(from_str, x), from_none], self.violations)
        if self.warnings is not None:
            result["warnings"] = from_union([lambda x: from_list(from_str, x), from_none], self.warnings)
        return result


