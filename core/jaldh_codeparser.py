"""------------------------------
Module: ./core\jaldh_codeparser.py
Description: <Short module description>
Notes: Functions that parses the code and adds documentation headers.
Author: Peter Jacobi
Created: 2025-06-22
------------------------------"""

import re
import os
from datetime import datetime

def parse_python_functions(content, config, filename):
    """
    Parses Python file content to add missing documentation headers.

    Parameters:
        content (str): The content of the Python file.
        config (dict): Configuration dictionary for header generation.
        filename (str): The name of the file being processed.

    Returns:
        str: The Python content with added documentation headers.
    """

    def generate_module_header(config, filename):
        """Generates the module-level header."""
        separator = config.get('file_separator', '------------------------------')
        author = config.get('header', {}).get('author', 'Unknown')
        include_date = config.get('header', {}).get('include_date', True)
        date_format = config.get('header', {}).get('date_format', '%Y-%m-%d')
        date_str = datetime.now().strftime(date_format) if include_date else ''

        header_lines = [
            f'"""{separator}',
            f'Module: {filename}',
            'Description: <Short module description>',
            'Notes: <Special remarks or dependencies>',
            f'Author: {author}',
        ]
        if include_date:
            header_lines.append(f'Created: {date_str}')
        header_lines.append(f'{separator}"""\n')

        return header_lines

    def generate_function_docstring(func_name, params, config):
        """Generates a docstring for a function."""
        separator = config.get('function_separator', '------------------------------')
        docstring_lines = [
            f'    """{separator}',
            f'    Description: <Describe what {func_name} does>',
            '',
        ]
        if params:
            docstring_lines.append('    Parameters:')
            for param in params:
                docstring_lines.append(f'        {param}: <description>')
        docstring_lines.extend([
            '',
            '    Returns:',
            '        <description>',
            f'    {separator}"""'
        ])

        return docstring_lines

    # Split the content into lines for processing
    lines = content.splitlines()

    # Add a module-level header if missing
    if not lines or not lines[0].strip().startswith('"""'):
        lines = generate_module_header(config, filename) + lines

    # Find all function definitions and add docstrings if missing
    pattern = re.compile(r'^def\s+(\w+)\s*\((.*?)\):')
    processed_lines = []
    for i, line in enumerate(lines):
        match = pattern.match(line)
        if match:
            func_name = match.group(1)
            params = [param.strip().split('=')[0].strip() for param in match.group(2).split(',') if param.strip()]

            # Check if next line is a docstring
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
            if not next_line.startswith('"""'):
                docstring_lines = generate_function_docstring(func_name, params, config)
                processed_lines.append(line)
                processed_lines.extend(docstring_lines)
                continue

        # Append current line if no processing is needed
        processed_lines.append(line)

    # Join processed lines into a single content string
    return '\n'.join(processed_lines)


def parse_c_functions(content, config, filename):
    """
    Parses C file content to add missing documentation comments.

    Parameters:
        content (str): The content of the C file.
        config (dict): Configuration dictionary for header generation.
        filename (str): The name of the file being processed.

    Returns:
        str: The C content with added documentation headers and function comments.
    """

    def generate_module_header(config, filename):
        """Generates the module-level header."""
        separator = config.get('file_separator', '------------------------------')
        author = config.get('header', {}).get('author', 'Unknown')
        include_date = config.get('header', {}).get('include_date', True)
        date_format = config.get('header', {}).get('date_format', '%Y-%m-%d')
        date_str = datetime.now().strftime(date_format) if include_date else ''

        header_lines = [
            f'/*{separator}',
            f'Module: {filename}',
            'Description: <Short module description>',
            'Notes: <Special remarks or dependencies>',
            f'Author: {author}',
        ]
        if include_date:
            header_lines.append(f'Created: {date_str}')
        header_lines.append(f'{separator}*/\n')

        return header_lines

    def generate_function_comment(return_type, func_name, params, config):
        """Generates a function-level comment."""
        separator = config.get('function_separator', '------------------------------')
        comment_lines = [
            f'/*{separator}',
            f'{func_name} - <Describe what this function does>',
            ''
        ]
        if params:
            comment_lines.append('Parameters:')
            for param in params:
                comment_lines.append(f'    {param} - <description>')
        comment_lines.extend([
            '',
            'Returns:',
            f'    {return_type} - <description>',
            f'{separator}*/'
        ])

        return comment_lines

    # Break the content into lines
    lines = content.splitlines()

    # Add a module-level header if missing
    if not lines or not lines[0].strip().startswith('/*'):
        lines = generate_module_header(config, filename) + lines

    # Regex pattern for function definitions
    pattern = re.compile(r'^\s*(\w[\w\s\*\[\]]+)\s+(\w+)\s*\(([^;]*)\)\s*\{')

    # Process lines to add function comments
    processed_lines = []
    for i, line in enumerate(lines):
        match = pattern.match(line)
        if match:
            return_type = match.group(1).strip()
            func_name = match.group(2).strip()
            param_list = match.group(3).strip()
            params = [p.strip().split()[-1] for p in param_list.split(',') if p.strip() and p.strip() != 'void']

            # Check if the previous line is already a comment
            prev_line = lines[i - 1].strip() if i > 0 else ''
            if not (prev_line.startswith("/*") or prev_line.startswith("//")):
                comment = generate_function_comment(return_type, func_name, params, config)
                processed_lines.extend(comment)

        # Append the current line to the output
        processed_lines.append(line)

    # Return the processed content
    return '\n'.join(processed_lines)



def parse_cpp_classes(content, config):
    """
    Parses C++ file content to add missing class documentation.

    Parameters:
        content (str): The content of the C++ file.
        config (dict): Configuration dictionary for comment generation.

    Returns:
        str: The C++ content with added class documentation.
    """

    def generate_class_comment(class_type, class_name, config):
        """Generates a class-level documentation comment."""
        separator = config.get('function_separator', '------------------------------')
        comment_lines = [
            f'/*{separator}',
            f'{class_name} - {class_type} overview',
            f'Constructor example: {class_name} obj;',
            f'{separator}*/'
        ]
        return comment_lines

    # Compile regex for class/struct declaration
    class_pattern = re.compile(r'\b(class|struct)\s+(\w+)\s*(?:[:\{])')

    lines = content.splitlines()
    processed_lines = []
    for line in lines:
        match = class_pattern.match(line)
        if match:
            class_type, class_name = match.groups()
            comment = generate_class_comment(class_type, class_name, config)
            processed_lines.extend(comment)
        processed_lines.append(line)

    # Return the processed content
    return '\n'.join(processed_lines)
