import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs_content = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_directory_abs_content, file_path))
        valid_file_path = os.path.commonpath([target_path,working_directory_abs_content]) == working_directory_abs_content
        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_path, "r") as file:  
            content = file.read(MAX_CHARS)      
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of file with a set maximum chars",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Reads file content",
            ),
        },
    ),
)