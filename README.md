# GOC Info Bot

A simple Telegram bot built with Python.

## Features
- /start command to welcome users
- /help command for assistance
- Echo functionality for text messages

## Requirements
- Python 3.7+
- python-telegram-bot library
- Flask for web server

## Installation
1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Set your Telegram bot token as an environment variable:
   ```
   export BOT_TOKEN="your_actual_bot_token_here"
   ```
   Or on Windows:
   ```
   set BOT_TOKEN=your_actual_bot_token_here
   ```

3. Run the bot:
   ```
   python bot.py
   ```

## Web Server
This bot includes a simple web server for health checks:
```
python app.py
```
The server will be available at http://localhost:8000

## Deployment
This bot is ready for deployment to platforms like BotHost.ru with the included:
- `Procfile` for process management
- `runtime.txt` for Python version specification
- `requirements.txt` for dependencies

## Usage
After starting the bot, you can use the following commands:
- `/start` - Welcome message
- `/help` - Help information