import os 

def get_files_info(working_directory: str, directory: str = ".") -> str:
    info = [f"Result for looking up {'current' if directory == '.' else f"'{directory}'"} directory:"]

    try:
        full_working_directory_path = os.path.abspath(working_directory)
        target_directory            = os.path.normpath(os.path.join(full_working_directory_path, directory))
        is_valid_target_directory   = os.path.commonpath([full_working_directory_path, target_directory]) == full_working_directory_path

        if not is_valid_target_directory:
            info.append(f'  Error: Cannot list "{directory}" as it is outside the permitted working directory')
            return "\n".join(info)
    
        if not os.path.isdir(target_directory):
            info.append(f'Error: "{directory}" is not a directory')
            return "\n".join(info)
        
        for dir_name in os.listdir(target_directory):
            abs_dir_name = os.path.join(target_directory, dir_name)
            info.append(f"  - {dir_name}: file_size={os.path.getsize(abs_dir_name)} bytes, is_dir={os.path.isdir(abs_dir_name)}")
        return "\n".join(info)
    
    except Exception as e:
        info.append(f'  Error: "{e}"')
        return "\n".join(info)
    
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
