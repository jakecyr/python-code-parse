from dataclasses import dataclass
from typing import List
from python_code_parse.models.function_arg import FunctionArg


@dataclass
class FunctionInfo:
    """A dataclass to hold information about a function."""

    name: str
    args: List[FunctionArg]
    return_type: str
    line: int
