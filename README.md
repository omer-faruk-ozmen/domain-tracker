# Domain Tracker v2.0

Professional domain backorder monitoring system with Telegram integration.

## 🚀 Features

- **Async Domain Monitoring**: RDAP + WHOIS checking with optimal timeouts
- **Instant Notifications**: Telegram alerts when domains become available
- **Bot Interface**: Manage domains via Telegram commands
- **Persistent State**: JSON-based domain tracking across restarts
- **Smart Logging**: Daily rotating logs with optimized output
- **Production Ready**: Error handling, rate limiting, concurrent processing

## 📁 Project Structure

```
domain-tracker/
├── main.py              # 🚀 Main entry point
├── config.py            # ⚙️ Configuration settings
├── domain_monitor.py    # 🔍 Domain checking logic
├── telegram_bot_new.py  # 🤖 Telegram bot interface
├── state_manager.py     # 💾 JSON state persistence
├── utils.py             # 🛠️ Common utilities
├── domain_state.json    # 📊 Domain tracking data (auto-created)
├── requirements.txt     # 📦 Python dependencies
└── logs/               # 📝 Daily log files
```

## 🔧 Setup

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Settings**:
   Edit `config.py` with your:

   - Telegram bot token
   - Chat IDs for notifications
   - Monitoring intervals

3. **Run Application**:
   ```bash
   python main.py
   ```

## 🤖 Telegram Commands

Available in both notification chats:

- `/add <domain>` - Add domain to monitoring
- `/remove <domain>` - Remove domain from monitoring
- `/list` - Show all monitored domains
- `/status` - Show monitoring statistics
- `/help` - Show command help

### Examples:

```
/add example.com
/add test.org
/list
/remove example.com
/status
```

## 📊 State Management

Domain states are automatically saved to `domain_state.json`:

```json
{
  "domains": {
    "example.com": {
      "status": "available",
      "last_checked": "2025-09-19T17:30:00",
      "notification_sent": true,
      "first_available_date": "2025-09-19T17:25:00",
      "last_status_change": "2025-09-19T17:25:00"
    }
  },
  "last_updated": "2025-09-19T17:30:00",
  "total_checks": 1500
}
```

## ⚙️ Configuration

Key settings in `config.py`:

- `CHECK_INTERVAL`: Seconds between domain checks (default: 60)
- `STATUS_REPORT_CYCLES`: Cycles between status reports (default: 120)
- `RDAP_TIMEOUT`: RDAP query timeout (default: 10s)
- `WHOIS_TIMEOUT`: WHOIS query timeout (default: 25s)

## 📝 Logging

- **Location**: `logs/domain_tracker_YYYY-MM-DD.log`
- **Rotation**: Daily files
- **Levels**: INFO for operations, CRITICAL for alerts
- **Format**: Timestamp + Module + Level + Message

## 🔒 Security

- Only authorized chat IDs can use bot commands
- State file excluded from git via `.gitignore`
- Error handling prevents crashes from invalid domains
- Rate limiting respects service provider limits

## 🚀 Production Deployment

1. **Environment Setup**:

   ```bash
   # Create virtual environment
   python -m venv myenv
   myenv/Scripts/activate  # Windows
   # source myenv/bin/activate  # Linux/Mac

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Run as Service**:

   ```bash
   # Direct execution
   python main.py

   # Background execution (Linux)
   nohup python main.py &

   # Windows Service
   # Use NSSM or similar service wrapper
   ```

3. **Monitoring**:
   - Check logs for errors: `logs/domain_tracker_*.log`
   - Monitor Telegram for notifications
   - Use `/status` command for health checks

## 🔄 Migration from v1.0

1. Backup existing `domain_state.json`
2. Install new version
3. Update `config.py` with your settings
4. Run `python main.py`

Old files (`app.py`, `run_all.py`) can be safely deleted.

## 📞 Support

- **Logs**: Check daily log files for errors
- **State**: Inspect `domain_state.json` for domain status
- **Bot**: Use `/help` command for available options
- **Manual**: Edit `domain_state.json` to add/remove domains manually

---

**Domain Tracker v2.0** - Professional domain monitoring made simple! 🎯
