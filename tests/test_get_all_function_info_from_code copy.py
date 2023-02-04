from python_code_parse import get_all_function_info_from_code


def test_get_all_function_info_from_code_returns_array():
    assert isinstance(get_all_function_info_from_code(""), list)
    assert isinstance(get_all_function_info_from_code("def test(): pass"), list)
    assert isinstance(
        get_all_function_info_from_code("def test(a: int, b: float) -> float: pass"),
        list,
    )

    multi_long_function = """\ndef test(a: int, b: float) -> float:\n\tpass"""

    assert isinstance(
        get_all_function_info_from_code(multi_long_function),
        list,
    )


def test_get_all_function_info_from_code_returns_expected_info_with_one_function():
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


def test_get_all_function_info_from_code_returns_expected_info_with_two_functions():
    multi_long_function = """def test(a: int, b: float) -> float:\n\tpass"""
    multi_long_function += """\n\ndef test2(a: int, b: float) -> float:\n\tpass"""

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
