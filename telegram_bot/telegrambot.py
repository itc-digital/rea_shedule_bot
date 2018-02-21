from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)
from django_telegrambot.apps import DjangoTelegramBot

import logging

import states_chain


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

FACULTY, COURSE, BACHELOR, GROUP, FINISH_RECORDING, DEFAULT = range(6)


def help(bot, update):
    update.message.reply_text('Help!')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


if __name__ == '__main__':
    dispatcher = DjangoTelegramBot.dispatcher
    states_handler = ConversationHandler(
        entry_points=[CommandHandler('start', states_chain.get_faculty)],
        states={
            COURSE: [CallbackQueryHandler(states_chain.get_course)],
            BACHELOR: [CallbackQueryHandler(states_chain.get_bachelor)],
            GROUP: [CallbackQueryHandler(states_chain.get_group)],
            FINISH_RECORDING: [CallbackQueryHandler(states_chain.finish_recording_user)],
            DEFAULT: [MessageHandler(Filters.text, states_chain.default)],
        },
        allow_reentry=True
    )
    dispatcher.add_handler(states_handler)
    dispatcher.add_handler(
        MessageHandler(
            Filters.text,
            states_chain.default
        )
    )
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_error_handler(error)
