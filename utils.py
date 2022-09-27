import requests
from bs4 import BeautifulSoup

page = requests.get('https://mpt.ru/studentu/raspisanie-zanyatiy/')
html = BeautifulSoup(page.content, 'lxml')


def check_zameny(td):
    div = td.find('div')
    if div:
        week = ''
        try:
            week = html.find('span', class_='label label-info').text
        except:
            week = html.find('span', class_='label label-danger').text
        if week == 'Числитель':
            return td.find('div', class_='label label-danger').text.strip()
        else:
            return td.find('div', class_='label label-info').text.strip()
    else:
        return td.text


def find_str(stroka):
    if stroka.find('Нахимовский') != -1:
        i = stroka.find('Нахимовский')
        Day = stroka[:i]
        Place = stroka[i:]
        return {
                'day': Day,
                'place': Place
                }
    elif stroka.find('Нежинская') != -1:
        i = stroka.find('Нежинская')
        Day = stroka[:i]
        Place = stroka[i:]
        return {
                'day': Day,
                'place': Place
                }
    else:
        return "День не найден"


def refact_JSON(untimetable):
    timetable = []
    days = []
    dct = {}
    subjects = []
    dct['info'] = untimetable[0]['Info']
    days.append(untimetable[0]['Info']['day'])
    for day in untimetable:
        if day['Info']['day'] in days:
            subjects.append(day['Timetable'])
        else:
            dct['subjects'] = subjects
            timetable.append(dct)
            subjects = []
            dct = {}
            dct['info'] = day['Info']
            days.append(day['Info']['day'])
            subjects.append(day['Timetable'])
    dct2 = {
        'info': untimetable[len(untimetable)-1]['Info']
    }
    subjects2 = []
    for day in untimetable:
        if day['Info']['day'] == dct2['info']['day']:
            subjects2.append(day['Timetable'])
    dct2['subjects'] = subjects2
    timetable.append(dct2)

    return timetable


def parse_tname(tname):
    rtname = tname[::-1]
    count = 0
    rresult = ""
    for i in range(len(rtname)):
        if rtname[i] == ' ' and count == 1:
            for j in range(i):
                rresult += rtname[j]
        elif rtname[i] == ' ' and count != 1:
            count += 1
    print(rresult)
