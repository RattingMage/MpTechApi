from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from utils import check_zameny, find_str, refact_JSON

page = requests.get('https://mpt.ru/studentu/raspisanie-zanyatiy/')
html = BeautifulSoup(page.content, 'lxml')


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/groups/<speciality>')
def api_groups(speciality):
    groups = html.find_all("ul", role="tablist", class_='nav nav-tabs')
    if speciality ==  '09.02.01':
        group = groups[1].text.split('\n')
        for i in range(len(group)):
            try:
                group.remove('')
            except:
                pass
        return jsonify({"groups": group})
    if speciality ==  '09.02.06':
        group = groups[2].text.split('\n')
        for i in range(len(group)):
            try:
                group.remove('')
            except:
                pass
        return jsonify({"groups": group})
    if speciality ==  '09.02.07':
        group = groups[3].text.split('\n')
        for i in range(len(group)):
            try:
                group.remove('')
            except:
                pass
        return jsonify({"groups": group})
    if speciality == '10.02.03':
        group = groups[4].text.split('\n')
        for i in range(len(group)):
            try:
                group.remove('')
            except:
                pass
        return jsonify({"groups": group})
    if speciality == '10.02.05':
        group = groups[5].text.split('\n')
        for i in range(len(group)):
            try:
                group.remove('')
            except:
                pass
        return jsonify({"groups": group})
    if speciality == '40.02.01':
        group = groups[6].text.split('\n')
        for i in range(len(group)):
            try:
                group.remove('')
            except:
                pass
        return jsonify({"groups": group})
    if speciality == 'Popuski':
        group = groups[7].text.split('\n')
        for i in range(len(group)):
            try:
                group.remove('')
            except:
                pass
        return jsonify({"groups": group})


@app.route("/timetable/<groupname>")
def api_timetable(groupname):
    group = html.find("a", string=groupname)
    href = group.get('href')
    href = href[1::]
    div = html.find('div', id=href)
    tables = div.find_all('table')
    JSON = []
    for table in tables:
        tds = table.find_all('td')
        dct = {}
        dct2 = {}
        for i in range(len(tds)):
            if i == 0:
                dct['Number'] = tds[i].text
            if i == 1:
                dct['Subject'] = check_zameny(tds[i])
            if i == 2:
                dct['Teacher'] = check_zameny(tds[i])
                dct2['Info'] = find_str(table.find('h4').text.replace('\n', ''))
                dct2['Timetable'] = dct
                JSON.append(dct2)
                dct = {}
                dct2 = {}
            if i % 3 == 0:
                dct['Number'] = tds[i].text
            if i % 3 == 1:
                dct['Subject'] = check_zameny(tds[i])
            if i % 3 == 2 and i != 2:
                dct['Teacher'] = check_zameny(tds[i])
                dct2['Info'] = find_str(table.find('h4').text.replace('\n', ''))
                dct2['Timetable'] = dct
                JSON.append(dct2)
                dct = {}
                dct2 = {}
    return jsonify(refact_JSON(JSON))


@app.route("/week")
def api_week():
    week = ''
    try:
        week = html.find('span', class_='label label-info').text
    except:
        week = html.find('span', class_='label label-danger').text
    result = {
       'week': week
    }
    return jsonify(result)


@app.route("/replacement/<groupname>")
def api_replacement(groupname):
    page2 = requests.get('https://mpt.ru/studentu/izmeneniya-v-raspisanii/')
    html2 = BeautifulSoup(page2.content, 'lxml')

    all_b = html2.find_all('b')

    for b in all_b:
        if groupname == b.text:
            table = b.previous_element.previous_element.previous_element.previous_element

            return {
                "replace": {
                    'number': table.findNext('td', class_='lesson-number').text,
                    'from': table.findNext('td', class_='replace-from').text,
                    'to': table.findNext('td', class_='replace-to').text,
                    'updated-at': table.findNext('td', class_='updated-at').text
                }
            }
    return {
                "replace": "На этот день нет замен"
            }


if __name__ == '__main__':
    app.run()
