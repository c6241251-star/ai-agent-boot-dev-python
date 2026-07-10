import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    info = [f"Result for running '{file_path}{f' "{" ".join(args)}"' if args is not None else ''}' file:"]

    try:
        full_working_directory_path = os.path.abspath(working_directory)
        target_directory            = os.path.normpath(os.path.join(full_working_directory_path, file_path))
        is_valid_target_directory   = os.path.commonpath([full_working_directory_path, target_directory]) == full_working_directory_path

        if not is_valid_target_directory:
            info.append(f'  Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
            return "\n".join(info)

        if not os.path.exists(target_directory) or not os.path.isfile(target_directory):
            info.append(f'  Error: "{file_path}" does not exist or is not a regular file')
            return "\n".join(info)
        
        if not target_directory.endswith(".py"):
            info.append(f'  Error: "{file_path}" is not a Python file')
            return "\n".join(info)

        command = ["python", target_directory]
        if args is not None:
            command.extend(args)

        completed_process = subprocess.run(
            command, 
            text=True, 
            timeout=30,
            cwd=full_working_directory_path,
            capture_output=True,
        )
        
        if completed_process.returncode != 0:
            info.append(f"  Process exited with code {completed_process.returncode}")
        if completed_process.stdout == "" and completed_process.stderr == "":
            info.append(f"  No output produced")
        if completed_process.stdout != "":
            info.append(f"  STDOUT:")
            info.append("\n".join([f"    {val}" for val in completed_process.stdout.split("\n")]))
        if completed_process.stderr != "":
            info.append(f"  STDERR:")
            info.append("\n".join([f"    {val}" for val in completed_process.stderr.split("\n")]))
        return "\n".join(info)
    
    except Exception as e:
        info.append(f"  Error: executing Python file: {e}")
        return "\n".join(info)
    

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}

