#!/usr/bin/env python3
"""
Domain Tracker - Main Entry Point

Production-ready domain backorder monitoring system with:
- Async domain availability checking using RDAP and WHOIS
- Instant Telegram notifications for available domains
- Telegram bot interface for domain management
- Persistent JSON-based state management
- Daily rotating logs with optimized output

Author: Domain Tracker Team
Version: 2.0.0
"""

import asyncio
import logging
import sys
import os

# Add multiple path options for maximum compatibility
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
sys.path.insert(0, os.getcwd())
sys.path.insert(0, '.')

# Now import local modules with enhanced error handling
try:
    from utils import setup_logging
    from domain_monitor import DomainMonitor
    from telegram_bot import TelegramBot
except ImportError as e:
    print(f"❌ Import error in main.py: {e}")
    print(f"📁 Current working directory: {os.getcwd()}")
    print(f"📁 Script directory: {script_dir}")
    print(f"📄 Files in current directory:")
    for f in sorted(os.listdir('.')):
        if f.endswith('.py'):
            print(f"   ✓ {f}")
    print(f"🐍 Python path (first 5): {sys.path[:5]}")
    print("\n💡 Troubleshooting:")
    print("   1. Make sure you're in the correct directory")
    print("   2. Check if config.py exists")
    print("   3. Try: python3 -c 'import config; print(\"Config OK\")'")
    sys.exit(1)

logger = logging.getLogger(__name__)


class DomainTracker:
    """Main application coordinator."""
    
    def __init__(self):
        self.domain_monitor = DomainMonitor()
        self.telegram_bot = TelegramBot()
    
    async def run_domain_monitor(self) -> None:
        """Run the domain monitoring service."""
        try:
            logger.info("🔍 Starting domain monitoring service...")
            await self.domain_monitor.run()
        except Exception as e:
            logger.error(f"Domain monitor error: {e}")
    
    async def run_telegram_bot(self) -> None:
        """Run the Telegram bot service."""
        try:
            logger.info("🤖 Starting Telegram bot service...")
            await self.telegram_bot.run()
        except Exception as e:
            logger.error(f"Telegram bot error: {e}")
            # Continue without Telegram bot if it fails
    
    async def run(self) -> None:
        """Run both services concurrently."""
        logger.info("🚀 Domain Tracker v2.0 Starting...")
        logger.info("📊 Services: Domain Monitor + Telegram Bot")
        
        try:
            # Run both services concurrently
            await asyncio.gather(
                self.run_domain_monitor(),
                self.run_telegram_bot(),
                return_exceptions=False
            )
        except KeyboardInterrupt:
            logger.info("👋 System stopped by user")
        except Exception as e:
            logger.critical(f"💥 System crashed: {e}")
            raise


def main():
    """Application entry point."""
    # Setup logging first
    setup_logging()
    
    # Create and run the application
    app = DomainTracker()
    
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.critical(f"Application crashed: {e}")
        exit(1)


if __name__ == "__main__":
    main()