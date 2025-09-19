#!/usr/bin/env python3
"""
Configuration Settings for Domain Tracker
"""

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "8440365885:AAHzFhnDqnmviK1G3y5SYWKTT9kWPP4f3SM"
TELEGRAM_AVAILABLE_CHAT_ID = "-1003070547606"  # Domain available notifications
TELEGRAM_UNAVAILABLE_CHAT_ID = "-1002696377311"  # Status reports and bot commands

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