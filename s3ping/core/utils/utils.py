import random
import string
from typing import List, Optional

def random_string(length: int = 8, chars: Optional[str] = None) -> str:
    """
    Generate a random string of given length.
    
    Args:
        length (int): Length of the string.
        chars (str, optional): Characters to choose from. Defaults to letters + digits.
        
    Returns:
        str: Random string.
    """
    if chars is None:
        chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def chunk_list(data: List, chunk_size: int) -> List[List]:
    """
    Split a list into chunks of a given size.
    
    Args:
        data (List): The list to chunk.
        chunk_size (int): The size of each chunk.
        
    Returns:
        List[List]: List of chunks.
    """
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def safe_get(d: dict, key: str, default=None):
    """
    Safely get a value from a dictionary.
    
    Args:
        d (dict): Dictionary to access.
        key (str): Key to look for.
        default: Default value if key is not present.
    
    Returns:
        Value from dict or default.
    """
    return d.get(key, default)