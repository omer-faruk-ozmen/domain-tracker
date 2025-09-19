#!/usr/bin/env python3
"""
Domain Monitor Module

Handles domain availability checking and monitoring logic.
"""

import asyncio
import asyncwhois
import logging
from datetime import datetime
from typing import List

from config import (
    RDAP_TIMEOUT, WHOIS_TIMEOUT, CHECK_INTERVAL, STATUS_REPORT_CYCLES,
    TELEGRAM_AVAILABLE_CHAT_ID, TELEGRAM_UNAVAILABLE_CHAT_ID
)
from state_manager import state_manager
from utils import send_telegram_message, format_datetime, get_status_emoji

logger = logging.getLogger(__name__)


class DomainChecker:
    """Handles domain availability checking using RDAP and WHOIS."""
    
    @staticmethod
    def _is_rdap_error_indicating_availability(error_message: str) -> bool:
        """Check if RDAP error indicates domain availability."""
        availability_indicators = [
            'domain not found', 'negative_answer_404', 'not found', 
            'no matching record', 'does not exist'
        ]
        return any(indicator in error_message.lower() for indicator in availability_indicators)
    
    @staticmethod
    def _has_registration_indicators(parsed_dict: dict) -> bool:
        """Check if parsed WHOIS data contains registration indicators."""
        registration_indicators = [
            'created', 'creation_date', 'registered', 'registrar', 'domain_name', 
            'expires', 'expiry_date', 'updated', 'status'
        ]
        
        for key in registration_indicators:
            if key in parsed_dict and parsed_dict[key]:
                return True
        return False
    
    @staticmethod
    def _check_query_string_for_availability(query_string: str) -> bool:
        """Check raw query string for availability patterns."""
        not_found_patterns = [
            'no match', 'not found', 'no data found', 'not exist',
            'no entries found', 'no matching record', 'available',
            'not registered', 'no such domain', 'domain not found'
        ]
        
        query_lower = query_string.lower()
        return any(pattern in query_lower for pattern in not_found_patterns)
    
    @staticmethod
    async def _try_rdap_query(domain: str) -> tuple:
        """Try RDAP query with timeout."""
        return await asyncio.wait_for(
            asyncwhois.aio_rdap(domain),
            timeout=RDAP_TIMEOUT
        )
    
    @staticmethod
    async def _try_whois_query(domain: str) -> tuple:
        """Try WHOIS query with timeout."""
        return await asyncio.wait_for(
            asyncwhois.aio_whois(domain),
            timeout=WHOIS_TIMEOUT
        )
    
    async def check_domain_availability(self, domain: str) -> bool:
        """
        Check if a domain is available for registration using asyncwhois.
        Returns True if domain is available, False if taken.
        """
        try:
            # Try RDAP first (usually faster), then fallback to WHOIS
            try:
                query_string, parsed_dict = await self._try_rdap_query(domain)
            except Exception as rdap_error:
                if self._is_rdap_error_indicating_availability(str(rdap_error)):
                    return True
                
                # Otherwise try WHOIS fallback
                try:
                    query_string, parsed_dict = await self._try_whois_query(domain)
                except OSError as whois_error:
                    logger.warning(f"Network error for {domain}: {whois_error}")
                    return False  # Assume unavailable on network errors
            
            # Check if domain is registered based on parsed data
            if parsed_dict and self._has_registration_indicators(parsed_dict):
                return False  # Domain is registered
            
            # Check raw query string for availability patterns
            if query_string and self._check_query_string_for_availability(query_string):
                return True
            
            # Default to unavailable for safety
            return False
            
        except asyncio.TimeoutError:
            logger.warning(f"Timeout checking {domain}")
            return False
        except asyncwhois.NotFoundError:
            return True
        except OSError as e:
            logger.warning(f"Network error checking {domain}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error checking {domain}: {type(e).__name__}")
            return False


class DomainMonitor:
    """Main domain monitoring class."""
    
    def __init__(self):
        self.checker = DomainChecker()
        self.cycle_count = 0
    
    async def monitor_single_domain(self, domain: str) -> None:
        """Monitor a single domain and handle notifications."""
        try:
            is_available = await self.checker.check_domain_availability(domain)
            should_notify = state_manager.update_domain_status(domain, is_available)
            
            if should_notify and is_available:
                await self._send_availability_notification(domain)
                
        except Exception as e:
            logger.error(f"Error monitoring domain {domain}: {e}")
    
    async def _send_availability_notification(self, domain: str) -> None:
        """Send Telegram notification for newly available domain."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = "🚨 <b>DOMAIN AVAILABLE!</b> 🚨\n\n"
        message += f"Domain: <code>{domain}</code>\n"
        message += "Status: ✅ Available for registration\n"
        message += f"Time: {current_time}\n\n"
        message += "Act fast! Register this domain now!"
        
        success = await send_telegram_message(message, TELEGRAM_AVAILABLE_CHAT_ID)
        if success:
            logger.critical(f"ALERT: {domain} is AVAILABLE - Notification sent!")
        else:
            logger.error(f"Failed to send availability notification for {domain}")
    
    async def monitor_all_domains(self) -> None:
        """Monitor all domains concurrently (excluding already available ones)."""
        domains = state_manager.get_domains_to_check()  # Use new method
        if not domains:
            logger.info("No domains need checking (all may be available and notified)")
            return
        
        total_domains = len(state_manager.get_domains())
        logger.info(f"Monitoring {len(domains)}/{total_domains} domains: {', '.join(domains)}")
        
        # Monitor all domains concurrently
        tasks = [self.monitor_single_domain(domain) for domain in domains]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def send_status_report(self) -> None:
        """Send periodic status report."""
        try:
            stats = state_manager.get_domain_stats()
            state = state_manager.load_state()
            domains = state.get("domains", {})
            
            available_domains = []
            unavailable_domains = []
            
            for domain, info in domains.items():
                if info.get("status") == "available":
                    available_domains.append((domain, info))
                else:
                    unavailable_domains.append((domain, info))
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            message = "📊 <b>Domain Monitoring Status Report</b>\n\n"
            message += f"🔄 Cycle: #{self.cycle_count}\n"
            message += f"⏰ Time: {current_time}\n"
            message += f"📋 Total domains: {stats['total']}\n"
            message += f"✅ Available: {stats['available']}\n"
            message += f"⏳ Unavailable: {stats['unavailable']}\n"
            message += f"❓ Unknown: {stats['unknown']}\n"
            message += f"🔍 Total checks: {stats['total_checks']}\n\n"
            
            if available_domains:
                message += f"✅ <b>Available domains ({len(available_domains)}):</b>\n"
                for domain, info in available_domains:
                    first_available = format_datetime(info.get("first_available_date", ""))
                    message += f"   • {domain} (since: {first_available})\n"
                message += "\n"
            
            if unavailable_domains:
                message += f"⏳ <b>Still unavailable ({len(unavailable_domains)}):</b>\n"
                for domain, info in unavailable_domains[:10]:  # Limit to first 10
                    last_checked = format_datetime(info.get("last_checked", ""), "Never")
                    message += f"   • {domain} (checked: {last_checked})\n"
                
                if len(unavailable_domains) > 10:
                    message += f"   ... and {len(unavailable_domains) - 10} more\n"
                message += "\n"
            
            message += f"🤖 Next report in {STATUS_REPORT_CYCLES} cycles"
            
            success = await send_telegram_message(message, TELEGRAM_UNAVAILABLE_CHAT_ID)
            if success:
                logger.info(f"Status report sent (Cycle #{self.cycle_count})")
            else:
                logger.error("Failed to send status report")
                
        except Exception as e:
            logger.error(f"Error sending status report: {e}")
    
    async def run(self) -> None:
        """Main monitoring loop."""
        logger.info("Domain monitoring started")
        
        try:
            while True:
                self.cycle_count += 1
                
                # Update state with current cycle count
                state = state_manager.load_state()
                state["total_checks"] = self.cycle_count
                state_manager.save_state(state)
                
                # Monitor all domains
                await self.monitor_all_domains()
                
                # Send status report every N cycles
                if self.cycle_count % STATUS_REPORT_CYCLES == 0:
                    await self.send_status_report()
                
                # Wait before next cycle
                logger.debug(f"Cycle {self.cycle_count} completed, waiting {CHECK_INTERVAL}s")
                await asyncio.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("Domain monitoring stopped by user")
        except Exception as e:
            logger.critical(f"Domain monitoring crashed: {e}")
            raise