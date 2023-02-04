from python_code_parse import (
    get_function_info_by_name,
    FunctionInfo,
    FunctionNotFoundException,
)
import pytest


def test_get_function_info_by_name_returns_function_info():
    assert isinstance(
        get_function_info_by_name("def test(): pass", "test"), FunctionInfo
    )


def test_get_function_info_by_name_raises_function_not_found_exception():
    with pytest.raises(FunctionNotFoundException):
        get_function_info_by_name("def test(): pass", "test2")


def test_get_function_info_by_name_returns_expected_info_with_one_function():
    multi_long_function = """def test(a: int, b: float) -> float:\n\tpass"""
    result = get_function_info_by_name(multi_long_function, "test")
    assert isinstance(
        result,
        FunctionInfo,
    )

    assert result.name == "test"
    assert result.line == 1
    assert result.return_type == "float"
    assert len(result.args) == 2
    assert result.args[0].name == "a"
    assert result.args[0].annotation == "int"
    assert result.args[1].name == "b"
    assert result.args[1].annotation == "float"


def test_get_function_info_by_name_returns_expected_info_with_two_functions():
    multi_long_function = """def test(a: int, b: float) -> float:\n\tpass"""
    multi_long_function += """\n\ndef test2(a: int, b: float) -> float:\n\tpass"""

    result = get_function_info_by_name(multi_long_function, "test")
    assert isinstance(
        result,
        FunctionInfo,
    )

    assert result.name == "test"
    assert result.line == 1
    assert result.return_type == "float"
    assert len(result.args) == 2
    assert result.args[0].name == "a"
    assert result.args[0].annotation == "int"
    assert result.args[1].name == "b"
    assert result.args[1].annotation == "float"
