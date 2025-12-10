from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional, Dict, Union, TypeVar, Callable, Type, cast
import json
from datetime import datetime

from .shared import *

class LLMGatewayRule:
    action: str
    match: InputClass
    metadata: Optional[InputClass]

    def __init__(self, action: str, match: InputClass, metadata: Optional[InputClass]) -> None:
        self.action = action
        self.match = match
        self.metadata = metadata

    @staticmethod
    def from_dict(obj: Any) -> 'LLMGatewayRule':
        assert isinstance(obj, dict)
        action = from_str(obj.get("action"))
        match = InputClass.from_dict(obj.get("match"))
        metadata = from_union([InputClass.from_dict, from_none], obj.get("metadata"))
        return LLMGatewayRule(action, match, metadata)

    def to_dict(self) -> dict:
        result: dict = {}
        result["action"] = from_str(self.action)
        result["match"] = to_class(InputClass, self.match)
        if self.metadata is not None:
            result["metadata"] = from_union([lambda x: to_class(InputClass, x), from_none], self.metadata)
        return result



class LLMGatewayPolicyConfig:
    model_routing: Optional[InputClass]
    onnx_models: Optional[List[str]]
    opa_policies: Optional[List[str]]
    rules: Optional[List[LLMGatewayRule]]

    def __init__(self, model_routing: Optional[InputClass], onnx_models: Optional[List[str]], opa_policies: Optional[List[str]], rules: Optional[List[LLMGatewayRule]]) -> None:
        self.model_routing = model_routing
        self.onnx_models = onnx_models
        self.opa_policies = opa_policies
        self.rules = rules

    @staticmethod
    def from_dict(obj: Any) -> 'LLMGatewayPolicyConfig':
        assert isinstance(obj, dict)
        model_routing = from_union([InputClass.from_dict, from_none], obj.get("model_routing"))
        onnx_models = from_union([lambda x: from_list(from_str, x), from_none], obj.get("onnx_models"))
        opa_policies = from_union([lambda x: from_list(from_str, x), from_none], obj.get("opa_policies"))
        rules = from_union([lambda x: from_list(LLMGatewayRule.from_dict, x), from_none], obj.get("rules"))
        return LLMGatewayPolicyConfig(model_routing, onnx_models, opa_policies, rules)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.model_routing is not None:
            result["model_routing"] = from_union([lambda x: to_class(InputClass, x), from_none], self.model_routing)
        if self.onnx_models is not None:
            result["onnx_models"] = from_union([lambda x: from_list(from_str, x), from_none], self.onnx_models)
        if self.opa_policies is not None:
            result["opa_policies"] = from_union([lambda x: from_list(from_str, x), from_none], self.opa_policies)
        if self.rules is not None:
            result["rules"] = from_union([lambda x: from_list(lambda x: to_class(LLMGatewayRule, x), x), from_none], self.rules)
        return result



class LLMGatewayRequest:
    context: Optional[InputClass]
    input: InputClass
    model: str
    provider: Optional[str]
    request_id: str
    source: Optional[str]
    timestamp: str

    def __init__(self, context: Optional[InputClass], input: InputClass, model: str, provider: Optional[str], request_id: str, source: Optional[str], timestamp: str) -> None:
        self.context = context
        self.input = input
        self.model = model
        self.provider = provider
        self.request_id = request_id
        self.source = source
        self.timestamp = timestamp

    @staticmethod
    def from_dict(obj: Any) -> 'LLMGatewayRequest':
        assert isinstance(obj, dict)
        context = from_union([InputClass.from_dict, from_none], obj.get("context"))
        input = InputClass.from_dict(obj.get("input"))
        model = from_str(obj.get("model"))
        provider = from_union([from_str, from_none], obj.get("provider"))
        request_id = from_str(obj.get("request_id"))
        source = from_union([from_str, from_none], obj.get("source"))
        timestamp = from_str(obj.get("timestamp"))
        return LLMGatewayRequest(context, input, model, provider, request_id, source, timestamp)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.context is not None:
            result["context"] = from_union([lambda x: to_class(InputClass, x), from_none], self.context)
        result["input"] = to_class(InputClass, self.input)
        result["model"] = from_str(self.model)
        if self.provider is not None:
            result["provider"] = from_union([from_str, from_none], self.provider)
        result["request_id"] = from_str(self.request_id)
        if self.source is not None:
            result["source"] = from_union([from_str, from_none], self.source)
        result["timestamp"] = from_str(self.timestamp)
        return result



class LLMGatewayResponseApproval:
    approval_id: Optional[str]
    reason: Optional[str]
    required_role: Optional[str]

    def __init__(self, approval_id: Optional[str], reason: Optional[str], required_role: Optional[str]) -> None:
        self.approval_id = approval_id
        self.reason = reason
        self.required_role = required_role

    @staticmethod
    def from_dict(obj: Any) -> 'LLMGatewayResponseApproval':
        assert isinstance(obj, dict)
        approval_id = from_union([from_str, from_none], obj.get("approval_id"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        required_role = from_union([from_str, from_none], obj.get("required_role"))
        return LLMGatewayResponseApproval(approval_id, reason, required_role)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.approval_id is not None:
            result["approval_id"] = from_union([from_str, from_none], self.approval_id)
        if self.reason is not None:
            result["reason"] = from_union([from_str, from_none], self.reason)
        if self.required_role is not None:
            result["required_role"] = from_union([from_str, from_none], self.required_role)
        return result



class LLMGatewayResponseDecision(Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"
    WARN = "warn"



class LLMGatewayResponse:
    approval: Optional[LLMGatewayResponseApproval]
    decision: LLMGatewayResponseDecision
    gateway_payload: Optional[InputClass]
    request_id: str
    rewritten_input: Optional[InputClass]
    routed_model: Optional[str]
    timestamp: str
    violations: Optional[List[str]]
    warnings: Optional[List[str]]

    def __init__(self, approval: Optional[LLMGatewayResponseApproval], decision: LLMGatewayResponseDecision, gateway_payload: Optional[InputClass], request_id: str, rewritten_input: Optional[InputClass], routed_model: Optional[str], timestamp: str, violations: Optional[List[str]], warnings: Optional[List[str]]) -> None:
        self.approval = approval
        self.decision = decision
        self.gateway_payload = gateway_payload
        self.request_id = request_id
        self.rewritten_input = rewritten_input
        self.routed_model = routed_model
        self.timestamp = timestamp
        self.violations = violations
        self.warnings = warnings

    @staticmethod
    def from_dict(obj: Any) -> 'LLMGatewayResponse':
        assert isinstance(obj, dict)
        approval = from_union([LLMGatewayResponseApproval.from_dict, from_none], obj.get("approval"))
        decision = LLMGatewayResponseDecision(obj.get("decision"))
        gateway_payload = from_union([InputClass.from_dict, from_none], obj.get("gateway_payload"))
        request_id = from_str(obj.get("request_id"))
        rewritten_input = from_union([InputClass.from_dict, from_none], obj.get("rewritten_input"))
        routed_model = from_union([from_str, from_none], obj.get("routed_model"))
        timestamp = from_str(obj.get("timestamp"))
        violations = from_union([lambda x: from_list(from_str, x), from_none], obj.get("violations"))
        warnings = from_union([lambda x: from_list(from_str, x), from_none], obj.get("warnings"))
        return LLMGatewayResponse(approval, decision, gateway_payload, request_id, rewritten_input, routed_model, timestamp, violations, warnings)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.approval is not None:
            result["approval"] = from_union([lambda x: to_class(LLMGatewayResponseApproval, x), from_none], self.approval)
        result["decision"] = to_enum(LLMGatewayResponseDecision, self.decision)
        if self.gateway_payload is not None:
            result["gateway_payload"] = from_union([lambda x: to_class(InputClass, x), from_none], self.gateway_payload)
        result["request_id"] = from_str(self.request_id)
        if self.rewritten_input is not None:
            result["rewritten_input"] = from_union([lambda x: to_class(InputClass, x), from_none], self.rewritten_input)
        if self.routed_model is not None:
            result["routed_model"] = from_union([from_str, from_none], self.routed_model)
        result["timestamp"] = from_str(self.timestamp)
        if self.violations is not None:
            result["violations"] = from_union([lambda x: from_list(from_str, x), from_none], self.violations)
        if self.warnings is not None:
            result["warnings"] = from_union([lambda x: from_list(from_str, x), from_none], self.warnings)
        return result


