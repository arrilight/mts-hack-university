# -*- coding: utf-8 -*-
from flask import Flask, request

app = Flask(__name__)

authorizedUses = set()
userToSMS = {}


@app.route('/sms_send', methods=['POST'])
def send_sms():
    # Вклюдчить генерацию возможно
    userToSMS[request.json['session_id']] = ["я", "ем", "мороженое"]
    return 'Sms was sent', 200


@app.route('/sms_check', methods=['POST'])
def check_sms():
    if not request.json.__contains__('words') or userToSMS[request.json['session_id']] != request.json['words']:
        return 'Words are not equal!', 401
    else:
        authorizedUses.add(request.json['session_id'])
        return 'Successful', 200


@app.route('/', methods=['POST'])
def hello_world():
    if not check_authorization(request):
        return 'Not authorized', 401
    else:
        return 'Hello world!'


def check_authorization(req):
    return req.json.__contains__('session_id') and authorizedUses.__contains__(req.json['session_id'])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
