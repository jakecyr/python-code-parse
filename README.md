# Python Code Parser

Parse Python code to extract information about functions, classes, methods, etc.

## Install with pip

```bash
pip install python_code_parse
```

## Usage

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

## Setup for Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
pip install -e .[dev]
```

## Upload to PyPi

First you have to build the wheel file:

```bash
python3 -m pip wheel .
```

Then the wheel file can be uploaded to PyPi with:

```bash
twine upload --skip-existing python_code_parse-*.whl
```
