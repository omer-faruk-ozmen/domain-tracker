#!/usr/bin/env python3
"""
Import Helper for Domain Tracker

Handles proper import path setup for different environments.
"""

import sys
import os
import importlib.util

def setup_import_path():
    """Setup proper import paths for all environments."""
    # Get current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add current directory to path if not already there
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Also try parent directory
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

def safe_import(module_name, from_list=None):
    """
    Safely import a module with proper error handling.
    
    Args:
        module_name: Name of the module to import
        from_list: List of items to import from module (for 'from' imports)
    
    Returns:
        The imported module or items
    """
    setup_import_path()
    
    try:
        if from_list:
            module = __import__(module_name, fromlist=from_list)
            if len(from_list) == 1:
                return getattr(module, from_list[0])
            else:
                return [getattr(module, item) for item in from_list]
        else:
            return __import__(module_name)
    except ImportError as e:
        print(f"❌ Failed to import {module_name}: {e}")
        print(f"📁 Current directory: {os.getcwd()}")
        print(f"📁 Script directory: {os.path.dirname(os.path.abspath(__file__))}")
        print(f"📁 Python path (first 3): {sys.path[:3]}")
        
        # List available Python files
        python_files = [f for f in os.listdir('.') if f.endswith('.py')]
        print(f"📄 Available Python files: {python_files}")
        
        raise ImportError(f"Cannot import {module_name}. Check if the file exists and is accessible.")

def check_module_exists(module_name):
    """Check if a module exists and can be imported."""
    setup_import_path()
    
    spec = importlib.util.find_spec(module_name)
    return spec is not None