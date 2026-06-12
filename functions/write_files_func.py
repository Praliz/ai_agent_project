import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.abspath(os.path.join(working_directory_abs, file_path))
        valid_target_file = os.path.commonpath([target_file, working_directory_abs]) == working_directory_abs
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        get_parent_dir = os.path.dirname(target_file)
        os.makedirs(get_parent_dir, exist_ok=True)
        with open(target_file,"w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as Error_messege:
        return f"Error: {Error_messege}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes content to file_path",
    parameters=types.Schema(
        required=["file_path","content"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="writes content to file_path and tells how many characters are written",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the actual content which is written to file_path"
            ),
        },
    ),
)