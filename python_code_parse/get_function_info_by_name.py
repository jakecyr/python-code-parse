import ast
from typing import List
from python_code_parse.models.function_arg import FunctionArg
from python_code_parse.models.function_info import FunctionInfo
from python_code_parse.exceptions import FunctionNotFoundException


def get_function_info_by_name(code: str, function_name: str) -> FunctionInfo:
    """Get information about a function in a given code string."""

    tree: ast.Module = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name != function_name:
                continue

            args: List[FunctionArg] = []
            for arg in node.args.args:
                arg_str = arg.arg
                if arg.annotation:
                    arg_str += ": " + ast.unparse(arg.annotation).strip()
                    args.append(
                        FunctionArg(
                            name=arg.arg, annotation=ast.unparse(arg.annotation).strip()
                        )
                    )
                else:
                    args.append(FunctionArg(name=arg.arg, annotation=""))

            return FunctionInfo(
                name=node.name,
                args=args,
                return_type=ast.unparse(node.returns).strip() if node.returns else "",
                line=node.lineno,
            )

    raise FunctionNotFoundException(function_name)
