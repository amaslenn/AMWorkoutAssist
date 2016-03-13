#!/usr/bin/env python
import unittest
from datetime import datetime


class Message:
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

    def init_json(self, update):
        if not update:
            self.error_message = "JSON update is not defined"
            return False

        if 'update_id' not in update:
            self.error_message = "JSON doesn't contain 'update_id'"
            return False

        if 'message' not in update:
            self.error_message = "JSON doesn't contain 'message'"
            return False

        message = update['message']
        if 'text' not in message:
            self.error_message = "JSON message doesn't contain 'text'"
            return False

        if 'date' not in message:
            self.error_message = "JSON message doesn't contain 'date'"
            return False

        self.text = message['text']
        self.date = datetime.fromtimestamp(message['date'])
        self.update_id = update['update_id']

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
        ret = m.init(None)
        self.assertEqual(False, ret, msg='Check object initialization')

    def test_init_json(self):
        m = Message()
        ret = m.init_json({})
        self.assertEqual(False, ret, msg='init_json({})')

    def test_init_json2(self):
        m = Message()
        ret = m.init_json({'update_id': 2})
        self.assertEqual(False, ret, msg="init_json({'update_id': 2})")

    def test_init_json3(self):
        m = Message()
        ret = m.init_json({'update_id': 2, 'message': {}})
        self.assertEqual(False, ret, msg="init_json({'update_id': 2, 'message': {}})")

    def test_init_json4(self):
        m = Message()
        ret = m.init_json({'update_id': 2, 'message': {'text': 'sample text'}})
        self.assertEqual(False, ret, msg="init_json(): no date")

    def test_init_json5(self):
        m = Message()
        ret = m.init_json({'update_id': 2, 'message': {'text': 'sample text', 'date': 1438004886}})
        self.assertEqual(True, ret, msg="init_json(): OK")

if __name__ == '__main__':
    unittest.main()
