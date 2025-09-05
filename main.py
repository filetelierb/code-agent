import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function


if len(sys.argv) > 1:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    
    Try making sense of the working directory structure first by listing files and reading files as needed. Then write or execute code as needed to fulfill the user's request.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )
    my_config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )
    
    verbose = "--verbose" in sys.argv
    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    client = genai.Client(api_key=api_key)
    try:
        for i in range(20):
            response = client.models.generate_content(model="gemini-2.5-flash",contents=messages, config=my_config)
            for candidate in response.candidates:
                messages.append(candidate.content)
            #print(response.text)
            if not response.function_calls is None and len(response.function_calls) >= 0:
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose=verbose)
                    messages.append(types.Content(role="user", parts=function_call_result.parts))

            elif response.text is not None:
                print(response.text)
                exit(0)
            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
else:
    print("Please provide an argument to run the script.")
    exit(1)