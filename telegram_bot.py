from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import groups_parser

import json
import os


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

FACULTY, COURSE, BACHELOR, GROUP, FINISH_RECORDING = range(5)

PATH = 'db.json'


def load_data(path):
    if not os.path.exists(path):
        return None
    with open(path, mode='r', encoding='utf-8') as infile:
        read_data = json.load(infile)
        return read_data


def write_data(path, data):
    if not os.path.exists(path):
        return None
    with open(path, mode='w', encoding='utf-8') as outfile:
        json.dump(data, outfile)


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
    reply_keyboard = [['Boy', 'Girl', 'Other']]
    update.message.reply_text(
        'Привет! Сейчас мы попробуем понять в какой ты группе.'
        'Скажи, как мне к тебе обращаться?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return FACULTY


def get_faculty(bot, update):
    global PATH
    chat_id = update.message.chat.id
    name = update.message.text
    data = load_data(PATH)
    user = {}
    course_dict, asp_keys = groups_parser.parse_options_and_keys()
    user['name'] = name
    user['keys'] = asp_keys
    data[str(chat_id)] = user
    write_data(PATH, data)
    reply_markup = create_buttons_markup(course_dict)
    reply_text = 'Выбери факультет, на котором ты учишься:'
    update.message.reply_text(reply_text, reply_markup=reply_markup)
    return COURSE


def get_course(bot, update):
    global PATH
    query = update.callback_query
    chat_id = query.message.chat_id
    faculty_id = query.data
    data = load_data(PATH)
    user = data[str(chat_id)]
    asp_keys = user['keys']
    course_dict, asp_keys = groups_parser.parse_options_and_keys(
        faculty=faculty_id,
        asp_keys=asp_keys
    )
    user['faculty_id'] = faculty_id
    user['keys'] = asp_keys
    data[str(chat_id)] = user
    write_data(PATH, data)
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
    global PATH
    query = update.callback_query
    chat_id = query.message.chat_id
    course_id = query.data
    data = load_data(PATH)
    user = data[str(chat_id)]
    asp_keys = user['keys']
    bachelor_dict, asp_keys = groups_parser.parse_options_and_keys(
        faculty=user['faculty_id'],
        course=course_id,
        asp_keys=asp_keys
    )
    user['course_id'] = course_id
    user['keys'] = asp_keys
    data[str(chat_id)] = user
    write_data(PATH, data)
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
    global PATH
    query = update.callback_query
    chat_id = query.message.chat_id
    bachelor_id = query.data
    data = load_data(PATH)
    user = data[str(chat_id)]
    asp_keys = user['keys']
    groups_dict, asp_keys = groups_parser.parse_options_and_keys(
        faculty=user['faculty_id'],
        course=user['course_id'],
        bachelor=bachelor_id,
        asp_keys=asp_keys
    )
    buttons = []
    for option in groups_dict:
        buttons.append([InlineKeyboardButton(
            option,
            callback_data=option
        ), ])
    reply_markup = InlineKeyboardMarkup(buttons)
    reply_text = 'И наконец из какой ты группы?..'
    bot.edit_message_text(
        text=reply_text,
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )
    return FINISH_RECORDING


def finish_recording_user(bot, update):
    global PATH
    query = update.callback_query
    chat_id = query.message.chat_id
    group_title = query.data
    data = load_data(PATH)
    user = data[str(chat_id)]
    user['group_title'] = group_title
    data[str(chat_id)] = user
    write_data(PATH, data)
    reply_text = 'Хорошо, я тебя запомнил!'
    bot.edit_message_text(
        text=reply_text,
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
    )
    return


def help(bot, update):
    update.message.reply_text('Help!')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')
    return ConversationHandler.END


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