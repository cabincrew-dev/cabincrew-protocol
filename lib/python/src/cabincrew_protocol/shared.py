from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Any, List, Optional, Dict, Union, TypeVar, Callable, Type, cast
import json
from datetime import datetime

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)

def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x



def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }



def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]



def from_none(x: Any) -> Any:
    assert x is None
    return x



def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False



def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()



def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x



def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)



def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x



def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value



class InputClass:
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'InputClass':
        assert isinstance(obj, dict)
        return InputClass()

    def to_dict(self) -> dict:
        result: dict = {}
        return result



def engine_schema_from_dict(s: Any) -> EngineSchema:
    return EngineSchema.from_dict(s)



def engine_schema_to_dict(x: EngineSchema) -> Any:
    return to_class(EngineSchema, x)



def llm_gateway_from_dict(s: Any) -> LlmGateway:
    return LlmGateway.from_dict(s)



def llm_gateway_to_dict(x: LlmGateway) -> Any:
    return to_class(LlmGateway, x)



def mcp_gateway_from_dict(s: Any) -> MCPGateway:
    return MCPGateway.from_dict(s)



def mcp_gateway_to_dict(x: MCPGateway) -> Any:
    return to_class(MCPGateway, x)



def orchestrator_schema_from_dict(s: Any) -> OrchestratorSchema:
    return OrchestratorSchema.from_dict(s)



def orchestrator_schema_to_dict(x: OrchestratorSchema) -> Any:
    return to_class(OrchestratorSchema, x)


