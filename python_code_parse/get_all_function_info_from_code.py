import ast
from typing import List
from python_code_parse.enums.special_arg import SpecialArg

from python_code_parse.models.function_arg import FunctionArg
from python_code_parse.models.function_info import FunctionInfo
from python_code_parse.replace_function_signature import (
    get_signature_end_index,
)
from python_code_parse.utils.get_function_arg_from_ast_arg import (
    get_function_arg_from_ast_arg,
)


def get_all_function_info_from_code(code: str) -> List[FunctionInfo]:
    """Get a list of functions found in a code string."""

    functions: List[FunctionInfo] = []
    names_seen = dict()
    tree: ast.Module = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args: List[FunctionArg] = []
            defaults: list[ast.expr] = node.args.defaults
            function_name: str = node.name

            if names_seen.get(function_name):
                names_seen[function_name] += 1
            else:
                names_seen[function_name] = 1

            while len(defaults) < len(node.args.args):
                defaults.insert(0, None)

            for i, arg in enumerate(node.args.args):
                args.append(get_function_arg_from_ast_arg(arg, defaults[i]))

            # add *args if exists
            if node.args.vararg:
                args.append(
                    get_function_arg_from_ast_arg(
                        node.args.vararg, None, SpecialArg.vararg
                    )
                )

            # add *kwargs if exists
            if node.args.kwarg:
                args.append(
                    get_function_arg_from_ast_arg(
                        node.args.kwarg, None, SpecialArg.kwarg
                    )
                )

            # add kwonlyargs if exist
            for arg in node.args.kwonlyargs:
                args.append(
                    get_function_arg_from_ast_arg(
                        arg, None, SpecialArg.kwonlyargs
                    )
                )

            functions.append(
                FunctionInfo(
                    name=function_name,
                    args=args,
                    return_type=ast.unparse(node.returns).strip()
                    if node.returns
                    else "",
                    line=node.lineno,
                    signature_end_line_index=get_signature_end_index(node),
                    instance=names_seen.get(function_name) - 1,
                )
            )

    return functions
