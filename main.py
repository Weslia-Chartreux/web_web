import os

from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from requests import request
from flask import request as re
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from random import choice


def okr(name):
    response = request(
        method='GET',
        url='http://geocode-maps.yandex.ru/1.x/',
        params={
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
            'geocode': name,
            'format': 'json',
        }
    )
    if response.status_code == 200:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"].replace(' ', ',')
        response = request(
            method='GET',
            url='http://static-maps.yandex.ru/1.x/',
            params={
                'll': toponym_coodrinates,
                'l': 'sat',
                'z': 8
            }
        )
        map_file = "static/img/1.png"
        with open(map_file, "wb") as file:
            file.write(response.content)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
otv = ""
city = ['Москва', 'Казань', 'Саратов']


@app.route('/', methods=['GET', 'POST'])
def reg():
    global c
    if re.method == 'GET':
        c = choice(city)
        okr(c)
        print(c)
        return render_template('main.html', img=url_for("static", filename="img/1.png"))
    elif re.method == 'POST':
        if c == re.form['email']:
            return "Правильно"
        return "Неправильно"


if __name__ == '__main__':
    app.run(debug=True)
