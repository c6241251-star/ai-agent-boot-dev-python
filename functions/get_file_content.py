import os

from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    info = [f"Result for reading '{file_path}' file:"]

    try:
        full_working_directory_path = os.path.abspath(working_directory)
        target_directory            = os.path.normpath(os.path.join(full_working_directory_path, file_path))
        is_valid_target_directory   = os.path.commonpath([full_working_directory_path, target_directory]) == full_working_directory_path

        if not is_valid_target_directory:
            info.append(f'  Error: Cannot read "{file_path}" as it is outside the permitted working directory')
            return "\n".join(info)
    
        if os.path.isdir(target_directory):
            info.append(f'  Error: File not found or is not a regular file: "{file_path}"')
            return "\n".join(info)
        
        with open(target_directory, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        info.append(file_content_string)
        return "\n".join(info)
    
    except Exception as e:
        info.append(f'  Error: "{e}"')
        return "\n".join(info)
    

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Retrieves the content (at most {MAX_CHARS} characters) of a specified file within the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}


    