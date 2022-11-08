import requests
from bs4 import BeautifulSoup

page = requests.get('https://mpt.ru/studentu/raspisanie-zanyatiy/')
html = BeautifulSoup(page.content, 'lxml')


def check_zameny_sub(td):
    div = td.find('div')
    if div:
        try:
            week = html.find('span', class_='label label-info').text
        except:
            week = html.find('span', class_='label label-danger').text
        if week == 'Числитель':
            return {
                "week": week,
                "sub": td.find('div', class_='label label-danger').text.strip()
            }
        else:
            return {
                "week": week,
                "sub": td.find('div', class_='label label-info').text.strip()
            }
    else:
        return {
            "week": None,
            "sub": td.text
        }


def check_zameny_tech(td):
    div = td.find('div')
    if div:
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
    dct['info'] = untimetable[0]['info']
    days.append(untimetable[0]['info']['day'])
    for day in untimetable:
        if day['info']['day'] in days:
            subjects.append(day['timetable'])
        else:
            dct['subjects'] = subjects
            timetable.append(dct)
            subjects = []
            dct = {}
            dct['info'] = day['info']
            days.append(day['info']['day'])
            subjects.append(day['timetable'])
    dct2 = {
        'info': untimetable[len(untimetable) - 1]['info']
    }
    subjects2 = []
    for day in untimetable:
        if day['info']['day'] == dct2['info']['day']:
            subjects2.append(day['timetable'])
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
