#!/usr/bin/env python3
"""
Telegram Bot Module
"""

import asyncio
import aiohttp
import logging
from datetime import datetime
from typing import Dict, List

from config import (
    TELEGRAM_BOT_TOKEN, TELEGRAM_AVAILABLE_CHAT_ID, TELEGRAM_UNAVAILABLE_CHAT_ID
)
from state_manager import state_manager
from utils import send_telegram_message, format_datetime_short, get_status_emoji, validate_domain

logger = logging.getLogger(__name__)


class TelegramBot:
    """Handles Telegram bot commands for domain management."""
    
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.authorized_chat_ids = [TELEGRAM_AVAILABLE_CHAT_ID, TELEGRAM_UNAVAILABLE_CHAT_ID]
        self.offset = 0
    
    async def get_updates(self) -> List[Dict]:
        """Get new messages from Telegram."""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
            params = {
                "offset": self.offset,
                "timeout": 30,
                "allowed_updates": ["message"]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=35) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("result", [])
                    else:
                        logger.error(f"Failed to get updates: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error getting updates: {e}")
            return []
    
    def is_authorized(self, chat_id: str) -> bool:
        """Check if chat is authorized to use bot commands."""
        return str(chat_id) in [str(cid) for cid in self.authorized_chat_ids]
    
    def handle_add_command(self, domain: str) -> str:
        """Add domain to monitoring list."""
        try:
            # Validate domain format
            if not validate_domain(domain):
                return "❌ Invalid domain format. Please provide a valid domain (e.g., example.com)"
            
            domain = domain.lower().strip()
            
            # Add domain using state manager
            success = state_manager.add_domain(domain)
            
            if success:
                logger.info(f"Added domain {domain} via Telegram command")
                return f"✅ Domain <code>{domain}</code> added to monitoring list successfully!"
            else:
                return f"⚠️ Domain <code>{domain}</code> is already being monitored."
            
        except Exception as e:
            logger.error(f"Error adding domain {domain}: {e}")
            return f"❌ Error adding domain: {str(e)}"
    
    def handle_reset_command(self, domain: str) -> str:
        """Reset domain to be monitored again."""
        try:
            # Validate domain format
            if not validate_domain(domain):
                return "❌ Invalid domain format. Please provide a valid domain (e.g., example.com)"
            
            domain = domain.lower().strip()
            
            # Check if domain exists
            domains = state_manager.get_domains()
            if domain not in domains:
                return f"❌ Domain {domain} is not being monitored. Use /add to add it first."
            
            # Reset domain
            success = state_manager.reset_domain_for_monitoring(domain)
            
            if success:
                return f"✅ Domain {domain} has been reset and will be monitored again."
            else:
                return f"❌ Failed to reset domain {domain}. Please try again."
                
        except Exception as e:
            logger.error(f"Error in reset command for domain {domain}: {e}")
            return f"❌ Error resetting domain {domain}. Please try again."
    
    def handle_remove_command(self, domain: str) -> str:
        """Remove domain from monitoring list."""
        try:
            domain = domain.lower().strip()
            
            # Remove domain using state manager
            success = state_manager.remove_domain(domain)
            
            if success:
                logger.info(f"Removed domain {domain} via Telegram command")
                return f"✅ Domain <code>{domain}</code> removed from monitoring list successfully!"
            else:
                return f"⚠️ Domain <code>{domain}</code> is not in the monitoring list."
            
        except Exception as e:
            logger.error(f"Error removing domain {domain}: {e}")
            return f"❌ Error removing domain: {str(e)}"
    
    def handle_list_command(self) -> str:
        """List all monitored domains."""
        try:
            state = state_manager.load_state()
            domains = state.get("domains", {})
            
            if not domains:
                return "📋 No domains are currently being monitored."
            
            message = f"📋 <b>Monitored Domains ({len(domains)}):</b>\n\n"
            
            for domain, info in domains.items():
                status = info.get("status", "unknown")
                status_emoji = get_status_emoji(status)
                
                message += f"{status_emoji} <code>{domain}</code> ({status})\n"
            
            return message
            
        except Exception as e:
            logger.error(f"Error listing domains: {e}")
            return f"❌ Error retrieving domain list: {str(e)}"
    
    def handle_status_command(self) -> str:
        """Show current monitoring status."""
        try:
            stats = state_manager.get_domain_stats()
            
            message = "📊 <b>Domain Monitoring Status</b>\n\n"
            message += f"📋 Total domains: {stats['total']}\n"
            message += f"✅ Available: {stats['available']}\n"
            message += f"⏳ Monitoring: {stats['unavailable']}\n\n"
            message += "Use /list to see detailed domain status."
            
            return message
            
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return f"❌ Error retrieving status: {str(e)}"
    
    def handle_logs_command(self) -> str:
        """Show last 10 log entries."""
        try:
            from datetime import datetime
            import os
            
            # Get today's log file
            today = datetime.now().strftime("%Y-%m-%d")
            log_file = f"logs/domain_tracker_{today}.log"
            
            if not os.path.exists(log_file):
                return "� No log file found for today"
            
            # Read last 10 lines
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Get last 10 lines (or all if less than 10)
            last_lines = lines[-10:] if len(lines) >= 10 else lines
            
            if not last_lines:
                return "📝 Log file is empty"
            
            message = "� <b>Last 10 Log Entries:</b>\n\n"
            for line in last_lines:
                line = line.strip()
                if line:
                    # Format time and make it more readable
                    if ' - ' in line:
                        parts = line.split(' - ', 2)
                        if len(parts) >= 3:
                            timestamp = parts[0]
                            level = parts[1]
                            msg = parts[2]
                            # Show only time (HH:MM:SS)
                            if ',' in timestamp:
                                time_part = timestamp.split(',')[0].split(' ')[-1]
                                message += f"<code>{time_part}</code> {level}: {msg}\n"
                            else:
                                message += f"<code>{line}</code>\n"
                        else:
                            message += f"<code>{line}</code>\n"
                    else:
                        message += f"<code>{line}</code>\n"
            
            return message
            
        except Exception as e:
            logger.error(f"Error reading logs: {e}")
            return f"❌ Error reading log file: {e}"
    
    def handle_help_command(self) -> str:
        """Show available commands."""
        return """🤖 <b>Domain Tracker Bot Commands</b>

<b>Domain Management:</b>
/add &lt;domain&gt; - Add domain to monitoring
/remove &lt;domain&gt; - Remove domain from monitoring
/reset &lt;domain&gt; - Reset available domain to monitoring

<b>Information:</b>
/list - Show all monitored domains  
/status - Show monitoring statistics
/logs - Show last 10 log entries
/help - Show this help message

<b>Examples:</b>
<code>/add example.com</code>
<code>/remove example.com</code>
<code>/reset example.com</code>

<b>Note:</b> Available in both monitoring chats."""
    
    async def process_message(self, message: Dict) -> None:
        """Process incoming Telegram message."""
        try:
            chat_id = message["chat"]["id"]
            text = message.get("text", "").strip()
            
            # Check authorization
            if not self.is_authorized(chat_id):
                logger.warning(f"Unauthorized bot access attempt from chat_id: {chat_id}")
                return
            
            # Parse command
            if not text.startswith("/"):
                return
            
            parts = text.split()
            command = parts[0].lower()
            
            # Remove bot username from command if present (e.g., /logs@botname -> /logs)
            if "@" in command:
                command = command.split("@")[0]
            
            response = ""
            
            if command == "/add" and len(parts) >= 2:
                domain = parts[1]
                response = self.handle_add_command(domain)
                
            elif command == "/remove" and len(parts) >= 2:
                domain = parts[1]
                response = self.handle_remove_command(domain)
                
            elif command == "/reset" and len(parts) >= 2:
                domain = parts[1]
                response = self.handle_reset_command(domain)
                
            elif command == "/list":
                response = self.handle_list_command()
                
            elif command == "/status":
                response = self.handle_status_command()
                
            elif command == "/logs":
                response = self.handle_logs_command()
                
            elif command == "/help":
                response = self.handle_help_command()
                
            else:
                response = "❓ Unknown command. Use /help to see available commands."
            
            # Send response
            if response:
                await send_telegram_message(response, str(chat_id))
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    async def run(self) -> None:
        """Main bot loop."""
        logger.info("Telegram bot started - listening for commands...")
        
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while True:
            try:
                updates = await self.get_updates()
                
                if updates:
                    consecutive_errors = 0  # Reset error counter on success
                
                for update in updates:
                    # Update offset
                    self.offset = update["update_id"] + 1
                    
                    # Process message
                    if "message" in update:
                        await self.process_message(update["message"])
                
                # Small delay to prevent API spam
                await asyncio.sleep(1)
                
            except KeyboardInterrupt:
                logger.info("Telegram bot stopped by user")
                break
            except Exception as e:
                consecutive_errors += 1
                logger.error(f"Error in bot loop: {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    logger.warning(f"Too many consecutive errors ({consecutive_errors}), increasing delay")
                    await asyncio.sleep(30)  # Wait longer on repeated errors
                    consecutive_errors = 0
                else:
                    await asyncio.sleep(5)