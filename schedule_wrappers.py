from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def create_schedule_markups(schedule):
    markups = []
    for day in schedule:
        buttons = []
        buttons.append([InlineKeyboardButton(
            day,
            callback_data='#'
        ), ])
        for lesson in schedule[day]:
            lesson_markup_text = schedule[day][lesson] or '---'
            buttons.append([
                InlineKeyboardButton(
                    lesson,
                    callback_data='#'),
                InlineKeyboardButton(
                    lesson_markup_text,
                    callback_data='#'),
            ])
        markup = InlineKeyboardMarkup(buttons)
        markups.append(markup)
    return markups
