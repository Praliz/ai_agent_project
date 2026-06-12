import os
import subprocess
from google.genai import types
def run_python_file(
        working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs ,file_path ))
        valid_target_dir = os.path.commonpath([target_file,working_directory_abs]) == working_directory_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python",target_file]
        if args:
            command.extend(args)
        result = subprocess.run(command, cwd=working_directory_abs, capture_output=True, text=True, timeout=30)
        output = []
        if result.returncode !=0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append(f"No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return  "\n".join(output)
    except Exception as e:
        return f"Error: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs python on specified file",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="runs python on file and only the specified file and it takes into consideration if there are arguments to be handled.",
            ),
             "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="arguments are optional but we want to present them if they appear."
                
            ),
            
        }
    ),
)