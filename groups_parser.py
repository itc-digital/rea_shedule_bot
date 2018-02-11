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

# GET запрос к главной странице
def get_main_page():
    response = session.get(url, headers=headers)
    dom = BeautifulSoup(response.content, 'html.parser')
    return dom

# GET запрос к странице расписания группы group на неделю week
def get_faculty_page(group, week):
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

# Получение значений скрытых полей ASP.NET после POST запроса
def last_focus_post(dom):
    start_array = dom.text.find('|0|hiddenField|__EVENTTARGET|')
    array = dom.text[start_array:].split('|')[1:]
    index = array.index('__LASTFOCUS') + 1
    return array[index]

def view_state_post(dom):
    start_array = dom.text.find('|0|hiddenField|__EVENTTARGET|')
    array = dom.text[start_array:].split('|')[1:]
    index = array.index('__VIEWSTATE') + 1
    return array[index]

def view_state_generator_post(dom):
    start_array = dom.text.find('|0|hiddenField|__EVENTTARGET|')
    array = dom.text[start_array:].split('|')[1:]
    index = array.index('__VIEWSTATEGENERATOR') + 1
    return array[index]

def event_validation_post(dom):
    start_array = dom.text.find('|0|hiddenField|__EVENTTARGET|')
    array = dom.text[start_array:].split('|')[1:]
    index = array.index('__EVENTVALIDATION') + 1
    return array[index]

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

# POST запрос на главную страницу
# data = {
#   '__EVENTVALIDATION': ?,
#   '__LASTFOCUS': ?,
#   '__VIEWSTATE': ?,
#   '__VIEWSTATEGENERATOR': ?,
#   'ddlFaculty': ?,
#   'ddlBachelor': 'na',
#   'ddlCourse': 'na',
#   'ddlGroup': 'na'
# }
#
# target = 'ddlFaculty' - для отправки факультетов
#   'ddlCourse' - для отправки курсов
#   'ddlBachelor' - для отправки уровней
#   'ddlGroup' - для отправки групп
def post_main_page(data, target):
    data_default = {
        '__ASYNCPOST': 'true',
        '__EVENTARGUMENT': '',
        '__EVENTTARGET': target,
        'ctl11': 'upSelectGroup|' + target,
        'txtGroupName': ''
    }
    data_default.update(data)
    response = session.post(url, data=data_default, headers=headers)
    dom = BeautifulSoup(response.content, 'html.parser')
    return dom

# Функция спрашивания факультета
def question_faculty():
    print('Введи номер твоего факультета:')
    for index, faculty in enumerate(faculty_question):
        print(index+1, ':', faculty)

    faculty_answer = int(input())-1     # Получаем ответ и проверяем
    if (faculty_answer<0) or (faculty_answer>10):
        return False
    else:
        return faculty_answer

# Функция справшивания курса
def question_course(course_dict):
    print('Введи номер твоего курса:')
    sorted_dict = sorted(course_dict.items(), key=lambda x: x[1])

    for course, index in sorted_dict:
        print(index, ':', course)

    
if __name__ == "__main__":
    dom = get_main_page()
    faculty_dict = parse_select(dom, 'ddlFaculty')
    faculty_answer = question_faculty()

    data = {
        '__EVENTVALIDATION': event_validation(dom),
        '__LASTFOCUS': last_focus(dom),
        '__VIEWSTATE': view_state(dom),
        '__VIEWSTATEGENERATOR': view_state_generator(dom),
        'ddlBachelor': 'na',
        'ddlCourse': 'na',
        'ddlFaculty': faculty_dict[faculty_mask[faculty_answer]],
        'ddlGroup': 'na',
    }

    dom = post_main_page(data, 'ddlFaculty')
    course_dict = parse_select(dom, 'ddlCourse')
    course_answer = question_course(course_dict)

'''
print(last_focus_post(dom))
print(view_state_post(dom))
print(view_state_generator_post(dom))
print(event_validation_post(dom))'''