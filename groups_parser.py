import requests
from urllib.parse import urlencode, quote_plus
from bs4 import BeautifulSoup

headers = {
    'Host': 'rasp.rea.ru',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'X-MicrosoftAjax': 'Delta=true',
    'X-Requested-With': 'XMLHttpRequest',
    'Cache-Control': 'no-cache',
    'Referer': 'https://rasp.rea.ru/'
}
url = 'https://rasp.rea.ru/default'
faculty_mask = [
    'факультет "Международная школа бизнеса и мировой экономики"',
    'факультет "Экономики и права"',
    'факультет гостинично-ресторанной, туристической и спортивной индустрии',
    'факультет маркетинга',
    'факультет математической экономики, статистики и информатики',
    'факультет менеджмента',
    'факультет экономики торговли и товароведения',
    'финансовый факультет',
    'факультет дистанционного обучения',
    'факультет "Плехановская школа бизнеса Integral"',
    'факультет бизнеса "КАПИТАНЫ"'
]
faculty_question = [
    'МШБиМЭ',
    'ФЭП',
    'ГРТСИ',
    'ФМа',
    'ФМЭСИ',
    'ФМе',
    'ФЭТТ',
    'ФФ',
    'Факультет дистанционного обучения',
    'Плехановская школа бизнеса Integral',
    'Факультет бизнеса "КАПИТАНЫ"'
]

session = requests.Session() # Set session

# GET запросы к главной странице
def get_main_page(session, headers):
    response = session.get(url, headers=headers)
    dom = BeautifulSoup(response.content, 'html.parser')
    return dom

# GET запрос к странице расписания группы group на неделю week
def get_faculty_page(session, headers, group, week):
    get = {
        'GroupName': group,
        'Week': week
    }
    response = session.get(url+'?'+urlencode(get, quote_plus), headers=headers)
    dom = BeautifulSoup(response.content, 'html.parser')
    return dom

# Получение значений скрытых полей ASP.NET после GET запроса
def last_focus(dom):
    return dom.find('input', {'name': '__LASTFOCUS'}).get('value')

def view_state(dom):
    return dom.find('input', {'name': '__VIEWSTATE'}).get('value')

def view_state_generator(dom):
    return dom.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')

def event_validation(dom):
    return dom.find('input', {'name': '__EVENTVALIDATION'}).get('value')

# Создание словаря из:
# Факультетов - 'ddlFaculty'
# Курсов - 'ddlCourse'
# Уровней - 'ddlBachelor'
# Групп - 'ddlGroup'
def parse_select(dom, select_name):
    options = dom.find('select', {'name': select_name}).find_all('option')[1:]
    options_dict = {}
    for option in options:
        options_dict.update({option.text: option.get('value')})
    return options_dict

dom = get_main_page(session, headers)
faculty_dict = parse_select(dom, 'ddlFaculty')
print('Введи номер твоего факультета:')
for index, faculty in enumerate(faculty_question):
    print(index+1, ':', faculty)

faculty_answer = int(input())-1
if (faculty_answer<0) or (faculty_answer>10):
    print('Пошёл на хуй')
    exit()

data = {
    '__ASYNCPOST': 'true',
    '__EVENTARGUMENT': '',
    '__EVENTTARGET': 'ddlFaculty',
    '__EVENTVALIDATION': event_validation(dom),
    '__LASTFOCUS': last_focus(dom),
    '__VIEWSTATE': view_state(dom),
    '__VIEWSTATEGENERATOR': view_state_generator(dom),
    'ctl11': 'upSelectGroup|ddlFaculty',
    'ddlBachelor': 'na',
    'ddlCourse': 'na',
    'ddlFaculty': faculty_dict[faculty_mask[faculty_answer]],
    'ddlGroup': 'na',
    'txtGroupName': ''
}
response = session.post(url, data=data, headers=headers)
print(response.text)

'''
import requests
from urllib.parse import urlencode, quote_plus
from bs4 import BeautifulSoup

headers = {
    'Host': 'rasp.rea.ru',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'X-MicrosoftAjax': 'Delta=true',
    'X-Requested-With': 'XMLHttpRequest',
    'Cache-Control': 'no-cache',
    'Referer': 'https://rasp.rea.ru/'
}
cookies = {
    '_ym_uid': '0',
    '_ga': '0',
    'ASP.NET_SessionId': '0'
}

url = 'https://rasp.rea.ru/default?' + urlencode('', quote_plus)
session = requests.Session()
response = session.get(url, headers=headers, cookies=cookies)
dom = BeautifulSoup(response.content, 'html.parser')
lastFocus = dom.find('input', {'name': '__LASTFOCUS'}).get('value')
viewState = dom.find('input', {'name': '__VIEWSTATE'}).get('value')
viewStateGenerator = dom.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
eventValidation = dom.find('input', {'name': '__EVENTVALIDATION'}).get('value')

data = {'__ASYNCPOST': 'true',
        '__EVENTARGUMENT': '',
        '__EVENTTARGET': 'ddlFaculty',
        '__EVENTVALIDATION': eventValidation,
        '__LASTFOCUS': lastFocus,
        '__VIEWSTATE': viewState,
        '__VIEWSTATEGENERATOR': viewStateGenerator,
        'ctl11': 'upSelectGroup|ddlFaculty',
        'ddlBachelor': 'na',
        'ddlCourse': 'na',
        'ddlFaculty': '4737',
        'ddlGroup': 'na',
        'txtGroupName': ''}

response = session.post(url, data=data, headers=headers)
print(response.text)
'''