# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask, request
import json

app = Flask(__name__)

sessionStorage = {}


@app.route('/', methods=['POST'])
def hello_world():

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    session_id = req['session']['session_id']
    print(session_id)

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Собрать тариф",
                "Пополнить счет",
                "Все что вы хотите!",
            ]
        }

        res['response']['text'] = 'Привет! Я твой новый помощник в мире МТС! Чтобы мы могли свободно общаться, ' \
                                  'я должен знать что ты это ты. Для этого введи свой номер телефона)'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
    ]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    # session['suggests'] = session['suggests'][1:]
    # sessionStorage[user_id] = session

    return suggests


if __name__ == "__main__":
    app.run(host='0.0.0.0')