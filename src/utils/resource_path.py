import os
import sys

def resource_path(relative_path):
    """
    Get absolute path to resource, works for both development and PyInstaller environments.

    Parameters:
    relative_path (str): The relative path to the resource file.

    Returns:
    str: The absolute path to the resource file.
    """
    relative_path_parts = os.path.normpath(relative_path).split(os.sep)
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        if ".." == relative_path_parts[0]:
            relative_path_parts.pop(0)
    except Exception:
        # In development, use the absolute path of the current file's directory
        base_path = os.path.abspath(".")
        if ".." == relative_path_parts[0]: # Workaround with the new structure
            relative_path_parts.pop(0)
    
    # Join the base path with the relative path to get the absolute path to the resource
    return os.path.join(base_path, *relative_path_parts)
    


    
