FROM python:3.11-slim

# Setup a workdir
WORKDIR /app

# Copy files to the workdir
COPY . /app

# Setup the system dependencies
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install the dependencies for Python
RUN pip install --no-cache-dir -r requirements.txt

# Define the environment variables
ENV BOT_TOKEN=""
ENV ADMIN_IDS=""

# Specify command for starting the bot
CMD ["python", "bots/telegram/bot.py"]

# Bot's accessible port
# EXPOSE 80