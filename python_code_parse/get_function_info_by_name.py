import ast
from typing import List, Optional
from python_code_parse.enums.special_arg import SpecialArg

from python_code_parse.exceptions import FunctionNotFoundException
from python_code_parse.models.function_arg import FunctionArg
from python_code_parse.models.function_info import FunctionInfo
from python_code_parse.replace_function_signature import (
    get_signature_end_index,
)
from python_code_parse.utils.get_function_arg_from_ast_arg import (
    get_function_arg_from_ast_arg,
)


def get_function_info_by_name(
    code: str, function_name: str, instance: Optional[int] = 0
) -> List[FunctionInfo]:
    """Get info about a function by name."""

    names_seen = dict()
    tree: ast.Module = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if function_name != node.name:
                continue

            current_function_instance = names_seen.get(function_name, 0)

            if instance and current_function_instance != instance:
                names_seen[function_name] = current_function_instance + 1
                continue

            args: List[FunctionArg] = []
            defaults: list[ast.expr] = node.args.defaults

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

            return FunctionInfo(
                name=function_name,
                args=args,
                return_type=ast.unparse(node.returns).strip()
                if node.returns
                else "",
                line=node.lineno,
                signature_end_line_index=get_signature_end_index(node),
                instance=current_function_instance,
            )

    raise FunctionNotFoundException(
        f"Function not found by name '{function_name} and instance {instance}"
    )
