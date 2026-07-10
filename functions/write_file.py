import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    info = [f"Result for writing to '{file_path}' file:"]

    try:
        full_working_directory_path = os.path.abspath(working_directory)
        target_directory            = os.path.normpath(os.path.join(full_working_directory_path, file_path))
        is_valid_target_directory   = os.path.commonpath([full_working_directory_path, target_directory]) == full_working_directory_path

        if not is_valid_target_directory:
            info.append(f'  Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
            return "\n".join(info)

        if os.path.isdir(target_directory):
            info.append(f'  Error: Cannot write to "{file_path}" as it is a directory')
            return "\n".join(info)
        
        os.makedirs(os.path.dirname(target_directory), exist_ok=True)
        
        with open(target_directory, "w") as f:
            f.write(content)

        info.append(f'  Successfully wrote to "{file_path}" ({len(content)} characters written)')
        return "\n".join(info)
    
    except Exception as e:
        info.append(f'  Error: "{e}"')
        return "\n".join(info)
    
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text content to a specified file within the working directory (overwriting if the file exists)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
