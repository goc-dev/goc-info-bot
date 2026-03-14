# Bot Configuration

# Telegram Bot Token (replace with your actual token)
# You can set this as an environment variable BOT_TOKEN
import os
BOT_TOKEN = os.environ.get("API_TOKEN", "STORE_TOKEN_IN_ENV")

# Bot settings
BOT_NAME = "GOC Info Bot"
DEBUG = True

# Admin IDs (comma-separated Telegram user IDs)
ADMIN_IDS_STR = os.environ.get("ADMIN_IDS", "")
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(",") if id.strip()] if ADMIN_IDS_STR else []