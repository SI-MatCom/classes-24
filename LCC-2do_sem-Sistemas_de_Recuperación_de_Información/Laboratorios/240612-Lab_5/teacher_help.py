
import os
from os import path

def get_text(path_folder, text_processing_function):
    """Process multiple documents contained in the same folder

    Args:
        path_folder (str): Folder containing texts in TXT files.
        text_processing_function (function): function to process texts. It is expected to receive the text as a string and return a list of tokens.

    Returns:
        [list]: Set of all concatenated tokens, with the same original order.
        
    """
    result = []
    
    for file in os.listdir(path_folder):
        file_path = os.path.join(path_folder, file)
        
        with open(file_path, 'r', encoding='utf8', errors='ignore') as nf:
            lines = nf.readlines()
            
        result += text_processing_function(' '.join(lines))
        
    return result
    