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
