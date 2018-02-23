from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

import logging
import os

from . import states_chain


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


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')
    return ConversationHandler.END


def main():
    token = os.environ['TOKEN']
    port = int(os.environ.get('PORT', '8443'))
    appname = os.environ['APPNAME']
    updater = Updater(token)
    updater.start_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=token
    )
    updater.bot.set_webhook("https://{0}.herokuapp.com/{1}".format(appname, token))
    dispatcher = updater.dispatcher
    states_handler = ConversationHandler(
        entry_points=[CommandHandler('start', states_chain.get_faculty)],
        states={
            COURSE: [CallbackQueryHandler(states_chain.get_course)],
            BACHELOR: [CallbackQueryHandler(states_chain.get_bachelor)],
            GROUP: [CallbackQueryHandler(states_chain.get_group)],
            FINISH_RECORDING: [CallbackQueryHandler(states_chain.finish_recording_user)],
            DEFAULT: [MessageHandler(Filters.text, states_chain.default)],
        },
        allow_reentry=True,
        fallbacks=[CommandHandler('cancel', cancel)],
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
    updater.start_polling()
    updater.idle()
