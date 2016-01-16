#!/usr/bin/env python
import unittest
from twx.botapi import TelegramBot, Message
from message import Message as Msg
from datetime import datetime

TELEGRAM_TOKEN_FILE = 'telegram_token'
LAST_UPDATE_ID_STORAGE = '.cache'

class Telegram:
    initialized = False
    bot = None
    last_update_id = 0
    error_message = ''
    errors = dict()
    chat_id = None

    def __init__(self):
        self.initialized = False
        self.bot = None
        self.last_update_id = 0
        self.error_message = ''
        self.errors = dict()
        self.chat_id = None

    def _store_last_update_id(self):
        f = open(LAST_UPDATE_ID_STORAGE, 'w')
        f.write(str(self.last_update_id))
        f.close()

    def _restore_last_update_id(self):
        try:
            f = open(LAST_UPDATE_ID_STORAGE)
            self.last_update_id = f.read()
            f.close()
        except:
            pass

    def init(self):
        # init Telegram bot through API
        f = open(TELEGRAM_TOKEN_FILE)
        bot = TelegramBot(f.read())
        f.close()
        if not bot:
            self.error_message = 'Cannot initialize Bot'
            return False

        self._restore_last_update_id()

        self.initialized = True
        self.bot = bot

        return True

    def get_messages(self):
        if not self.initialized:
            self.error_message = 'Cannot get messages for non initialized Bot'
            return []

        messages = []
        updates = self.bot.get_updates(offset=self.last_update_id).wait()
        for update in updates:
            # always increase last_update_id to get only new messages next time
            self.last_update_id = update.update_id + 1
            self.chat_id = update.message.chat.id

            # skip all types of message except Message
            if not update.message or not isinstance(update.message, Message):
                continue

            m = Msg()
            ok = m.init(update)
            if not ok:
                self.errors[update.message.text] = m.get_error_message()
                continue

            messages.append(m)

        self._store_last_update_id()

        return messages

    def send_reply(self, reply):
        if not self.chat_id:
            self.error_message = 'Chat ID is not defined'
            return False

        m = self.bot.send_message(chat_id=self.chat_id, text=reply)
        if not m or not isinstance(m, Message):
            self.error_message = "Error sending message '{}'".format(reply)
            return False

        return True

class t_Telegram(unittest.TestCase):
    """Tests for Telegram"""
    def test_init(self):
        m = Telegram()
        ret = m.init()
        self.assertEqual(True, ret, msg='Check object initialization')

if __name__ == '__main__':
    unittest.main()
