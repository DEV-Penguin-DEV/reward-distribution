import time
import schedule
from telegram import Bot
from telegram.error import TelegramError

from config import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
from event_listener import generate_report

# Bot initialization
bot = Bot(token=TELEGRAM_TOKEN)

def send_telegram_message(message: str) -> None:
    """
    Sends a message to a specified Telegram chat.

    Args:
        message (str): The message to be sent to the Telegram chat.
    """
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except TelegramError as e:
        print(f"Failed to send message due to an error: {e}")

def send_regular_reports() -> None:
    """
    Retrieves the report from the database and sends it to the Telegram channel.
    """
    try:
        result = generate_report()
        if result:
            message = format_report_message(result)
            send_telegram_message(message)
        else:
            send_telegram_message("No transactions to report for the last day.")
    except Exception as e:
        send_telegram_message(f"Failed to fetch report data: {e}")

def format_report_message(result: dict) -> str:
    """
    Formats the report data into a readable message for sending to Telegram.

    Args:
        result (dict): The result dictionary containing report data.

    Returns:
        str: Formatted message string.
    """
    return (
        "Daily $AIX Stats:\n"
        f"    - First TX: {result['first_tx']}\n"
        f"    - Last TX: {result['last_tx']}\n"
        f"    - AIX processed: {result['aix_processed']:,.2f}\n"
        f"    - AIX distributed: {result['aix_distributed']:,.2f}\n"
        f"    - ETH bought: {result['eth_bought']:,.2f}\n"
        f"    - ETH distributed: {result['eth_distributed']:,.2f}\n\n"
        f"    Distributor wallet: {'0x9A0A9594Aa626EE911207DC001f535c9eb590b34'}\n"
        f"    Distributor balance: {result['eth_balance']} ETH\n"
    )

def start_regular_reports() -> None:
    """
    Schedules regular report sending every 4 hours.
    """
    schedule.every(4).hours.do(send_regular_reports)
    while True:
        schedule.run_pending()
        time.sleep(1)
