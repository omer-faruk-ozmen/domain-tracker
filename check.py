#!/usr/bin/env python3
"""
Environment Check Script for Domain Tracker

Checks if all dependencies and configurations are properly set up.
"""

import sys
import os

def check_python_version():
    """Check Python version."""
    print(f"✓ Python version: {sys.version}")
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    return True

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['asyncwhois', 'aiohttp']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing.append(package)
    
    if missing:
        print(f"\nInstall missing packages with:")
        print(f"pip install {' '.join(missing)}")
        return False
    return True

def check_config():
    """Check configuration file."""
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        import config
        print("✓ Config file found")
        
        # Check critical settings
        if hasattr(config, 'TELEGRAM_BOT_TOKEN') and config.TELEGRAM_BOT_TOKEN:
            if config.TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
                print("❌ TELEGRAM_BOT_TOKEN not configured")
                return False
            else:
                print("✓ TELEGRAM_BOT_TOKEN configured")
        else:
            print("❌ TELEGRAM_BOT_TOKEN missing")
            return False
            
        return True
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False

def check_files():
    """Check if all required files exist."""
    required_files = [
        'main.py', 'config.py', 'utils.py', 
        'domain_monitor.py', 'telegram_bot.py', 'state_manager.py'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"❌ {file} missing")
            missing.append(file)
    
    return len(missing) == 0

def main():
    """Run all checks."""
    print("🔍 Domain Tracker - Environment Check")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Configuration", check_config),
        ("Required Files", check_files)
    ]
    
    all_passed = True
    
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All checks passed! You can run 'python main.py'")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())