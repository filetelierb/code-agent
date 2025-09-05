import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specific file constrained to the working directory, creating directories as needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write the content, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        #print(full_path)
        file_abs_path = os.path.abspath(full_path)
        #print(file_abs_path)
        working_dir_abs = os.path.abspath(working_directory)
        #print(working_dir_abs)
        
        if not file_abs_path.startswith(working_dir_abs):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        file_path_dir = os.path.dirname(full_path)
        if not os.path.exists(file_path_dir):
            os.makedirs(file_path_dir, exist_ok=False)
        
        with open(full_path, "w") as f:
            f.write(content)
    

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        MAX_CHARS = MAX_CHARACTERS if isinstance(MAX_CHARACTERS, int) and MAX_CHARACTERS > 0 else 10000

        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
            
            if len(file_content_string) > MAX_CHARS:
                file_content_string = f"{file_content_string[:MAX_CHARS]} [...File \"{file_path}\" truncated at {MAX_CHARS} characters]"
 
            return file_content_string
        
    except Exception as e:
        return f"Error: {str(e)}"