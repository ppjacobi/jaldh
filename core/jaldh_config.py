"""------------------------------
Module: ./core\jaldh_config.py
Description: Reads or if not existent generates a config file and returns its contents.
Notes: <Special remarks or dependencies>
Author: Peter Jacobi
Created: 2025-06-22
------------------------------"""

import yaml
import os
from datetime import datetime

DEFAULT_CONFIG = {
    'language': 'auto',
    'file_separator': '------------------------------',
    'function_separator': '------------------------------',
    'header': {
        'author': 'Anonymous',
        'include_date': True,
        'date_format': '%Y-%m-%d'
    }
}

def ensure_default_config(path='config.yaml'):
    """------------------------------
    Description: <Describe what ensure_default_config does>

    Parameters:
        path: <description>

    Returns:
        <description>
    ------------------------------"""
    if not os.path.exists(path):
        with open(path, 'w') as f:
            yaml.dump(DEFAULT_CONFIG, f)
    return load_config(path)

def load_config(path):
    """------------------------------
    Description: <Describe what load_config does>

    Parameters:
        path: <description>

    Returns:
        <description>
    ------------------------------"""
    with open(path, 'r') as f:
        return yaml.safe_load(f)