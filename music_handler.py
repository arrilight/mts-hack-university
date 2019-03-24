from __future__ import unicode_literals

import workflow


class MusicHandler:
    def __init__(self, saved_state=workflow.flow["handle_music"]):
        self.flow = workflow.flow["handle_music"]
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

    def search_music(self, req):
        name = None

        response = req['command']
        new_flow = self.flow["state"][self.current_state]["events"]["next"]
        self.current_state = new_flow["newstate"]
        self.title = new_flow["title"]
        self.suggests = new_flow["suggests"]
        return

    def add_music(self, req):
        response = req['command']

        if response == 'Добавить' or response == 'Спасибо':
            new_flow = self.flow["state"]['add_music']['events']['next']
            self.current_state = None
            self.title = new_flow["title"]
            self.suggests = new_flow["suggests"]
            return

        self.current_state = self.current_state
        self.title = "Я не совсем поняла. Выбери один из предложенных вариантов."
        self.suggests = self.suggests
