import workflow
import requests


class AuthBuilder:
    def __init__(self, session_id, saved_state=workflow.flow["authorization"]):
        self.flow = workflow.flow["authorization"]
        self.current_state = saved_state["init"]
        self.title = saved_state["title"]
        self.suggests = saved_state["suggests"]
        self.service_ip = 'http://localhost:8000'
        self.session_id = session_id
        self.word_enter_attemps = 3

    def process_step(self, req=None):
        result = {}
        if req is not None:
            getattr(self, self.current_state)(req)
        result["suggests"] = self.suggests
        result["title"] = self.title
        result["newstate"] = self.current_state
        return result

    def number_validation(self, req):
        is_valid_number = (req['command'][0:2] == '+7' and len(req['command']) == 12) or (req['command'][0] == '8' and len(req['command']) == 11)

        if not is_valid_number:
            self.current_state = self.current_state
            self.title = "Номер должен быть начинаться с +7 или 8. Пожалуйста, попробуйте снова."
            self.suggests = self.suggests
            return

        # here we should add MTS logic
        new_flow = self.flow["state"][self.current_state]["events"]["next"]
        self.current_state = new_flow["newstate"]
        self.title = new_flow["title"]
        self.suggests = new_flow["suggests"]
        requests.post(self.service_ip + '/sms_send', json={'session_id': self.session_id})

    def sms_input(self, req):
        words = req['nlu']['tokens']
        r = requests.post(self.service_ip + '/sms_check', json={'session_id': self.session_id, 'words': words})
        self.word_enter_attemps -= 1

        if self.word_enter_attemps == 0:
            self.word_enter_attemps = 3
            new_flow = self.flow["state"][self.current_state]["events"]["fail"]
            self.current_state = new_flow["newstate"]
            self.title = new_flow["title"]
            self.suggests = new_flow["suggests"]
            return

        if r.status_code != 200:
            self.current_state = self.current_state
            self.title = "Неверный ввод"
            self.suggests = self.suggests
            return

        self.current_state = None
        self.title = ""
        self.suggests = None
