import os
def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        #print(full_path)
        dir_abs_path = os.path.abspath(full_path)
        #print(dir_abs_path)
        working_dir_abs = os.path.abspath(working_directory)
        #print(working_dir_abs)
        if not os.path.isdir(dir_abs_path):
            return f'Error: "{directory}" is not a directory'
        if not dir_abs_path.startswith(working_dir_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        
        dir_items = os.listdir(full_path)
        str_items = "\n".join(list(map(lambda x: f"- {x}: file_size={os.path.getsize(os.path.join(full_path, x))} bytes, is_dir={"True" if os.path.isdir(os.path.join(full_path, x)) else "False"}", dir_items)))
        return str_items


    
    
    except Exception as e:
        return f"Error: {str(e)}"