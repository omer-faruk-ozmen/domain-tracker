# Google VM Deployment Guide

## Quick Setup for Google VM

### 1. Prerequisites Check

```bash
python3 check.py
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure

Edit `config.py`:

```python
TELEGRAM_BOT_TOKEN = "your_actual_bot_token"
TELEGRAM_AVAILABLE_CHAT_ID = "your_chat_id"
TELEGRAM_UNAVAILABLE_CHAT_ID = "your_chat_id"
```

### 4. Run Application

```bash
python3 main.py
```

## Alternative Startup Methods

### Method 1: Direct Run

```bash
python3 main.py
```

### Method 2: Using Wrapper Script

```bash
python3 start.py
```

### Method 3: With Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError: No module named 'config'`:

1. Make sure you're in the correct directory:

   ```bash
   ls -la
   # Should show: config.py, main.py, etc.
   ```

2. Use the wrapper script:

   ```bash
   python3 start.py
   ```

3. Check Python path:
   ```bash
   python3 -c "import sys; print(sys.path)"
   ```

### Network Issues

Google VM should have no network restrictions for external APIs.

### Permission Issues

Make sure scripts are executable:

```bash
chmod +x *.py
```

## Service Setup (Optional)

Create a systemd service for auto-start:

1. Create service file:

```bash
sudo nano /etc/systemd/system/domain-tracker.service
```

2. Add content:

```ini
[Unit]
Description=Domain Tracker
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/domain-tracker
ExecStart=/usr/bin/python3 /home/your_username/domain-tracker/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Enable and start:

```bash
sudo systemctl enable domain-tracker
sudo systemctl start domain-tracker
sudo systemctl status domain-tracker
```

## Monitoring

Check logs:

```bash
tail -f logs/domain_tracker_*.log
```

Check status:

```bash
ps aux | grep python
```
