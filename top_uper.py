from __future__ import unicode_literals

import workflow


class TopUper:
    def __init__(self, saved_state=workflow.flow["top_up"]):
        self.flow = workflow.flow["top_up"]
        self.current_state = saved_state["init"]
        self.title = saved_state["title"]
        self.suggests = saved_state["suggests"]

    def process_step(self, req=None):
        result = {}
        if req is not None:
            getattr(self, self.current_state)(req)
        result["suggests"] = self.suggests
        result["title"] = self.title
        result["newstate"] = self.current_state
        return result

    def chose_to_who(self, req):
        my_tel_number = '+79179076245'
        reciever = None

        response = req['command']

        if 'мне' in req['nlu']['tokens']:
            reciever = my_tel_number
            new_flow = self.flow["state"][self.current_state]["events"]["next"]
            self.current_state = new_flow["newstate"]
            self.title = new_flow["title"]
            self.suggests = new_flow["suggests"]
            return

        if response == 'другой номер':
            new_flow = self.flow["state"][self.current_state]["events"]['enter_other_number']
            self.current_state = new_flow["newstate"]
            self.title = new_flow["title"]
            self.suggests = None
            return

    def other_number(self, req):
        reciever = ''

        entities = req['nlu']['entities']
        for entity in entities:
            if entity['type'] == "YANDEX.NUMBER":
                reciever = entity["value"]

        new_flow = self.flow["state"][self.current_state]["events"]["next"]
        self.current_state = new_flow["newstate"]
        self.title = new_flow["title"]
        self.suggests = new_flow["suggests"]

    def choose_amount(self, req):

        entities = req['nlu']['entities']
        for entity in entities:
            if entity['type'] == "YANDEX.NUMBER":
                amount = entity["value"]

            # number wasn't recognised
            if amount is None:
                self.current_state = self.current_state
                self.title = "Я не смогла понять сумму, попробуй еще раз."
                self.suggests = self.suggests
                return

            if isinstance(amount, type([])):
                self.current_state = self.current_state
                self.title = "Пожалуйста, назови только одно число."
                self.suggests = self.suggests
                return

            if isinstance(amount, int) and amount < 0:
                self.current_state = self.current_state
                self.title = "Сумма должна быть неотрицательным числом."
                self.suggests = self.suggests
                return

            if isinstance(amount, int) and amount > 10000:
                self.current_state = self.current_state
                self.title = "Сумма не может быть больше 10000."
                self.suggests = self.suggests
                return

            new_flow = self.flow["state"][self.current_state]["events"]["next"]
            self.current_state = new_flow["newstate"]
            self.title = new_flow["title"]
            self.suggests = new_flow["suggests"]

    def choose_source(self, req):
        response = req['command']

        if response == 'моя карта МТС Банка':
            self.current_state = None
            self.title = "Пополняю счет с твоей карты МТС Банка"
            self.suggests = None
            return

        if response == 'с мобильного баланса':
            self.current_state = None
            self.title = "Пополняю счет с твоего мобильного баланса"
            self.suggests = None
            return

        self.current_state = self.current_state
        self.title = "Я не совсем поняла. Выбери валидный способ оплаты."
        self.suggests = self.suggests
