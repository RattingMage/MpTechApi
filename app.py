import requests
from flask import Flask, jsonify, request
from flask_restx import Api, Namespace, Resource
from bs4 import BeautifulSoup
from utils import check_zameny_sub, check_zameny_tech, find_str, refact_JSON

page = requests.get('https://mpt.ru/studentu/raspisanie-zanyatiy/')
html = BeautifulSoup(page.content, 'lxml')

app = Flask(__name__)
api = Api(app)

specialities_ns = Namespace('specialities')
groups_ns = Namespace('groups')
timetable_ns = Namespace('timetable')
week_ns = Namespace('week')
replacement_ns = Namespace('replacement')
api.add_namespace(specialities_ns)
api.add_namespace(groups_ns)
api.add_namespace(timetable_ns)
api.add_namespace(week_ns)
api.add_namespace(replacement_ns)


@specialities_ns.route('/')
class SpecialitiesView(Resource):
    def get(self):
        s_specialities = html.find_all("ul", role="tablist", class_='nav nav-tabs')
        specialities = s_specialities[0].text.split('\n')
        for i in range(len(specialities)):
            try:
                if specialities[i] == '':
                    specialities.pop(i)
            except:
                pass
        return {
            "specialities": specialities
        }


@groups_ns.route('/<speciality>')
class GroupsView(Resource):
    def get(self, speciality):
        if speciality == "popuski":
            speciality = "Отделение первого курса"
        response = []
        specs = html.find_all("li", role="presentation")
        actual_href = []
        for i in specs:
            if speciality == i.text:
                a = i.find_next("a")
                actual_href = a.get("href").replace("#", "")
        actual_div = html.find("div", id=actual_href)
        ul = actual_div.find_next("ul")
        all_li = ul.children
        for li in all_li:
            response.append(li.next_element.text.replace("\n", ""))
        for i in response:
            try:
                response.remove("")
            except:
                pass
        return {
            "groups": response
        }


@timetable_ns.route("/")
class TimetableViews(Resource):
    def get(self):
        groupname = request.args.get("groupname")
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
                    dct['number'] = tds[i].text
                if i == 1:
                    dct['subject'] = check_zameny_sub(tds[i])
                if i == 2:
                    dct['teacher'] = check_zameny_tech(tds[i])
                    dct2['info'] = find_str(table.find('h4').text.replace('\n', ''))
                    dct2['timetable'] = dct
                    JSON.append(dct2)
                    dct = {}
                    dct2 = {}
                if i % 3 == 0:
                    dct['number'] = tds[i].text
                if i % 3 == 1:
                    dct['subject'] = check_zameny_sub(tds[i])
                if i % 3 == 2 and i != 2:
                    dct['teacher'] = check_zameny_tech(tds[i])
                    dct2['info'] = find_str(table.find('h4').text.replace('\n', ''))
                    dct2['timetable'] = dct
                    JSON.append(dct2)
                    dct = {}
                    dct2 = {}
        return jsonify(refact_JSON(JSON))


@week_ns.route("/")
class WeekView(Resource):
    def get(self):
        week = ''
        try:
            week = html.find('span', class_='label label-info').text
        except:
            week = html.find('span', class_='label label-danger').text
        result = {
            'week': week
        }
        return jsonify(result)


@replacement_ns.route("/<groupname>")
class ReplacementView(Resource):
    def get(self, groupname):
        page2 = requests.get('https://mpt.ru/studentu/izmeneniya-v-raspisanii/')
        html2 = BeautifulSoup(page2.content, 'lxml')

        all_b = html2.find_all('b')

        response = []

        for b in all_b:
            if groupname == b.text:
                table = b.previous_element.previous_element.previous_element.previous_element

                trs = table.findNext('th', class_='lesson-number').previous_element.previous_element.next_siblings
                for tr in trs:
                    if tr.text != '\n':
                        response.append({
                            'lessonNumber': tr.findNext('td', class_='lesson-number').text,
                            'from': tr.findNext('td', class_='replace-from').text,
                            'to': tr.findNext('td', class_='replace-to').text,
                            'updatedAt': tr.findNext('td', class_='updated-at').text
                        })

        if response is None:
            return {
                "replace": "На этот день нет замен"
            }
        else:
            return {
                "replace": response
            }


if __name__ == '__main__':
    app.run()
