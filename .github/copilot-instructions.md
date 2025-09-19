# Copilot Instructions for AI Agents

## Project Overview

This is a domain backorder monitoring application that checks domain availability using asyncwhois and sends Telegram notifications when domains become available for registration. The application runs continuously with 30-second intervals between checks.

## Environment

- The project uses a local virtual environment located in `myenv/`.
- The Python interpreter is at `myenv/Scripts/python.exe`.
- Dependencies: `asyncwhois`, `aiohttp` for async HTTP requests to Telegram API.

## Key Files and Structure

- `app.py`: Main application with domain monitoring logic, Telegram integration, and async scheduling.
- `myenv/`: Python virtual environment. Do not modify or commit files in this directory.

## Configuration

Before running, update these constants in `app.py`:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID where notifications will be sent
- `DOMAINS_TO_MONITOR`: List of domains to monitor for availability

## Development Workflow

- To run the application: `myenv/Scripts/python.exe app.py`
- To install packages: `myenv/Scripts/pip.exe install <package>`
- The app runs continuously until stopped with Ctrl+C

## Architecture

- **Domain Monitoring**: Uses `asyncwhois.aio_whois()` to check domain registration status
- **Rate Limiting**: 30-second intervals between check cycles to respect rate limits
- **Telegram Notifications**: Async HTTP requests to Telegram Bot API when domains become available
- **State Tracking**: Maintains `previously_unavailable_domains` set to detect state changes

## Example: Adding a Domain to Monitor

Edit the `DOMAINS_TO_MONITOR` list in `app.py`:

```python
DOMAINS_TO_MONITOR = [
    "example.com",
    "your-desired-domain.com"
]
```

## Example: Running the App

```pwsh
myenv/Scripts/python.exe app.py
```

---

If you add new files, update this document to reflect new conventions or workflows.
