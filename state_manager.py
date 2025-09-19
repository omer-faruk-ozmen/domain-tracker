#!/usr/bin/env python3
"""
State Manager for Domain Tracker

Handles JSON-based state persistence for domain monitoring.
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List

from config import STATE_FILE, DEFAULT_DOMAINS

logger = logging.getLogger(__name__)


class StateManager:
    """Manages domain state persistence using JSON files."""
    
    def __init__(self):
        self.state_file = STATE_FILE
        self._ensure_state_file_exists()
    
    def _ensure_state_file_exists(self) -> None:
        """Create state file with default structure if it doesn't exist."""
        if not os.path.exists(self.state_file):
            initial_state = {
                "domains": {},
                "last_updated": None,
                "total_checks": 0
            }
            
            # Initialize with default domains
            for domain in DEFAULT_DOMAINS:
                initial_state["domains"][domain] = self._create_domain_entry()
            
            self.save_state(initial_state)
            logger.info(f"Created initial state file with {len(DEFAULT_DOMAINS)} domains")
    
    def _create_domain_entry(self) -> Dict:
        """Create a new domain entry with default values."""
        return {
            "status": "unknown",
            "last_checked": None,
            "notification_sent": False,
            "first_available_date": None,
            "last_status_change": None
        }
    
    def load_state(self) -> Dict:
        """Load domain state from JSON file."""
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                logger.debug(f"Loaded state with {len(state.get('domains', {}))} domains")
                return state
        except Exception as e:
            logger.error(f"Error loading state: {e}")
            # Return minimal state on error
            return {"domains": {}, "last_updated": None, "total_checks": 0}
    
    def save_state(self, state: Dict) -> bool:
        """Save domain state to JSON file."""
        try:
            state["last_updated"] = datetime.now().isoformat()
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            logger.debug("State saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving state: {e}")
            return False
    
    def get_domains_to_check(self) -> List[str]:
        """
        Get list of domains that need to be checked.
        Excludes domains that are already available and have been notified.
        """
        state = self.load_state()
        domains_to_check = []
        
        for domain, info in state.get("domains", {}).items():
            # Skip if domain is available and notification was already sent
            if info.get("status") == "available" and info.get("notification_sent", False):
                logger.debug(f"Skipping {domain} - already available and notified")
                continue
            
            domains_to_check.append(domain)
        
        return domains_to_check
    
    def get_domains(self) -> List[str]:
        """Get list of all domains being monitored."""
        state = self.load_state()
        return list(state.get("domains", {}).keys())
    
    def add_domain(self, domain: str) -> bool:
        """Add a new domain to monitoring."""
        try:
            domain = domain.lower().strip()
            state = self.load_state()
            
            if domain in state["domains"]:
                logger.warning(f"Domain {domain} already exists")
                return False
            
            state["domains"][domain] = self._create_domain_entry()
            success = self.save_state(state)
            
            if success:
                logger.info(f"Added domain {domain} to monitoring")
            
            return success
        except Exception as e:
            logger.error(f"Error adding domain {domain}: {e}")
            return False
    
    def reset_domain_for_monitoring(self, domain: str) -> bool:
        """
        Reset a domain to be monitored again (useful for available domains).
        """
        try:
            domain = domain.lower().strip()
            state = self.load_state()
            
            if domain not in state["domains"]:
                logger.warning(f"Domain {domain} not found")
                return False
            
            # Reset domain to unknown status so it will be checked again
            domain_info = state["domains"][domain]
            domain_info["status"] = "unknown"
            domain_info["notification_sent"] = False
            domain_info["last_status_change"] = datetime.now().isoformat()
            
            success = self.save_state(state)
            
            if success:
                logger.info(f"Reset domain {domain} for monitoring")
            
            return success
        except Exception as e:
            logger.error(f"Error resetting domain {domain}: {e}")
            return False
    
    def remove_domain(self, domain: str) -> bool:
        """Remove a domain from monitoring."""
        try:
            domain = domain.lower().strip()
            state = self.load_state()
            
            if domain not in state["domains"]:
                logger.warning(f"Domain {domain} not found")
                return False
            
            del state["domains"][domain]
            success = self.save_state(state)
            
            if success:
                logger.info(f"Removed domain {domain} from monitoring")
            
            return success
        except Exception as e:
            logger.error(f"Error removing domain {domain}: {e}")
            return False
    
    def update_domain_status(self, domain: str, is_available: bool) -> bool:
        """
        Update domain status and return True if notification should be sent.
        """
        try:
            current_time = datetime.now().isoformat()
            state = self.load_state()
            
            # Ensure domain exists
            if domain not in state["domains"]:
                state["domains"][domain] = self._create_domain_entry()
            
            domain_info = state["domains"][domain]
            previous_status = domain_info["status"]
            new_status = "available" if is_available else "unavailable"
            
            # Update basic info
            domain_info["last_checked"] = current_time
            
            # Check if status changed
            if previous_status != new_status:
                domain_info["status"] = new_status
                domain_info["last_status_change"] = current_time
                
                if is_available:
                    # Domain became available
                    domain_info["first_available_date"] = current_time
                    domain_info["notification_sent"] = False
                    self.save_state(state)
                    return True  # Send notification
                else:
                    # Domain became unavailable
                    domain_info["notification_sent"] = False
                    self.save_state(state)
                    return False
            else:
                # Status didn't change
                domain_info["status"] = new_status
                
                if is_available and not domain_info["notification_sent"]:
                    # Domain is available but we haven't sent notification yet
                    domain_info["notification_sent"] = True
                    self.save_state(state)
                    return True
                
                self.save_state(state)
                return False
                
        except Exception as e:
            logger.error(f"Error updating domain status for {domain}: {e}")
            return False
    
    def get_domain_stats(self) -> Dict:
        """Get statistics about monitored domains."""
        state = self.load_state()
        domains = state.get("domains", {})
        
        stats = {
            "total": len(domains),
            "available": 0,
            "unavailable": 0,
            "unknown": 0,
            "total_checks": state.get("total_checks", 0),
            "last_updated": state.get("last_updated", "Never")
        }
        
        for domain_info in domains.values():
            status = domain_info.get("status", "unknown")
            if status == "available":
                stats["available"] += 1
            elif status == "unavailable":
                stats["unavailable"] += 1
            else:
                stats["unknown"] += 1
        
        return stats


# Global instance
state_manager = StateManager()