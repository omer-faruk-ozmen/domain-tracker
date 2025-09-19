#!/usr/bin/env python3
"""
Utility Functions for Domain Tracker
"""

import logging
import os
import aiohttp
from datetime import datetime
from typing import Optional

from config import TELEGRAM_BOT_TOKEN, LOGS_DIR, LOG_LEVEL, LOG_FORMAT

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure logging with daily rotation."""
    # Ensure logs directory exists
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    # Create daily log filename
    today = datetime.now().strftime("%Y-%m-%d")
    log_filename = os.path.join(LOGS_DIR, f"domain_tracker_{today}.log")
    
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger.info(f"Logging configured - File: {log_filename}")


def format_datetime(iso_string: str, fallback: str = "Unknown") -> str:
    """Format ISO datetime string to readable format."""
    if not iso_string or iso_string == fallback:
        return fallback
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        return fallback


def format_datetime_short(iso_string: str, fallback: str = "Unknown") -> str:
    """Format ISO datetime string to short readable format."""
    if not iso_string or iso_string == fallback:
        return fallback
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return dt.strftime("%m-%d %H:%M")
    except (ValueError, TypeError):
        return fallback


def validate_domain(domain: str) -> bool:
    """Basic domain format validation."""
    if not domain or not isinstance(domain, str):
        return False
    
    domain = domain.strip().lower()
    
    # Basic checks
    if not domain or '.' not in domain:
        return False
    
    # Check for invalid characters
    if any(char in domain for char in [' ', '/', '\\', '?', '#']):
        return False
    
    return True


async def send_telegram_message(message: str, chat_id: str) -> bool:
    """
    Send a message to Telegram using the bot API.
    Returns True if successful, False otherwise.
    """
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, timeout=30) as response:
                if response.status == 200:
                    logger.debug(f"Telegram message sent to {chat_id}")
                    return True
                else:
                    logger.error(f"Failed to send Telegram message: {response.status}")
                    return False
                    
    except Exception as e:
        logger.error(f"Error sending Telegram message: {e}")
        return False


def get_status_emoji(status: str) -> str:
    """Get emoji for domain status."""
    if status == "available":
        return "✅"
    elif status == "unavailable":
        return "⏳"
    else:
        return "❓"