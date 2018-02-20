from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

import schedule_wrappers

from telegram_bot import COURSE, BACHELOR, GROUP, FINISH_RECORDING, DEFAULT

from parsers import groups_parser
from parsers import shedule_parser

import datetime


def send_default_markup(bot, chat_id, reply_text):
    default_reply_keyboard = [
        ['Пары сегодня', 'Пары завтра'],
        ['Расписание на эту неделю', 'Расписание на следущую неделю'],
        ['пн', 'вт', 'ср', 'чт', 'пт', 'сб'],
    ]
    default_markup = ReplyKeyboardMarkup(default_reply_keyboard)
    bot.send_message(
        chat_id=chat_id,
        text=reply_text,
        reply_markup=default_markup
    )
    return


def get_current_week():
    now = datetime.datetime.now()
    timetuple = now.timetuple()
    days_this_year = timetuple.tm_yday - 1
    current_week = (days_this_year // 7) + 1
    return current_week


def get_current_day_of_the_week():
    now = datetime.datetime.now()
    timetuple = now.timetuple()
    current_day_of_the_week = timetuple.tm_wday
    return current_day_of_the_week


def get_wrapped_schedule_considering_choise(group_title, choise):
    current_week = get_current_week()
    current_day_of_the_week = get_current_day_of_the_week()
    schedule = []
    if choise == 'Пары сегодня':
        schedule = shedule_parser.parse_schedule(
            group_title,
            current_week
        )[current_day_of_the_week % 7]
        wrapped_schedule = [schedule_wrappers.wrap_schedule_with_ascii_lines(schedule)]
    if choise == 'Пары завтра':
        schedule = shedule_parser.parse_schedule(
            group_title,
            current_week
        )[(current_day_of_the_week + 1) % 7]
        wrapped_schedule = [schedule_wrappers.wrap_schedule_with_ascii_lines(schedule)]
    if choise == 'Расписание на эту неделю':
        schedule = shedule_parser.parse_schedule(
            group_title,
            current_week
        )
        wrapped_schedule = schedule_wrappers.wrap_schedule_week(schedule)
    if choise == 'Расписание на следущую неделю':
        schedule = shedule_parser.parse_schedule(
            group_title,
            current_week + 1
        )
        wrapped_schedule = schedule_wrappers.wrap_schedule_week(schedule)
    if choise == 'пн':
        schedule = shedule_parser.parse_schedule(
            group_title,
            current_week
        )[0]
        wrapped_schedule = [schedule_wrappers.wrap_schedule_with_ascii_lines(schedule)]
    if choise == 'вт':
        schedule = shedule_parser.parse_schedule(
            group_title,
            current_week
        )[1]
        wrapped_schedule = [schedule_wrappers.wrap_schedule_with_ascii_lines(schedule)]
    if choise == 'ср':
        schedule = shedule_parser.parse_schedule(
            group_title,
            current_week
        )[2]
        wrapped_schedule = [schedule_wrappers.wrap_schedule_with_ascii_lines(schedule)]
    if choise == 'чт':
        schedule = shedule_parser.parse_schedule(
            group_title,
            current_week
        )[3]
        wrapped_schedule = [schedule_wrappers.wrap_schedule_with_ascii_lines(schedule)]
    if choise == 'пт':
        schedule = shedule_parser.parse_schedule(
            group_title,
            current_week
        )[4]
        wrapped_schedule = [schedule_wrappers.wrap_schedule_with_ascii_lines(schedule)]
    if choise == 'сб':
        schedule = shedule_parser.parse_schedule(
            group_title,
            current_week
        )[5]
        wrapped_schedule = [schedule_wrappers.wrap_schedule_with_ascii_lines(schedule)]
    return wrapped_schedule or None


def get_faculty(bot, update):

    course_dict, asp_keys = groups_parser.parse_options_and_keys()

    reply_markup = schedule_wrappers.create_buttons_markup(course_dict)
    reply_text = 'Выбери факультет, на котором ты учишься:'
    update.message.reply_text(
        reply_text,
        reply_markup=reply_markup
    )
    return COURSE


def get_course(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    faculty_id = query.data

    course_dict, asp_keys = groups_parser.parse_options_and_keys(
        faculty=faculty_id,
        asp_keys=asp_keys
    )

    reply_markup = schedule_wrappers.create_buttons_markup(course_dict)
    reply_text = 'Теперь выбери на каком ты курсе:'
    bot.edit_message_text(
        text=reply_text,
        chat_id=chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )
    return BACHELOR


def get_bachelor(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    course_id = query.data

    bachelor_dict, asp_keys = groups_parser.parse_options_and_keys(
        faculty=user['faculty_id'],
        course=course_id,
        asp_keys=asp_keys
    )

    reply_markup = schedule_wrappers.create_buttons_markup(bachelor_dict)
    reply_text = 'Теперь выбери тип обучения:'
    bot.edit_message_text(
        text=reply_text,
        chat_id=chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )
    return GROUP


def get_group(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    bachelor_id = query.data

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
        chat_id=chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )
    return FINISH_RECORDING


def finish_recording_user(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    group_title = query.data

    reply_text = 'Хорошо, я тебя запомнил! Ты из {}'.format((group_title),)

    bot.delete_message(
        chat_id=chat_id,
        message_id=query.message.message_id
    )
    send_default_markup(bot, chat_id, reply_text)
    return DEFAULT


def default(bot, update):
    chat_id = update.message.chat_id
    choise = update.message.text

    wrapped_schedule = get_wrapped_schedule_considering_choise(group_title, choise)
    if not wrapped_schedule:
        reply_text = 'Прости, я тебя не понял... Попробуй воспользоваться кнопками меню?'
        send_default_markup(bot, chat_id, reply_text)
        return DEFAULT
    for wrapped_day in wrapped_schedule:
            bot.send_message(
                chat_id=chat_id,
                text=wrapped_day[0],
            )
    reply_text = 'Чем еще я могу помочь?'
    send_default_markup(bot, chat_id, reply_text)
    return DEFAULT
