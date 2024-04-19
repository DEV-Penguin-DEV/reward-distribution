import logging
from db_manager import create_table
from telegram_bot import send_telegram_message, start_regular_reports

logging.basicConfig(level=logging.INFO)

def start_bot() -> None:
    """
    Starts the bot, initializes database tables, and sends a startup message.
    """
    try:
        logging.info("Starting the bot...")
        create_table()  # Attempt to create the database table if it doesn't exist.
        logging.info("Table creation attempted...")
        
        send_telegram_message("Bot started successfully and listening for events.")
        logging.info("Startup message sent.")
        
        start_regular_reports()  # Begin scheduling regular report sending.
    except Exception as e:
        logging.error(f"Failed to start the bot: {str(e)}")

if __name__ == "__main__":
    start_bot()
