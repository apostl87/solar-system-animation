import os
import sys
from dotenv import load_dotenv

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

    except Exception:
        # In development, use the .env file
        load_dotenv()
        base_path = os.getenv('BASE_PATH')
        
    # Join the base path with the relative path to get the absolute path to the resource
    return os.path.join(base_path, 'resources', *relative_path_parts)
    


    
