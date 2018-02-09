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
groupName = '291Д-08ИБ/16'
week = 8
day = '19.02.2018'
lesson = 3
get = {
    'GroupName': groupName,
    'Week': week
}
url = 'https://rasp.rea.ru/default?' + urlencode(get, quote_plus)
session = requests.Session()
response = session.get(url, headers=headers, cookies=cookies)
dom = BeautifulSoup(response.content, 'html.parser')
eventTarget = 'upModal'
eventArgument = str(groupName) + ':' + str(day) + ':' + str(lesson)
lastFocus = dom.find('input', {'name': '__LASTFOCUS'}).get('value')
viewState = dom.find('input', {'name': '__VIEWSTATE'}).get('value')
viewStateGenerator = dom.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
eventValidation = dom.find('input', {'name': '__EVENTVALIDATION'}).get('value')

data = {'__ASYNCPOST': 'true',
        '__EVENTARGUMENT': eventArgument,
        '__EVENTTARGET': eventTarget,
        '__EVENTVALIDATION': eventValidation,
        '__LASTFOCUS': lastFocus,
        '__VIEWSTATE': viewState,
        '__VIEWSTATEGENERATOR': viewStateGenerator,
        'ctl11': 'upModal|upModal',
        'ddlBachelor': 'na',
        'ddlCourse': 'na',
        'ddlFaculty': 'na',
        'ddlGroup': 'na',
        'txtGroupName': ''}

response = session.post(url, data=data, headers=headers)
print(response.text)
