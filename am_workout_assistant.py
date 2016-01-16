#!/usr/bin/env python
from telegram import Telegram
from message_checker import MessageHandler
from data_updater import DataUpdater

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

for message in bot.get_messages():
    print("Handling message '{}'...".format(message.get_text()))
    msg_checker.set_message(message.get_text())
    ok = msg_checker.check()
    if not ok:
        bot.send_reply(msg_checker.get_error_message())
        continue

    ok = du.add_value(msg_checker.get_num_catch_ups())
    if ok == False:
        bot.send_reply(du.get_error_message())
        continue

    # success!
    bot.send_reply("Successfully added {}!".format(msg_checker.get_num_catch_ups()))
