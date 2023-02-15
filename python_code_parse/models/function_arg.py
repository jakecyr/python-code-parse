from dataclasses import dataclass

from python_code_parse.enums.special_arg import SpecialArg


@dataclass
class FunctionArg:
    """A dataclass to hold information about a function argument."""

    name: str
    annotation: str = None
    default: str = None
    special: SpecialArg = None
