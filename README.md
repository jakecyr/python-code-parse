# Python Code Parser

Simple functions built on Python `ast` to parse Python code and extract information about functions, parameters, etc.

Used for auto-type-hinting projects.

## Install with pip

```bash
pip install python_code_parse
```

## Functions

### get_function_info_by_name

Returns a [`FunctionInfo`](./python_code_parse/models/function_info.py) object containing information about a function and [it's parameters](./python_code_parse/models/function_arg.py) in a given code string.

### get_all_function_info_from_code

Returns a list of [`FunctionInfo`](./python_code_parse/models/function_info.py) objects, each containing information about a function and [it's parameters](./python_code_parse/models/function_arg.py) in a given code string.

### replace_function_signature

Replace a function declaration including the parameters (with annotations and default values) and the return type.

### function_returns

Returns a boolean value saying if a given function returns a value or `None`.

## Example

Below is the output of running the parser on the example `examples/basic_example.py`:

```python
from python_code_parse import get_all_function_info_from_code, FunctionInfo
from typing import List

with open("examples/basic_example.py", "r") as f:
    data = f.read()

function_infos: List[FunctionInfo] = get_all_function_info_from_code(data)

print(function_infos)

"""
[
  FunctionInfo(
    name='sum',
    args=[
      FunctionArg(name='a', annotation='int'),
      FunctionArg(name='b', annotation='', default = '1')
    ],
    return_type='None',
    line=1
  ),
  FunctionInfo(
    name='subtract',
    args=[
      FunctionArg(name='a', annotation=''),
      FunctionArg(name='b', annotation='')
    ],
    return_type='int',
    line=5
  ),
  FunctionInfo(
    name='log',
    args=[
      FunctionArg(name='message', annotation='str', special=SpecialArg.kwonlyargs),
    ],
    return_type='None',
    line=9
  )
]
"""
```
