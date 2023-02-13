import ast
from typing import List

from python_code_parse.models.function_arg import FunctionArg
from python_code_parse.models.function_info import FunctionInfo
from python_code_parse.replace_function_signature import (
    get_signature_end_index,
)


def get_all_function_info_from_code(code: str) -> List[FunctionInfo]:
    """Get a list of functions found in a code string."""

    functions: List[FunctionInfo] = []
    tree: ast.Module = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args: List[FunctionArg] = []
            defaults = node.args.defaults

            while len(defaults) < len(node.args.args):
                defaults.insert(0, None)

            for i, arg in enumerate(node.args.args):
                arg_str = arg.arg

                if arg.annotation:
                    arg_str += ": " + ast.unparse(arg.annotation).strip()
                    arg_default = None

                    if defaults[i] is not None:
                        arg_default = ast.unparse(defaults[i]).strip()

                    args.append(
                        FunctionArg(
                            name=arg.arg,
                            annotation=ast.unparse(arg.annotation).strip(),
                            default=arg_default,
                        )
                    )
                else:
                    arg_default = None

                    if defaults[i] is not None:
                        arg_default = ast.unparse(defaults[i]).strip()

                    args.append(
                        FunctionArg(
                            name=arg.arg, annotation="", default=arg_default
                        )
                    )

            functions.append(
                FunctionInfo(
                    name=node.name,
                    args=args,
                    return_type=ast.unparse(node.returns).strip()
                    if node.returns
                    else "",
                    line=node.lineno,
                    signature_end_line_index=get_signature_end_index(node),
                )
            )
    return functions
