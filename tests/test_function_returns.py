from python_code_parse import function_returns


test_functions = """
def sum(a,b):
    return a + b

def log(message):
    print(message)

def subtract(a, b):
    return a - b
"""


def test_function_returns_returns_true_when_function_returns():
    returns = function_returns(test_functions, "sum", instance=0)
    assert returns is True
    returns = function_returns(test_functions, "subtract", instance=0)
    assert returns is True


def test_function_returns_returns_false_when_function_does_not_return():
    returns = function_returns(test_functions, "log", instance=0)
    assert returns is False
