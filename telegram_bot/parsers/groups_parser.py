import requests
from bs4 import BeautifulSoup

HEADERS = {
    'Host': 'rasp.rea.ru',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    'X-MicrosoftAjax': 'Delta=true',
    'X-Requested-With': 'XMLHttpRequest',
    'Cache-Control': 'no-cache',
    'Referer': 'https://rasp.rea.ru/'
}

URL = 'https://rasp.rea.ru/default'

ASP_KEYS_TITLES = [
    '__EVENTVALIDATION',
    '__LASTFOCUS',
    '__VIEWSTATE',
    '__VIEWSTATEGENERATOR',
]

session = requests.Session()  # Set session


# GET запрос к главной странице
def get_main_page():
    response = session.get(URL, headers=HEADERS)
    dom = BeautifulSoup(response.content, 'html.parser')
    return dom


def get_asp_keys(dom, method):
    asp_keys = {}
    if method == 'get':
        for asp_key_title in ASP_KEYS_TITLES:
            asp_keys[asp_key_title] = dom.find(
                'input', {'name': asp_key_title}
            ).get('value')
        return asp_keys
    if method == 'post':
        start_index = dom.text.find('0|hiddenField|__EVENTTARGET|')
        array_with_keys = dom.text[start_index:].split('|')
        for asp_key_title in ASP_KEYS_TITLES:
            index_of_key = array_with_keys.index(asp_key_title) + 1
            asp_keys[asp_key_title] = array_with_keys[index_of_key]
        return asp_keys
    return


def parse_select(dom, select_name):
    options = dom.find('select', {'name': select_name}).find_all('option')[1:]
    options_dict = {}
    for option in options:
        options_dict.update({option.text: option.get('value')})
    return options_dict


def post_main_page(data, target):
    data_default = {
        '__ASYNCPOST': 'true',
        '__EVENTARGUMENT': '',
        '__EVENTTARGET': target,
        'ctl11': 'upSelectGroup|' + target,
        'txtGroupName': ''
    }
    data_default.update(data)
    response = session.post(URL, data=data_default, headers=HEADERS)
    dom = BeautifulSoup(response.content, 'html.parser')
    return dom


def parse_options_and_keys(faculty='na', course='na', bachelor='na', asp_keys=None):
    first_action, second_action = action_decoder(faculty, course, bachelor)
    if not asp_keys:
        dom = get_main_page()
        options_dict = parse_select(dom, second_action)
        asp_keys = get_asp_keys(dom, 'get')
        return options_dict, asp_keys
    data = {
        'ddlBachelor': bachelor,
        'ddlCourse': course,
        'ddlFaculty': faculty,
        'ddlGroup': 'na',
    }
    data.update(asp_keys)
    dom = post_main_page(data, first_action)
    asp_keys = get_asp_keys(dom, 'post')
    options_dict = parse_select(dom, second_action)
    return options_dict, asp_keys


def action_decoder(faculty='na', course='na', bachelor='na'):
    if bachelor != 'na':
        return 'ddlBachelor', 'ddlGroup'
    if course != 'na':
        return 'ddlCourse', 'ddlBachelor'
    if faculty != 'na':
        return 'ddlFaculty', 'ddlCourse'
    return None, 'ddlFaculty'
