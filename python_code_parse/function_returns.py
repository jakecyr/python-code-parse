import ast


def function_returns(code: str, function_name: str, instance: int = 0) -> bool:
    """Check if a function returns a value or not"""

    names_seen = dict()
    tree: ast.Module = ast.parse(code)

    found_function = False
    function_start_line = 0
    function_end_line = 0

    for node in ast.walk(tree):
        if not found_function and isinstance(node, ast.FunctionDef):
            if function_name != node.name:
                continue

            current_function_instance = names_seen.get(function_name, 0)

            if instance and current_function_instance != instance:
                names_seen[function_name] = current_function_instance + 1
                continue

            function_start_line = node.lineno
            function_end_line = node.end_lineno
            found_function = True
        elif (
            found_function
            and isinstance(node, ast.Return)
            and node.lineno > function_start_line
            and node.end_lineno <= function_end_line
        ):
            return True

    return False
