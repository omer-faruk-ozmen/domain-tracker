#!/usr/bin/env python3
"""
Domain Tracker Startup Script

This script ensures proper Python path setup for all environments
including Google VM, PythonAnywhere, and local development.
"""

import sys
import os

def setup_python_path():
    """Setup Python path for proper imports."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add to Python path if not already there
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    
    # Also add parent directory for relative imports
    parent_dir = os.path.dirname(script_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

def main():
    """Main entry point with proper path setup."""
    # Setup paths first
    setup_python_path()
    
    try:
        # Import and run the main application
        from main import main as run_main
        run_main()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Current working directory:", os.getcwd())
        print("Script directory:", os.path.dirname(os.path.abspath(__file__)))
        print("Python path:", sys.path[:3])  # Show first 3 entries
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()