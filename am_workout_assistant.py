#!/usr/bin/env python
# coding: utf-8
from datetime import datetime
from flask import Flask, request
from telegram import Telegram
from message_checker import MessageHandler
from data_updater import DataUpdater
from message import Message

supported_commands = """Supported commands:
/help - show this help
/catchups <number> - add number of catchups in this day

Supported messages:
*'<number> catchups'* or *'catchups <number>'* (catch ups is also fine)
*'<число> подтягиваний'* or *'подтягиваний <число>'*"""

# init telegram bot
bot = Telegram()
ok = bot.init()
if not ok:
    print("ERROR (bot init): {}".format(bot.get_messages()))
    exit(1)

# init message checker
msg_checker = MessageHandler()

# init data updater
du = DataUpdater()
ok = du.init()
if not ok:
    print("ERROR (data updater init): {}".format(du.get_error_message()))
    exit(1)

application = Flask(__name__)


@application.route("/", methods=['GET'])
def index():
    return "Hello from server"


@application.route("/telegram_updates", methods=['POST'])
def update_handler():
    m = Message()
    ok = m.init_json(request.json)
    if not ok:
        print("ERROR (init message): {}".format(m.get_error_message()))
        return 'fail'

    handle_message(m)
    return 'ok'


def handle_message(message):
    augment = 0
    msg_text = message.get_text()

    bot.set_chat_id(message.chat_id)

    # commands
    if msg_text.startswith('/'):
        error = ''
        if msg_text.startswith('/help'):
            bot.send_reply(supported_commands)
        elif msg_text.startswith('/catchups'):
            number = msg_text.replace('/catchups', '').lstrip()
            if number.isdigit():
                augment = number
            else:
                error = "/catchups accept only digits"
        else:
            error = "Command '{}' is unsupported. See /help.".format(msg_text)

        if error:
            bot.confirm_message(message)
            return 1
    else:
        msg_checker.set_message(msg_text)
        ok = msg_checker.check()
        if not ok:
            print("Error in message_checker: {}".format(msg_checker.get_error_message()))
            bot.send_reply(msg_checker.get_error_message())
            bot.confirm_message(message)    # don't need to re-check unsupported messages
            return 1

        augment = msg_checker.get_num_catch_ups()

    res = du.add_value(augment, message.get_date())
    if not res:
        bot.send_reply(du.get_error_message())
        return 1

    # success!
    bot.confirm_message(message)

    now = datetime.now()
    day_txt = 'day'
    if now.date() == message.get_date().date():
        day_txt = 'today'
    elif (now.date() - message.get_date().date()) == 1:
        day_txt = 'yesterday'
    bot.send_reply("Successfully added *{}*! Sum for {} is *{}*."
                   .format(augment, day_txt, res))

    return 0

if __name__ == '__main__':
    for message in bot.get_messages():
        msg_text = message.get_text()
        print("Handling message '{}'...".format(msg_text))
        handle_message(message)
