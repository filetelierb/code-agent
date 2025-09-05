from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    working_directory = "./calculator"
    function_name = function_call_part.name
    args = dict(function_call_part.args)
    args["working_directory"] = working_directory

    match function_name:
        case "get_files_info":
            function_result = get_files_info(**args)
        case "get_file_content":
            function_result = get_file_content(**args)
        case "write_file":
            function_result = write_file(**args)
        case "run_python_file":
            function_result = run_python_file(**args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )