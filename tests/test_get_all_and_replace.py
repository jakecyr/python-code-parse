from python_code_parse import (
    FunctionArg,
    FunctionInfo,
    replace_function_signature,
    get_all_function_info_from_code,
)


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


def test_get_all_and_replace_second_init_method():
    function_infos: list[FunctionInfo] = get_all_function_info_from_code(
        class_string
    )

    cat_init = function_infos[2]

    new_function_info = FunctionInfo(
        name=cat_init.name,
        args=[
            FunctionArg("self"),
            FunctionArg("name", "str"),
            FunctionArg("breed", "BreedEnum"),
            FunctionArg("favorite_toy", "ToyEnum"),
        ],
        return_type="None",
        line=cat_init.line,
        signature_end_line_index=cat_init.signature_end_line_index,
        instance=cat_init.instance,
    )

    updated_code = replace_function_signature(class_string, new_function_info)
    lines = updated_code.splitlines()

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
        == "    def __init__(self, name: str, breed: BreedEnum, favorite_toy: ToyEnum) -> None:"
    )
    assert lines[12] == "        self.name = name"
    assert lines[13] == "        self.breed = breed"
    assert lines[14] == "        self.favorite_toy = favorite_toy"
