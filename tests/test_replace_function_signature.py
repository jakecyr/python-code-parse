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
        FunctionInfo("test2", [], "float", line=4, signature_end_line_index=4),
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
            line=4,
            signature_end_line_index=None,
        ),
    )

    result = replace_function_signature(
        result,
        FunctionInfo(
            "test3",
            [FunctionArg("a", "Any", 1), FunctionArg("b", "Any", 2)],
            "float",
            line=7,
            signature_end_line_index=None,
        ),
    )

    lines = result.splitlines()

    assert lines[0] == "def test(a: int = 1, b: float = 2) -> float:"
    assert lines[1] == "\tpass"
    assert lines[2] == ""
    assert lines[3] == "def test2(a = 1) -> float:"
    assert lines[4] == "\tpass"
    assert lines[6] == "def test3(a: Any = 1, b: Any = 2) -> float:"
    assert lines[7] == "\tpass"


def test_replaces_with_default_args_after_first_argument():
    multi_long_function = """def test(a, b: float = 2) -> float:\n\tpass"""

    result = replace_function_signature(
        multi_long_function,
        FunctionInfo(
            "test",
            [FunctionArg("a", None, None), FunctionArg("b", "float", 2)],
            "float",
            line=1,
            signature_end_line_index=1,
        ),
    )
    lines = result.splitlines()

    assert lines[0] == "def test(a, b: float = 2) -> float:"
    assert lines[1] == "\tpass"


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
            line=2,
            signature_end_line_index=2,
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
            line=3,
            signature_end_line_index=8,
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
            line=14,
            signature_end_line_index=14,
        ),
    )

    lines = result.splitlines()

    assert lines[13] == "    def get_age(self: Any) -> int:"
    assert lines[14] == "        return self.age"


class_string = """
class Person:
    def __init__(self, name):
        self.name = name

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

class Cat:
    def __init__(self, name, breed, favorite_toy):
        self.name = name
        self.breed = breed
        self.favorite_toy = favorite_toy
"""


def test_replace_signatures_with_two_same_named_functions_first_function():
    result: list[FunctionInfo] = replace_function_signature(
        class_string,
        FunctionInfo(
            "__init__",
            [FunctionArg("self"), FunctionArg("name")],
            "None",
            3,
            3,
        ),
    )

    lines = result.splitlines()

    assert lines[1] == "class Person:"
    assert lines[2] == "    def __init__(self, name) -> None:"
    assert lines[3] == "        self.name = name"
    assert lines[4] == ""
    assert lines[5] == "class Dog:"
    assert lines[6] == "    def __init__(self, name, breed):"
    assert lines[7] == "        self.name = name"
    assert lines[8] == "        self.breed = breed"
    assert lines[9] == ""
    assert lines[10] == "class Cat:"
    assert lines[11] == "    def __init__(self, name, breed, favorite_toy):"
    assert lines[12] == "        self.name = name"
    assert lines[13] == "        self.breed = breed"
    assert lines[14] == "        self.favorite_toy = favorite_toy"


def test_replace_signatures_with_two_same_named_functions_second_function():
    result: list[FunctionInfo] = replace_function_signature(
        class_string,
        FunctionInfo(
            "__init__",
            [FunctionArg("self"), FunctionArg("name"), FunctionArg("breed")],
            "None",
            7,
            7,
            instance=1,
        ),
    )

    lines = result.splitlines()

    assert lines[1] == "class Person:"
    assert lines[2] == "    def __init__(self, name):"
    assert lines[3] == "        self.name = name"
    assert lines[4] == ""
    assert lines[5] == "class Dog:"
    assert lines[6] == "    def __init__(self, name, breed) -> None:"
    assert lines[7] == "        self.name = name"
    assert lines[8] == "        self.breed = breed"
    assert lines[9] == ""
    assert lines[10] == "class Cat:"
    assert lines[11] == "    def __init__(self, name, breed, favorite_toy):"
    assert lines[12] == "        self.name = name"
    assert lines[13] == "        self.breed = breed"
    assert lines[14] == "        self.favorite_toy = favorite_toy"


def test_replace_signatures_with_two_same_named_functions_third_function():
    result: list[FunctionInfo] = replace_function_signature(
        class_string,
        FunctionInfo(
            "__init__",
            [
                FunctionArg("self"),
                FunctionArg("name"),
                FunctionArg("breed"),
                FunctionArg("favorite_toy"),
            ],
            "None",
            None,
            None,
            instance=2,
        ),
    )

    lines = result.splitlines()

    assert lines[1] == "class Person:"
    assert lines[2] == "    def __init__(self, name):"
    assert lines[3] == "        self.name = name"
    assert lines[4] == ""
    assert lines[5] == "class Dog:"
    assert lines[6] == "    def __init__(self, name, breed):"
    assert lines[7] == "        self.name = name"
    assert lines[8] == "        self.breed = breed"
    assert lines[9] == ""
    assert lines[10] == "class Cat:"
    assert (
        lines[11]
        == "    def __init__(self, name, breed, favorite_toy) -> None:"
    )
    assert lines[12] == "        self.name = name"
    assert lines[13] == "        self.breed = breed"
    assert lines[14] == "        self.favorite_toy = favorite_toy"
