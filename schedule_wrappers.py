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


def wrap_schedule_with_ascii_lines(schedule):
    wrapped_schedule = []
    for day in schedule:
        wrapped_day = """╔══ {0}
""".format(day)
        for class_ in schedule[day]:
            wrapped_class = """╠════════════════════
║► {0} ({1})
║  {2}
║  {3}
║  {4}
""".format(
                class_,
                schedule[day][class_]['time'],
                schedule[day][class_]['type'],
                schedule[day][class_]['title'],
                schedule[day][class_]['room']
            )
            wrapped_day += wrapped_class
        wrapped_day += """╚════════════════════"""
        wrapped_schedule.append(wrapped_day)
    return wrapped_schedule


def wrap_schedule_week(schedule):
    wrapped_schedule = []
    for day in schedule:
        wrapped_day = wrap_schedule_with_ascii_lines(day)
        wrapped_schedule.append(wrapped_day)
    return wrapped_schedule
