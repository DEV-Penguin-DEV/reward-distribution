# Ethereum Reward Distribution Bot

This Telegram bot monitors reward distribution events on an Ethereum contract and sends daily statistics to a specified Telegram group. The bot also stores event data in a PostgreSQL database for further analysis and reporting.

## Features

- Monitors Ethereum blockchain for specific contract events.
- Stores events data in a PostgreSQL database.
- Sends automated reports every four hours to a Telegram group.
- Can backfill data on startup to recover from downtime.

## Prerequisites

Before you start, make sure you have installed the following:
- Python 3.8 or higher
- PostgreSQL
- pip packages: `web3`, `python-telegram-bot`, `psycopg2-binary`, `python-dotenv`, `pytest`, `pytest-mock`, `schedule`

## Setup

### Step 1: Clone the repository

Clone this repository to your local machine using:
```bash
git clone https://github.com/yourgithub/reward-distribution-bot.git
cd reward-distribution-bot
```

### Step 2: Install Dependencies

Install the required Python libraries by running:
```bash
    pip install -r requirements.txt
```

### Step 3: Configuration

Create a .env file in the root directory and update it with your credentials and configurations:

```yml
DB_USER=username
DB_PASSWORD=admin
DB_NAME=reward-distribution
HOST=localhost

# Telegram bot
TELEGRAM_TOKEN=7010282781:AAF-zjrGH8oAmflhWx0h0Jd-8QeWagFMmas
TELEGRAM_CHAT_ID=testeth2

# Infura project
INFURA_PROJECT_ID=669b9e0845e24f21903587ce8a8e3f2c

# Ethereum Contract
CONTRACT_ADDRESS=0xaBE235136562a5C2B02557E1CaE7E8c85F2a5da0

# ABI 
CONTRACT_ABI_PATH=/contract-abi.json
```

### Step 5: Run the Bot

Execute the bot with:

```bash
    python3 main.py
```