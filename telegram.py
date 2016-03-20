#!/usr/bin/env python
import os
import unittest
from twx.botapi import TelegramBot, Message
from message import Message as Msg

TELEGRAM_TOKEN_FILE = 'telegram_token'
LAST_UPDATE_ID_STORAGE = '.cache'


class Telegram:
    def __init__(self):
        self.initialized = False
        self.bot = None
        self.last_update_id = 0
        self.error_message = ''
        self.errors = dict()
        self.chat_id = None

    def init(self):
        # init Telegram bot through API
        token = os.environ.get('TELEGRAM_TOKEN')
        if not token:
            f = open(TELEGRAM_TOKEN_FILE)
            token = f.read()
            f.close()
        bot = TelegramBot(token)
        if not bot:
            self.error_message = 'Cannot initialize Bot'
            return False

        self.initialized = True
        self.bot = bot

        return True

    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

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

        return messages

    def confirm_message(self, msg):
        """Get Updates for Message's update id + 1 to mark it as confirmed"""
        self.bot.get_updates(offset=msg.get_update_id() + 1).wait()

    def send_reply(self, reply):
        if not self.chat_id:
            self.error_message = 'Chat ID is not defined'
            return False

        m = self.bot.send_message(chat_id=self.chat_id, text=reply, parse_mode="Markdown")
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
