# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask, request
import json
import pickle
from global_handler import GlobalHandler

app = Flask(__name__)

sessionStorage = {}

session_path = './sessions/'


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

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Собрать тариф",
                "Пополнить счет",
                "Все что вы хотите!",
            ],
            'current_flow': None
        }

        res['response']['text'] = 'Привет! Я твой новый помощник в мире МТС! Чтобы мы могли свободно общаться, ' \
                                  'я должен знать что ты это ты. Для этого введи свой номер телефона)'
        with open(session_path + session_id + '.pickle', 'wb') as f:
            pickle.dump(sessionStorage, f)

        return

    # Обрабатываем ответ пользователя.
    handler = GlobalHandler(session_id)
    handler.handle_request(req['request'], res)


if __name__ == "__main__":
    app.run(host='0.0.0.0')