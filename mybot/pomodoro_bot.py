#!/usr/bin/env python

import os
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters


def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hi! I set alarms"
    )

def bot_help(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="""
            Use /set s to set an alarm in s seconds.
            Use /unset to unset the alarm.
        """
    )

def alarm(bot, job):
    message = 'Beep!'
    if len(job.context['message']) > 0:
        message = job.context['message']
    bot.send_message(job.context['chat_id'], text=message)

def set_timer(bot, update, args, job_queue, chat_data):
    chat_id = update.message.chat_id
    logger.info(args)
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        message = ' '.join(args[1:]) if len(args) > 1 else ''
        if due < 0:
            update.message.reply_text(
                'Sorry we can not go back to future!'
            )
            return
        job = job_queue.run_once(alarm, due, context={
        'chat_id': chat_id,
        'message': message,
        })
        chat_data['job'] = job
        update.message.reply_text('Timer successfully set!')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set seconds')


def unset_timer(bot, update, chat_data):
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return
    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']
    update.message.reply_text('Timer successfully unset!')

def error(bot, update, error):
    logger.warning(
        'Update "%s" caused error "%s"',
        update,
        error,
    )


logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.INFO
)
logger = logging.getLogger(__name__)

updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', bot_help))
dispatcher.add_handler(CommandHandler(
    'set',
    set_timer,
    pass_args=True,
    pass_job_queue=True,
    pass_chat_data=True,
))
dispatcher.add_handler(CommandHandler(
    'unset',
    unset_timer,
    pass_chat_data=True,
))
dispatcher.add_error_handler(error)
updater.start_polling()
