# Python Code Parser

Parse Python code to extract information about functions, classes, methods, etc.

## Upload to PyPi

First you have to build the wheel file:

```bash
python setup.py bdist_wheel
```

Then the wheel file can be uploaded to PyPi with:

```bash
twine upload --skip-existing dist/*
```
