import os
from dotenv import load_dotenv
import json

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
INFURA_URL = f"https://mainnet.infura.io/v3/{os.getenv('INFURA_PROJECT_ID')}"
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
CONTRACT_ABI = ''

# Function to parse ABI from file
def load_contract_abi():
    try:
        with open(os.getenv('CONTRACT_ABI_PATH'), 'r') as abi_file:
            return json.load(abi_file)
    except FileNotFoundError:
        print("ABI file not found")
        return None
    except json.JSONDecodeError:
        print("Error decoding ABI JSON")
        return None

CONTRACT_ABI = load_contract_abi()
