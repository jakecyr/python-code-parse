# Python Code Parser

Parse Python code to extract information about functions, classes, methods, etc.

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
