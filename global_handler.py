import pickle

from plan_builder import PlanBuilder


class GlobalHandler:
    def __init__(self, session_id):
        self.session_storage = {}
        self.user_data = {}
        self.session_path = './sessions/'
        self.session_id = session_id
        self.load_session_storage()

    def handle_request(self, req, res):
        # current flow переимновыываем в current subflow
        if 'current_subflow' not in self.session_storage.keys():
            self.handle_generic_request(req, res)
            self.save_session_storage()
            return
        self.handle_specific_request(req, res)
        self.save_session_storage()

    def handle_generic_request(self, req, res):
        original_utterance = req['original_utterance']
        tokens = req['nlu']['tokens']
        program = None
        flow_state = None
        if 'тариф' in tokens:
            self.session_storage['current_subflow'] = 'plan_builder'
            program = PlanBuilder()
        # вся оставшаяся логика по рекогнишену будет тут
        result = program.process_step()
        res['response']['text'] = result['title']
        res['response']['buttons'] = self.get_suggests(result['suggests'])
        result['init'] = result['newstate']
        self.session_storage['flow_state'] = result

    def handle_specific_request(self, req, res):
        program = None
        name = self.session_storage['current_subflow']
        state = self.session_storage['flow_state']
        if name == 'plan_builder':
            program = PlanBuilder(state)


        if name == 'top_up':
            ...
        if name == 'music':
            ...

        result = program.process_step(req)
        res['response']['text'] = result['title']
        res['response']['buttons'] = self.get_suggests(result['suggests'])
        result['init'] = result['newstate']
        self.session_storage['flow_state'] = result

    def load_session_storage(self):
        self.session_storage = {}
        with open(self.session_path + self.session_id + '.pickle', 'rb') as f:
            self.session_storage = pickle.load(f)

    def save_session_storage(self):
        with open(self.session_path + self.session_id + '.pickle', 'wb') as f:
            pickle.dump(self.session_storage, f)

    def load_user_data(self):
        ...

    def save_user_data(self):
        ...

    def get_suggests(self, suggestions_raw):

        if suggestions_raw is None:
            return None

        # Выбираем две первые подсказки из массива.
        suggests = [
            {'title': suggest, 'hide': True}
            for suggest in suggestions_raw
        ]

        return suggests
