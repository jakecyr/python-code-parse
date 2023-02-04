import os
from python_code_parse.get_all_function_info_from_code import get_function_info_from_code
import json


def main():
    file_path = os.path.join(os.path.dirname(__file__), "../test.py")

    with open(file_path, encoding="utf-8") as f:
        code = f.read()

    functions = get_function_info_from_code(code)
    json_version = json.dumps(functions, default=lambda o: o.__dict__, indent=4)

    print(json_version)


if __name__ == "__main__":
    main()
