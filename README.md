# 📡 XUI Telegram Monitoring Bot

A lightweight and efficient Telegram bot built with `aiogram` for monitoring multiple servers using the **3x-ui** panel.

## 🔧 Features

- Add and manage servers via Telegram interface
- View server statistics:
  - Total number of users
  - Number of active (online) keys
  - Number of expired keys
- Automatic monitoring every 10 minutes
  - Sends alerts if:
    - Online users < 10
    - Expired keys > 10
    - Server is unreachable

## 🚀 Getting Started with Docker

1. **Build the Docker image:**

```bash
docker build -t xui-bot .
```

2. **Run the container:**

```bash
docker run -d --restart=always --name xui_monitor_bot xui-bot
```

> ✅ The bot will start automatically and begin monitoring all servers listed in the `servers.db` SQLite database.

## 📁 Project Structure

```
.
├── bot.py                  # Main entry point
├── config.py               # Telegram token configuration
├── database.py             # SQLite helper functions
├── services/
│   └── xui_api.py          # Interaction with 3x-ui API
├── handlers/
│   ├── commands.py         # Command handlers (/start, /add, etc.)
│   ├── buttons.py          # Inline button callbacks
│   └── messages.py         # Message responses
├── keyboards/
│   └── inline.py           # Inline keyboard definitions
└── monitor.py              # Background monitoring logic
```

## ⚙️ Configuration

Create a `config.py` file with the following content:

```python
TELEGRAM_TOKEN = "your_bot_token_here"
```

## 📬 Feedback & Contributions

Built with ❤️ for internal use. Feel free to open an issue or submit a pull request if you'd like to contribute or suggest improvements.
