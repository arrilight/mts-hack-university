import pickle

from authorization_builder import AuthBuilder


class Authorization:
    def __init__(self, session_id):
        self.session_storage = {}
        self.user_data = {}
        self.session_path = './sessions/'
        self.session_id = session_id
        self.load_session_storage()

    def is_authorized(self):
        return 'auth_status' in self.session_storage.keys() and self.session_storage['auth_status'] == 'authorized'

    def init_authorization(self):
        self.session_storage['auth_status'] = 'in_progress'

    def finish_authorization(self):
        self.session_storage['auth_status'] = 'authorized'
        del self.session_storage['auth_state']

    def authorize(self, req, res):
        result = None
        if 'auth_state' not in self.session_storage.keys():
            self.init_authorization()
            auth_builder = AuthBuilder(self.session_id)
            result = auth_builder.process_step()
        elif self.session_storage['auth_status'] == 'in_progress':
            auth_builder = AuthBuilder(self.session_id, self.session_storage['auth_state'])
            result = auth_builder.process_step(req)
        self.generate_response(res, result['title'])
        result['init'] = result['newstate']
        self.session_storage['auth_state'] = result
        if result['newstate'] is None:
            self.finish_authorization()
            self.generate_response(res, 'Авторизация прошла успешно!')
        self.save_session_storage()

    def save_session_storage(self):
        with open(self.session_path + self.session_id + '.pickle', 'wb') as f:
            pickle.dump(self.session_storage, f)

    def load_session_storage(self):
        self.session_storage = {}
        with open(self.session_path + self.session_id + '.pickle', 'rb') as f:
            self.session_storage = pickle.load(f)

    def generate_response(self, res, text):
        res['response']['text'] = text


