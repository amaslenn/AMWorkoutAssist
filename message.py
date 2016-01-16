#!/usr/bin/env python
import unittest
from datetime import datetime

class Message:
    text = ''
    date = None
    error_message = ''
    update_id = 0

    def __init__(self):
        self.text = ''
        self.date = None
        self.error_message = ''
        self.update_id = 0

    def init(self, telegram_update):
        if not telegram_update:
            self.error_message = "Telegram Update is not defined"
            return False

        message = telegram_update.message

        self.text = message.text
        self.date = datetime.fromtimestamp(message.date)
        self.update_id = telegram_update.update_id

        return True

    def get_text(self):
        return self.text

    def get_date(self):
        return self.date

    def get_update_id(self):
        return self.update_id

    def get_error_message(self):
        return self.error_message


class t_Message(unittest.TestCase):
    """Tests for Message"""
    def test_init(self):
        m = Message()
        ret = m.init()
        self.assertEqual(False, ret, msg='Check object initialization')

if __name__ == '__main__':
    unittest.main()
