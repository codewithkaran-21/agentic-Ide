from __future__ import annotations
import abc 
from  enum import Enum
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field
from pydantic import BaseModel, ValidationError

@dataclass
class ToolInvocation:
    params : dict[str,Any]
    cwd : Path

@dataclass
class ToolResult:
    success : bool 
    output : str 
    error : str | None = None 
    metadata : dict[str , Any] = field(default_factory=dict)

@dataclass
class ToolConfirmation:
    tool_name : str 
    params : dict[str,Any]
    description : str 
    

class ToolKind(str , Enum):
    READ = "read"
    WRITE = "write"
    SHELL = "shell"
    NETWORK = "network"
    MEMORY ="memory"
    MCP = "mcp"

class Tool(abc.ABC):
    name : str = "base_tool"
    description : str = "Base Tool"

    kind : ToolKind = ToolKind.READ

    def __init__(self) -> None:
        pass

    @property    
    def schema(self) -> dict[str,Any] | type["BaseModel"]:
        raise NotImplementedError("Tool must define system property or class attributes")

    @abc.abstractmethod
    async def execute(self , invocation : ToolInvocation) -> ToolResult:
        pass

    def validate_params(self , params : dict[str,Any]) -> list[str]:
        schema = self.schema()
        if isinstance(schema,type) and issubclass(schema , BaseModel):
            try:
                schema(**params)
            except ValidationError as e:
                errors = []
                for error in e.errors:
                    field = ".".join(str(x) for x in error.get("loc",[]))
                    msg = error.get("msg","ValidationError")
                    errors.append(f"Parameter `{field}`:{msg}")

                return errors
            except Exception as e:
                return [str(e)]

        return []

    def is_mutating(self , params : dict[str,Any]) -> bool:
        return self.kind in {
            ToolKind.WRITE,
            ToolKind.SHELL,
            ToolKind.NETWORK,
            ToolKind.MCP
        }

    async def get_confirmation(self , invocation : ToolInvocation) -> ToolInvocation | None : 
        if not self.is_mutating(invocation.params):
            return None 
        return ToolConfirmation()




    
                
