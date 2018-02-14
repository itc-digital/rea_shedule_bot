from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import groups_parser

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

FACULTY, COURSE, BACHELOR, GROUP, FINISH_RECORDING = range(5)

USER = {}


def create_buttons_markup(options):
    buttons = []
    for option in options:
        buttons.append([InlineKeyboardButton(
            option,
            callback_data=options[option]
        ), ])
    reply_markup = InlineKeyboardMarkup(buttons)
    return reply_markup


def start(bot, update):
    global USER
    USER['chat_id'] = update.message.chat.id
    reply_keyboard = [['Boy', 'Girl', 'Other']]
    update.message.reply_text(
        'Привет! Сейчас мы попробуем понять в какой ты группе.'
        'Скажи, как мне к тебе обращаться?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return FACULTY


def help(bot, update):
    update.message.reply_text('Help!')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')
    return ConversationHandler.END


def get_faculty(bot, update):
    global USER
    USER['name'] = update.message.text
    dom = groups_parser.get_main_page()
    faculty_dict = groups_parser.parse_select(dom, 'ddlFaculty')
    reply_markup = create_buttons_markup(faculty_dict)
    reply_text = 'Выбери факультет, на котором ты учишься:'
    update.message.reply_text(reply_text, reply_markup=reply_markup)
    return COURSE


def get_course(bot, update):
    query = update.callback_query
    global USER
    USER['faculty_id'] = query.data
    course_dict = groups_parser.parse_options(
        faculty=USER['faculty_id'],
    )
    reply_markup = create_buttons_markup(course_dict)
    reply_text = 'Теперь выбери на каком ты курсе:'
    bot.edit_message_text(
        text=reply_text,
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )
    return BACHELOR


def get_bachelor(bot, update):
    query = update.callback_query
    global USER
    USER['course_id'] = query.data
    bachelor_dict = groups_parser.parse_options(
        faculty=USER['faculty_id'],
        course=USER['course_id']
    )
    reply_markup = create_buttons_markup(bachelor_dict)
    reply_text = 'Теперь выбери тип обучения:'
    bot.edit_message_text(
        text=reply_text,
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )
    return GROUP


def get_group(bot, update):
    query = update.callback_query
    global USER
    USER['bachelor_id'] = query.data
    groups_dict = groups_parser.parse_options(
        faculty=USER['faculty_id'],
        course=USER['course_id'],
        bachelor=USER['bachelor_id'],
    )
    reply_markup = create_buttons_markup(groups_dict)
    reply_text = 'И наконец из какой ты группы?..'
    bot.edit_message_text(
        text=reply_text,
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )
    return FINISH_RECORDING


def finish_recording_user(bot, update):
    query = update.callback_query
    global USER
    USER['course_id'] = query.data
    return


if __name__ == '__main__':
    token = ''
    updater = Updater(token)
    dispatcher = updater.dispatcher
    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FACULTY: [MessageHandler(Filters.text, get_faculty)],
            COURSE: [CallbackQueryHandler(get_course)],
            BACHELOR: [CallbackQueryHandler(get_bachelor)],
            GROUP: [CallbackQueryHandler(get_group)],
            FINISH_RECORDING: [CallbackQueryHandler(finish_recording_user)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True,
    )

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()
