import requests
from bs4 import BeautifulSoup

REA_HREF = 'https://rasp.rea.ru/default'


def parse_day(rows):
    day_title = rows[0].findAll("td")[1].font.b.contents[0]
    serialized_day = {}
    for day in rows[1:]:
        day_data = day.findAll("td")
        class_number = day_data[0].span.contents[0]
        class_data = None
        if day_data[1].a:
            class_data = day_data[1].a.span.contents[0]
        serialized_day[class_number] = class_data
    return day_title, serialized_day


def parse_shedule(group, week):
    shedule_href = '{0}?GroupName={1}&Week={2}'.format(REA_HREF, group, week)
    shedule_page = requests.get(shedule_href).text
    soup = BeautifulSoup(shedule_page, 'html.parser')
    shedule_table = soup.find(id="ttWeek_tblTime").findAll("tr")
    serialized_week = {}
    for day_number in range(6):
        current_day = shedule_table[day_number * 9:day_number * 9 + 9]
        day_title, serialized_day = parse_day(current_day)
        serialized_week[day_title] = serialized_day
    return serialized_week
