# -*- coding: utf-8 -*-
import workflow


class PlanBuilder:
    def __init__(self, saved_state=workflow.flow["build_plan"]):
        self.flow = workflow.flow["build_plan"]
        self.current_state = saved_state["init"]
        self.title = saved_state["title"]
        self.suggests = saved_state["suggests"]

    def process_step(self, req):
        result = {}
        getattr(self, self.current_state)(req)
        result["suggests"] = self.suggests
        result["title"] = self.title
        result["newstate"] = self.current_state
        return result

    def choose_minutes(self, req):
        entities = req["nlu"]["entities"]
        minutes = None
        for entity in entities:
            if entity.type == "YANDEX.NUMBER":
                minutes = entity.value

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
