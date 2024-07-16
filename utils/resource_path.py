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
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # In development, use the absolute path of the current file's directory
        base_path = os.path.abspath(".")
    
    # Join the base path with the relative path to get the absolute path to the resource
    return os.path.join(base_path, relative_path)
    


    
