import requests
from bs4 import BeautifulSoup

REA_HREF = 'https://rasp.rea.ru/default'


def serialize_day(rows):
    day_title = rows[0].findAll("td")[1].font.b.contents[0]
    serialized_day = {}
    for class_ in rows[1:]:
        class_data = class_.findAll("td")
        class_number = class_data[0].span.contents[0]
        if not class_data[1].a:
            continue
        class_title = class_data[1].a.span.contents[0]
        class_type = class_data[1].a.span.contents[2][1:]
        class_room = class_data[1].a.span.contents[4]
        serialized_class = {}
        serialized_class['title'] = class_title
        serialized_class['type'] = class_type
        serialized_class['room'] = class_room
        serialized_day[class_number] = serialized_class
    return day_title, serialized_day


def parse_shedule(group, week):
    shedule_href = '{0}?GroupName={1}&Week={2}'.format(REA_HREF, group, week)
    shedule_page = requests.get(shedule_href).text
    soup = BeautifulSoup(shedule_page, 'html.parser')
    shedule_table = soup.find(id="ttWeek_tblTime").findAll("tr")
    serialized_week = {}
    for day_number in range(6):
        current_day = shedule_table[day_number * 9:day_number * 9 + 9]
        day_title, serialized_day = serialize_day(current_day)
        serialized_week[day_title] = serialized_day
    return serialized_week
