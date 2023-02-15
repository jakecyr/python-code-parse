import ast
from typing import Any, Optional

from python_code_parse.enums.special_arg import SpecialArg
from python_code_parse.models import FunctionArg


def get_function_arg_from_ast_arg(
    arg, default: Optional[Any] = None, special: SpecialArg = None
):
    arg_default = None

    if default is not None:
        arg_default = ast.unparse(default).strip()

    return FunctionArg(
        name=arg.arg,
        annotation=ast.unparse(arg.annotation).strip()
        if arg.annotation
        else "",
        default=arg_default,
        special=special,
    )
