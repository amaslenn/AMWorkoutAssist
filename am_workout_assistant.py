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
    msg_text = message.get_text()
    print("Handling message '{}'...".format(msg_text))

    # commands
    if msg_text.startswith('/'):
        if msg_text.startswith('/help'):
            bot.send_reply("Supported commands:\n" +
                           "/help - show this help\n" +
                           "/catchups <number> - add number of catchups in this day\n" +
                           "\nSupported messages:\n" +
                           "*'<number> catchups'* or *'catchups <number>'* (catch ups is also fine)\n" +
                           "*'<число> подтягиваний'* or *'подтягиваний <число>'*")
        elif msg_text.startswith('/catchups'):
            number = msg_text.replace('/catchups', '').lstrip()
            if number.isdigit():
                res = du.add_value(number, message.get_date())
                if res == False:
                    bot.send_reply(du.get_error_message())
                else:
                    bot.send_reply("Successfully added *{}*! Sum for the day is *{}*."
                                   .format(number, res))
            else:
                bot.send_reply("/catchups accept only digits")
        else:
            bot.send_reply("Command '{}' is unsupported. See /help.".format(msg_text))

        bot.confirm_message(message)
        continue

    msg_checker.set_message(msg_text)
    ok = msg_checker.check()
    if not ok:
        bot.send_reply(msg_checker.get_error_message())
        bot.confirm_message(message)    # don't need to re-check unsupported messages
        continue

    res = du.add_value(msg_checker.get_num_catch_ups(), message.get_date())
    if res == False:
        bot.send_reply(du.get_error_message())
        continue

    # success!
    bot.confirm_message(message)
    bot.send_reply("Successfully added *{}*! Sum for the day is *{}*."
                   .format(msg_checker.get_num_catch_ups(), res))
