# -*- coding: utf-8 -*-
import workflow


class PlanBuilder:
    def __init__(self, saved_state=workflow.flow["build_plan"]):
        self.flow = workflow.flow["build_plan"]
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

    def choose_minutes(self, req):
        entities = req["nlu"]["entities"]
        minutes = None
        for entity in entities:
            if entity["type"] == "YANDEX.NUMBER":
                minutes = entity["value"]

        # number wasn't recognised
        if minutes is None:
            self.current_state = self.current_state
            self.title = "Я не смогла понять сколько минут вам нужно, попробуйте еще раз"
            self.suggests = self.suggests
            return

        if isinstance(minutes, type([])):
            self.current_state = self.current_state
            self.title = "Пожалуйста, назовите только одно число"
            self.suggests = self.suggests
            return

        if isinstance(minutes, int) and minutes < 0:
            self.current_state = self.current_state
            self.title = "Количество минут не может быть отрицательным"
            self.suggests = self.suggests
            return

        if isinstance(minutes, int) and minutes > 10000:
            self.current_state = self.current_state
            self.title = "Количество минут не может быть больше 10000"
            self.suggests = self.suggests
            return

        # here we should add MTS logic
        new_flow = self.flow["state"][self.current_state]["events"]["next"]
        self.current_state = new_flow["newstate"]
        self.title = new_flow["title"]
        self.suggests = new_flow["suggests"]

    def choose_data(self, req):
        entities = req["nlu"]["entities"]
        minutes = None
        for entity in entities:
            if entity["type"] == "YANDEX.NUMBER":
                minutes = entity["value"]

        # number wasn't recognised
        if minutes is None:
            self.current_state = self.current_state
            self.title = "Я не смогла понять сколько гигабайт интернета вам нужно, попробуйте еще раз"
            self.suggests = self.suggests
            return

        if isinstance(minutes, type([])):
            self.current_state = self.current_state
            self.title = "Пожалуйста, назовите только одно число"
            self.suggests = self.suggests
            return

        if isinstance(minutes, int) and minutes < 0:
            self.current_state = self.current_state
            self.title = "Количество гигабайт не может быть отрицательным"
            self.suggests = self.suggests
            return

        if isinstance(minutes, int) and minutes > 10000:
            self.current_state = self.current_state
            self.title = "Количество гигабайт не может быть больше 10000"
            self.suggests = self.suggests
            return

        # here we should add MTS logic
        new_flow = self.flow["state"][self.current_state]["events"]["next"]
        self.current_state = new_flow["newstate"]
        self.title = new_flow["title"]
        self.suggests = new_flow["suggests"]

    def choose_sms(self, req):
        entities = req["nlu"]["entities"]
        minutes = None
        for entity in entities:
            if entity["type"] == "YANDEX.NUMBER":
                minutes = entity["value"]

        # number wasn't recognised
        if minutes is None:
            self.current_state = self.current_state
            self.title = "Я не смогла понять сколько смс вам нужно, попробуйте еще раз"
            self.suggests = self.suggests
            return

        if isinstance(minutes, type([])):
            self.current_state = self.current_state
            self.title = "Пожалуйста, назовите только одно число"
            self.suggests = self.suggests
            return

        if isinstance(minutes, int) and minutes < 0:
            self.current_state = self.current_state
            self.title = "Количество минут не может быть отрицательным"
            self.suggests = self.suggests
            return

        if isinstance(minutes, int) and minutes > 10000:
            self.current_state = self.current_state
            self.title = "Количество минут не может быть больше 10000"
            self.suggests = self.suggests
            return

        # here we should add MTS logic
        new_flow = self.flow["state"][self.current_state]["events"]["next"]
        self.current_state = new_flow["newstate"]
        self.title = new_flow["title"]
        self.suggests = new_flow["suggests"]

    def choose_tv(self, req):
        tokens = req["nlu"]["tokens"]

        # number wasn't recognised

        if "да" in tokens:
            # save positive response

            self.current_state = None
            self.title = "Ваш тариф создан!"
            self.suggests = None
            return

        if "нет" in tokens:
            # save negative response
            self.current_state = None
            self.title = "Ваш тариф создан!"
            self.suggests = None
            return

        self.current_state = self.current_state
        self.title = "Я не совсем поняла. Ответь да или нет."
        self.suggests = self.suggests



