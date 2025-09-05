import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file constrained to the working directory and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to run the code, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of arguments to pass to the Python script.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        #print(full_path)
        file_abs_path = os.path.abspath(full_path)
        #print(file_abs_path)
        working_dir_abs = os.path.abspath(working_directory)
        #print(working_dir_abs)
        if not file_abs_path.startswith(working_dir_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(file_abs_path):
            return f'Error: File "{file_path}" not found.'
        elif not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        new_args = ["python3",file_abs_path] + args
        completed_process = subprocess.run(timeout=30,capture_output=True,args=new_args)
        if completed_process is None:
            return "No output produced."
        if completed_process.returncode != 0:
            return f'STDOUT: {completed_process.stdout.decode()}\nSTDERR: {completed_process.stderr.decode()}\nProcess exited with code {completed_process.returncode}'
        return f'STDOUT: {completed_process.stdout.decode()}\nSTDERR: {completed_process.stderr.decode()}'

        
        
        
        
    except Exception as e:
        return f"Error: executing Python file: {e}"