from python_code_parse import get_all_function_info_from_code
from python_code_parse.enums.special_arg import SpecialArg
from python_code_parse.models.function_info import FunctionInfo


def test_returns_array():
    assert isinstance(get_all_function_info_from_code(""), list)
    assert isinstance(
        get_all_function_info_from_code("def test(): pass"), list
    )
    assert isinstance(
        get_all_function_info_from_code(
            "def test(a: int, b: float) -> float: pass"
        ),
        list,
    )

    multi_long_function = """\ndef test(a: int, b: float) -> float:\n\tpass"""

    assert isinstance(
        get_all_function_info_from_code(multi_long_function),
        list,
    )


def test_returns_expected_info_with_one_function():
    multi_long_function = """def test(a: int, b: float) -> float:\n\tpass"""
    result = get_all_function_info_from_code(multi_long_function)
    assert isinstance(
        result,
        list,
    )

    assert len(result) == 1
    assert result[0].name == "test"
    assert result[0].line == 1
    assert result[0].return_type == "float"
    assert len(result[0].args) == 2
    assert result[0].args[0].name == "a"
    assert result[0].args[0].annotation == "int"
    assert result[0].args[1].name == "b"
    assert result[0].args[1].annotation == "float"


def test_returns_expected_info_with_two_functions():
    multi_long_function = """def test(a: int, b: float) -> float:\n\tpass"""
    multi_long_function += (
        """\n\ndef test2(a: int, b: float) -> float:\n\tpass"""
    )

    result = get_all_function_info_from_code(multi_long_function)
    assert isinstance(
        result,
        list,
    )

    assert len(result) == 2

    assert result[0].name == "test"
    assert result[0].line == 1
    assert result[0].return_type == "float"
    assert len(result[0].args) == 2
    assert result[0].args[0].name == "a"
    assert result[0].args[0].annotation == "int"
    assert result[0].args[1].name == "b"
    assert result[0].args[1].annotation == "float"

    assert result[1].name == "test2"
    assert result[1].line == 4
    assert result[1].return_type == "float"
    assert len(result[1].args) == 2
    assert result[1].args[0].name == "a"
    assert result[1].args[0].annotation == "int"
    assert result[1].args[1].name == "b"
    assert result[1].args[1].annotation == "float"


def test_returns_expected_info_with_default_value():
    multi_long_function = (
        """def test(a: int = 1, b: float = '1') -> float:\n\tpass"""
    )
    multi_long_function += """\n\ndef sum(a = 1, b = 2):\n\treturn a + b"""
    result: list[FunctionInfo] = get_all_function_info_from_code(
        multi_long_function
    )

    assert len(result) == 2
    assert result[0].args[0].default == "1"
    assert result[0].args[1].default == "'1'"
    assert result[1].args[0].default == "1"
    assert result[1].args[1].default == "2"


def test_returns_expected_info_with_default_value_after_first_argument():
    multi_long_function = (
        """def test(a, b: float = 1, c = 3) -> float:\n\tpass"""
    )
    result: list[FunctionInfo] = get_all_function_info_from_code(
        multi_long_function
    )

    assert len(result) == 1
    assert result[0].args[0].name == "a"
    assert result[0].args[0].default is None
    assert result[0].args[1].name == "b"
    assert result[0].args[1].default == "1"
    assert result[0].args[2].name == "c"
    assert result[0].args[2].default == "3"


class_string = """
class Person:
    def __init__(self, name):
        self.name = name

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
"""


def test_returns_expected_info_with_two_same_named_functions():
    result: list[FunctionInfo] = get_all_function_info_from_code(class_string)

    assert len(result) == 2

    assert len(result[0].args) == 2
    assert result[0].instance == 0
    assert result[0].args[0].name == "self"
    assert result[0].args[1].name == "name"

    assert len(result[1].args) == 3
    assert result[1].instance == 1
    assert result[1].args[0].name == "self"
    assert result[1].args[1].name == "name"
    assert result[1].args[2].name == "breed"


function_with_args_and_kwargs = """
def log(message: str, *args, **kwargs):
    print(f"LOG: {message}")
"""


def test_get_all_function_info_includes_args_and_kwargs():
    function_infos = get_all_function_info_from_code(
        function_with_args_and_kwargs
    )

    assert len(function_infos) == 1
    assert len(function_infos[0].args) == 3
    assert function_infos[0].args[0].name == "message"
    assert function_infos[0].args[0].annotation == "str"
    assert function_infos[0].args[1].name == "args"
    assert function_infos[0].args[1].special == SpecialArg.vararg
    assert function_infos[0].args[2].name == "kwargs"
    assert function_infos[0].args[2].special == SpecialArg.kwarg


function_with_required_kwargs = """
def log(*, message:str):
    print(f"LOG: {message}")
    return "hello"
"""


def test_get_all_function_info_includes_forced_kwargs():
    function_infos = get_all_function_info_from_code(
        function_with_required_kwargs
    )

    assert len(function_infos) == 1
    assert len(function_infos[0].args) == 1
    assert function_infos[0].args[0].name == "message"
    assert function_infos[0].args[0].annotation == "str"
