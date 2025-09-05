import os
from config import MAX_CHARACTERS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specific file constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get the content from, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        #print(full_path)
        file_abs_path = os.path.abspath(full_path)
        #print(file_abs_path)
        working_dir_abs = os.path.abspath(working_directory)
        #print(working_dir_abs)
        if not os.path.isfile(file_abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        if not file_abs_path.startswith(working_dir_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        MAX_CHARS = MAX_CHARACTERS if isinstance(MAX_CHARACTERS, int) and MAX_CHARACTERS > 0 else 10000

        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
            
            if len(file_content_string) > MAX_CHARS:
                file_content_string = f"{file_content_string[:MAX_CHARS]} [...File \"{file_path}\" truncated at {MAX_CHARS} characters]"
 
            return file_content_string
        
    except Exception as e:
        return f"Error: {str(e)}"