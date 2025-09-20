#!/usr/bin/env python3
"""
Configuration Settings for Domain Tracker
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_AVAILABLE_CHAT_ID = os.getenv("TELEGRAM_AVAILABLE_CHAT_ID", "YOUR_AVAILABLE_CHAT_ID_HERE")  # Domain available notifications
TELEGRAM_UNAVAILABLE_CHAT_ID = os.getenv("TELEGRAM_UNAVAILABLE_CHAT_ID", "YOUR_UNAVAILABLE_CHAT_ID_HERE")  # Status reports and bot commands

# Monitoring Configuration
CHECK_INTERVAL = 60  # seconds between domain checks
STATUS_REPORT_CYCLES = 120  # send status report every N cycles

# Timeouts
RDAP_TIMEOUT = 10  # seconds
WHOIS_TIMEOUT = 20  # seconds
TELEGRAM_TIMEOUT = 15  # seconds

# File Paths
STATE_FILE = "domain_state.json"
LOGS_DIR = "logs"

# Default domains to monitor (if state file doesn't exist)
DEFAULT_DOMAINS = [
    "memurx.com",
]

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"