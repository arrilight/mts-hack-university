# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask, request
import json
import pickle
import plan_builder

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

    with open(session_path + session_id + '.pickle', 'rb') as f:
        sessionStorage1 = pickle.load(f)
        result = {}

        if req['request']['original_utterance'].lower() in ['собрать тариф']:
            pb = plan_builder.PlanBuilder()
            result = pb.process_step()
            sessionStorage1['current_flow'] = 'build_plan'

        # if sessionStorage1['current_flow'] is None:
        #     pb = plan_builder.PlanBuilder()
        #     result = pb.process_step()
        #     sessionStorage1['current_flow'] = 'build_plan'

        elif 'current_flow' in sessionStorage1.keys():
            state = sessionStorage1['flow_step']
            pb = plan_builder.PlanBuilder(state)
            result = pb.process_step(req['request'])

        res['response']['text'] = result['title']
        res['response']['buttons'] = get_suggests(result['suggests'])
        result['init'] = result['newstate']
        sessionStorage1['flow_step'] = result

        with open(session_path + session_id + '.pickle', 'wb') as f:
            pickle.dump(sessionStorage1, f)

        return


def get_suggests(session_raw):

    if session_raw is None:
        return None

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session_raw
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    # session['suggests'] = session['suggests'][1:]
    # sessionStorage[user_id] = session

    return suggests


if __name__ == "__main__":
    app.run(host='0.0.0.0')