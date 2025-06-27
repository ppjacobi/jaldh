"""
------------------------------
Module: ./core/jaldh_fileparser.py
Description: Recognizes the file type, opens and parses them and returns their contents.
Notes: Depends on the core.jaldh_codeparser module.
Author: Peter Jacobi
Created: 2025-06-22
------------------------------
"""

import re
import os
from typing import Optional
from core.jaldh_codeparser import parse_python_functions, parse_c_functions, parse_cpp_classes
from core.jaldh_logger import logIt

# Centralized list for supported file extensions
SUPPORTED_LANGUAGES = {
    'python': ['.py'],
    'c': ['.c', '.h'],
    'cpp': ['.cpp', '.hpp', '.cc']
}

class FileParser:
    def __init__(self, config: dict):
        self.config = config

    def parse_file_and_insert_headers(filepath: str, lang: str, config: dict, dry_run: bool = False) -> Optional[str]:
        """
        Parses the file based on its language and inserts documentation headers.

        Parameters:
            filepath (str): The path to the input file to process.
            lang (str): The language of the source file. If set to 'auto', language will be detected based on extension.
            config (dict): Configuration settings for the parser.
            dry_run (bool): If True, no changes will be written to the file.

        Returns:
            Optional[str]: The modified file content with inserted headers, or None if the language is unsupported.
        """
        # Get the file extension
        ext = os.path.splitext(filepath)[1]

        # Language auto-detection based on file extension
        if lang == 'auto':
            for detected_lang, extensions in SUPPORTED_LANGUAGES.items():
                if ext in extensions:
                    lang = detected_lang
                    break
            else:
                print(f"[ERROR] Unsupported file extension for auto-detection: {ext}")
                logIt(f"Unsupported file extension for auto-detection: {ext}")
                return None

        # Open and read the file's content
        try:
            with open(filepath, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"[ERROR] File not found: {filepath}")
            logIt(f"File not found: {filepath}")
            return None
        except PermissionError:
            print(f"[ERROR] Permission denied: {filepath}")
            logIt(f"Permission denied: {filepath}")
            return None
        except Exception as e:
            print(f"[ERROR] Failed to read file {filepath}: {e}")
            logIt(f"Failed to read file {filepath}: {e}")
            return None

        # Process the file based on its language
        try:
            if lang == 'python':
                return parse_python_functions(content, config, filepath)
            elif lang == 'c':
                return parse_c_functions(content, config, filepath)
            elif lang == 'cpp':
                content = parse_c_functions(content, config, filepath)
                if ext in ['.h', '.hpp']:
                    content = parse_cpp_classes(content, config)
                return content
            else:
                print(f"[ERROR] Unsupported language specified: {lang}")
                logIt(f"Unsupported language specified: {lang}")
                return None
        except Exception as e:
            print(f"[ERROR] Failed to parse file {filepath} for language {lang}: {e}")
            logIt(f"Failed to parse file {filepath} for language {lang}: {e}")
            return None

