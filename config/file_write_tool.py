import logging
import os
from pathlib import Path
from typing import Optional, Union
from ..config.settings import resolve_path

logger = logging.getLogger(__name__)

def write_file(file_path: str, content: Union[str, bytes]) -> bool:
    """
    Write content to a file.
    
    Args:
        file_path (str): Path to the file to write (relative to project root)
        content (Union[str, bytes]): Content to write to the file
        
    Returns:
        bool: True if successful, False if error
    """
    try:
        # Resolve path to absolute path
        abs_path = resolve_path(file_path)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        
        # Determine write mode based on content type
        mode = 'wb' if isinstance(content, bytes) else 'w'
        encoding = None if isinstance(content, bytes) else 'utf-8'
        
        with open(abs_path, mode, encoding=encoding) as f:
            f.write(content)
            
        logger.info(f"Successfully wrote to file: {abs_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error writing to file {abs_path}: {str(e)}")
        return False 