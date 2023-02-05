from python_code_parse.get_function_indentation_str import (
    get_function_indentation_str,
)


simple_funcion = """
def sum(a, b):
  return a + b
"""


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


def test_get_function_indentation_str_returns_zero_spaces():
    """Test get_function_indentation_str returns zero spaces."""
    assert get_function_indentation_str(simple_funcion, "sum") == ""


def test_get_function_indentation_str_returns_correct_spaces():
    """Test get_function_indentation_str returns zero spaces."""
    assert get_function_indentation_str(multi_line_signature, "__init__") == "    "
    assert get_function_indentation_str(multi_line_signature, "__str__") == "    "
    assert get_function_indentation_str(multi_line_signature, "__repr__") == "    "
    assert get_function_indentation_str(multi_line_signature, "get_age") == "    "
