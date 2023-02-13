import ast
from python_code_parse import (
    FunctionArg,
    FunctionInfo,
    replace_function_signature,
)

from python_code_parse.replace_function_signature import (
    get_signature_end_index,
)

multi_line_signature = '''
class Person:
    def __init__(
        self,
        name: str,
        age: int,
        job: str
    ):
        """This function is a constructor for a new person."""
        self.name = name
        self.age = age

    def __str__(self):
        return f"Person(name={self.name}, age={self.age})"

    def __repr__(self):
        return f"Person(name={self.name}, age={self.age})"

    def get_age(
        self,
    ):
        return self.age
'''


def test_get_signature_end_index_returns_correct_length():
    tree: ast.Module = ast.parse(multi_line_signature)
    init_function_def: ast.FunctionDef = tree.body[0].body[0]
    assert get_signature_end_index(init_function_def) == 7

    str_function_def: ast.FunctionDef = tree.body[0].body[1]
    assert get_signature_end_index(str_function_def) == 12

    rep_function_def: ast.FunctionDef = tree.body[0].body[2]
    assert get_signature_end_index(rep_function_def) == 15

    get_age_function_def = tree.body[0].body[3]
    assert get_signature_end_index(get_age_function_def) == 20


def test_replaces_the_correct_line():
    multi_long_function = """def test(a: int, b: float) -> float:\n\tpass"""
    multi_long_function += (
        """\n\ndef test2(a: int, b: float) -> float:\n\tpass"""
    )

    result = replace_function_signature(
        multi_long_function,
        FunctionInfo(
            "test2", [], "float", line=None, signature_end_line_index=None
        ),
    )

    lines = result.splitlines()

    assert lines[0] == "def test(a: int, b: float) -> float:"
    assert lines[1] == "\tpass"
    assert lines[2] == ""
    assert lines[3] == "def test2() -> float:"
    assert lines[4] == "\tpass"


def test_replaces_with_default_args():
    multi_long_function = (
        """def test(a: int = 1, b: float = 2) -> float:\n\tpass"""
    )
    multi_long_function += """\n\ndef test2(a = 1, b = 2) -> float:\n\tpass"""
    multi_long_function += """\n\ndef test3(a, b) -> float:\n\tpass"""

    result = replace_function_signature(
        multi_long_function,
        FunctionInfo(
            "test2",
            [FunctionArg("a", None, 1)],
            "float",
            line=None,
            signature_end_line_index=None,
        ),
    )

    result = replace_function_signature(
        result,
        FunctionInfo(
            "test3",
            [FunctionArg("a", "Any", 1), FunctionArg("b", "Any", 2)],
            "float",
            line=None,
            signature_end_line_index=None,
        ),
    )

    lines = result.splitlines()

    assert lines[0] == "def test(a: int = 1, b: float = 2) -> float:"
    assert lines[1] == "\tpass"
    assert lines[2] == ""
    assert lines[3] == "def test2(a = 1) -> float:"
    assert lines[4] == "\tpass"
    assert lines[6] == 'def test3(a: Any = 1, b: Any = 2) -> float:'
    assert lines[7] == '\tpass'


def test_replaces_the_correct_line_with_indentation():
    multi_long_function = "class Person:\n"
    multi_long_function += "  def __init__(self, name: str, age: int):\n"
    multi_long_function += "    self.name = name\n"

    result = replace_function_signature(
        multi_long_function,
        FunctionInfo(
            "__init__",
            [FunctionArg("self")],
            "None",
            line=None,
            signature_end_line_index=None,
        ),
    )

    lines = result.splitlines()

    assert lines[0] == "class Person:"
    assert lines[1] == "  def __init__(self) -> None:"


def test_replaces_multi_line_signature():
    result = replace_function_signature(
        multi_line_signature,
        FunctionInfo(
            "__init__",
            [FunctionArg("self", "Any")],
            "None",
            line=None,
            signature_end_line_index=None,
        ),
    )

    lines = result.splitlines()

    assert lines[1] == "class Person:"
    assert lines[2] == "    def __init__(self: Any) -> None:"
    assert (
        lines[3]
        == '        """This function is a constructor for a new person."""'
    )

    result = replace_function_signature(
        result,
        FunctionInfo(
            "get_age",
            [FunctionArg("self", "Any")],
            "int",
            line=None,
            signature_end_line_index=None,
        ),
    )

    lines = result.splitlines()

    assert lines[13] == "    def get_age(self: Any) -> int:"
    assert lines[14] == "        return self.age"
