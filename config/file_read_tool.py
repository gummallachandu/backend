import logging
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

def read_file(file_path: str) -> str:
    """
    Read content from a text file.
    
    Args:
        file_path (str): Path to the file to read
        
    Returns:
        str: Content of the file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        Exception: For other file reading errors
    """
    try:
        logger.info(f"Reading file: {file_path}")
        with open(file_path, 'r') as f:
            content = f.read()
        logger.info(f"Successfully read file: {file_path}")
        return content
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        raise