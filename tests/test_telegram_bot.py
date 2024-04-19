import unittest
from unittest.mock import patch
from telegram_bot import send_telegram_message

class TestTelegramBot(unittest.TestCase):
    @patch('telegram.Bot.send_message')
    def test_send_message(self, mock_send):
        send_telegram_message("Hello, world!")
        mock_send.assert_called_once_with(chat_id='-1002030336293', text="Hello, world!")

if __name__ == '__main__':
    unittest.main()
