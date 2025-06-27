"""
------------------------------
Module: .\jaldh.py
Description: Main execution file for jaldh (Just Another Little Doc Helper)
    JALDH supports Python, C, C++, and auto-detection of language based on file extension.
Author: Peter Jacobi
Created: 2025-06-22
------------------------------
"""

import argparse
import os
import sys
from typing import Generator

from core.jaldh_config import load_config, ensure_default_config
from core.jaldh_fileparser import FileParser
from core.jaldh_docwriter import extract_headers_and_write_doc
from core.jaldh_logger import logIt

VERSION = "0.1.0 Beta"

# Define supported file extensions as a constant
SUPPORTED_EXTENSIONS = ('.py', '.c', '.h', '.cpp', '.hpp', '.cc')


def collect_files(base_path: str, recursive: bool) -> Generator[str, None, None]:
    """
    Collect files from a given directory based on supported extensions.

    Parameters:
        base_path (str): Base directory path.
        recursive (bool): Whether to search subdirectories recursively.

    Yields:
        str: Absolute path to a matching file.
    """
    for root, dirs, files in os.walk(base_path):
        for f in files:
            if f.endswith(SUPPORTED_EXTENSIONS):
                yield os.path.join(root, f)
        if not recursive:
            break


def main():
    """
    Main script execution function. Handles argument parsing and processing.
    """
    print(f"jaldh (Just-Another-Little-Doc-Helper) - Version {VERSION}")
    logIt(f"Starting jaldh {VERSION} with arguments: {sys.argv[1:]}...")

    parser = argparse.ArgumentParser(description='jaldh - Just Another Little Doc Helper')
    parser.add_argument('--source', '-s', help='Path to source file or directory')
    parser.add_argument('--lang', '-l', choices=['python', 'c', 'cpp', 'auto'], default='auto', help='Source language')
    parser.add_argument('--config', '-c', default='config.yaml', help='Path to config file')
    parser.add_argument('-a', action='store_true', help='Apply to all files in current directory')
    parser.add_argument('-r', action='store_true', help='Apply recursively to subdirectories')
    parser.add_argument('-o', metavar='PREFIX', help='Write output to new files with prefix')
    parser.add_argument('--doc', metavar='FILENAME', help='Write collected documentation to FILENAME ')

    args = parser.parse_args()

    # Validate input arguments
    if not args.a and not args.r and not args.source:
        parser.error("--source (-s) is required unless -a or -r is specified.")

    # Ensure default configuration exists or is loaded
    try:
        config = ensure_default_config(args.config)
    except FileNotFoundError:
        print(f"Configuration file not found: {args.config} and can not be created. ... System error! exiting.")
        logIt("Configuration file not found and cant be created. This is a fatal error.")
        sys.exit(1)

    # Collect target files
    targets = []
    try:
        if args.a or args.r:
            base_path = args.source or '.'
            targets = list(collect_files(base_path, recursive=args.r))
        elif os.path.isfile(args.source):
            targets = [args.source]
        else:
            print("Invalid source path or missing flags (-a / -r) for directory processing.")
            return
    except Exception as e:
        print(f"Error while collecting files: {e}")
        logIt(f"Error while collecting files: {e}")
        sys.exit(1)

    # Process documentation writing
    if args.doc:
        try:
            extract_headers_and_write_doc(targets, args.doc)
        except Exception as e:
            print(f"Error while writing documentation: {e}")
            logIt(f"Error while writing documentation: {e}")
        return

    # Process target files
    for filepath in targets:
        try:
            fparser = FileParser(config)
            new_content = fparser.parse_file_and_insert_headers(filepath, args.lang, config, dry_run=bool(args.o))
            if new_content is None:
                continue

            if args.o:
                dir_name = os.path.dirname(filepath)
                base_name = os.path.basename(filepath)
                output_path = os.path.join(dir_name, f"{args.o}{base_name}")
                with open(output_path, 'w') as f:
                    f.write(new_content)
            else:
                with open(filepath, 'w') as f:
                    f.write(new_content)
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")
            logIt(f"Error processing file {filepath}: {e}")


if __name__ == '__main__':
    main()
    