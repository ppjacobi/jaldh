"""------------------------------
Module: ./core\jaldh_docwriter.py
Description: Extracts the documentation headers from files and writes them to a single file.
Notes: <Special remarks or dependencies>
Author: Peter Jacobi
Created: 2025-06-22
------------------------------"""

import re
import os
from jaldh_logger import logIt

def extract_headers_and_write_doc(filepaths, output_file):
    """
    Extracts documentation headers from a list of files and writes them to a single output file.

    Parameters:
        filepaths (list[str]): A list of file paths where headers will be extracted from.
        output_file (str): The path to the output file where extracted headers will be written.

    Returns:
        None
    """

    def extract_header(content):
        """
        Extracts the documentation header from the file content.

        Parameters:
            content (str): The content of the file.

        Returns:
            str: The extracted documentation header, or an empty string if no header is found.
        """
        # Regex for Python ("""...""") or C/C++ style comments (/*...*/)
        header_pattern = re.compile(r'(\"\"\"|/\*)[-=]{5,}(.*?)(\"\"\"|\*/)', re.DOTALL)
        match = header_pattern.search(content)
        return match.group(0).strip() if match else None

    documentation = []

    for filepath in filepaths:
        try:
            with open(filepath, 'r') as file:
                content = file.read()

            name = os.path.basename(filepath)
            documentation.append(f"File: {name}\n")
            documentation.append("=" * 60 + "\n")

            # Extract header
            header = extract_header(content)
            if header:
                documentation.append(header + "\n")
            else:
                documentation.append("No documentation header found.\n")

            documentation.append("=" * 60 + "\n")
        except (IOError, FileNotFoundError):
            documentation.append(f"File: {filepath} - ERROR: Could not read file.\n")
            documentation.append("=" * 60 + "\n")
            logIt(f"File: {filepath} - ERROR: Could not read file.\n")

    try:
        with open(output_file, 'w') as out:
            out.writelines(documentation)
    except IOError:
        print(f"ERROR: Could not write to output file: {output_file}")
        logIt(f"ERROR: Could not write to output file: {output_file}")