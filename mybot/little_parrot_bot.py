#!/usr/bin/env python

import os
from telegram.ext import Updater

updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dispatcher = updater.dispatcher

def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="I'm a bot, please talk to me!"
    )

def bot_help(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="I will just reply to your messages"
    )


def echo(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=update.message.text
    )

from telegram.ext import CommandHandler, MessageHandler, Filters

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', bot_help))
dispatcher.add_handler(MessageHandler(Filters.text, echo))
updater.start_polling()
