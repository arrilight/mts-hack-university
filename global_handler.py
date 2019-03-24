import pickle
from nltk.stem.snowball import SnowballStemmer

from top_uper import TopUper
from plan_builder import PlanBuilder
from  music_handler import MusicHandler


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

        music_stemmed = {"музык", "песн", "мелод", "игра", "проигра", "сыгра", "включ", "добав"}
        plan_stemmed = {"тариф", "план"}
        top_up_stemmed = {"счет", "баланс", "закинь", "кинь", "пополн", "полож"}

        stemmer = SnowballStemmer("russian")
        stemmed_tokens = set([stemmer.stem(word) for word in tokens])

        program = None
        flow_state = None
        if len(stemmed_tokens.intersection(plan_stemmed)) > 0:
            self.session_storage['current_subflow'] = 'plan_builder'
            program = PlanBuilder()
        if len(stemmed_tokens.intersection(top_up_stemmed)) > 0:
            self.session_storage['current_subflow'] = 'top_up'
            program = TopUper()
            # if len(stemmed_tokens.intersection({'', ''})) > 0:
              #  program.process_step()
        if len(stemmed_tokens.intersection(music_stemmed)) > 0:
            self.session_storage['current_subflow'] = 'handle_music'
            program = MusicHandler()
        if program is None:
            self.generate_response(res, 'Я тебя не поняла. Попытайся объясниться по-другому.')
            return

        # вся оставшаяся логика по рекогнишену будет тут
        result = program.process_step()
        if isinstance(program, type(TopUper)) and len(stemmed_tokens.intersection({'', ''})) > 0:
            result['init'] = result['newstate']
            program = TopUper(result)
            result = program.process_step(req)
        self.generate_response(res, result['title'], result['suggests'])
        result['init'] = result['newstate']
        self.session_storage['flow_state'] = result

    def handle_specific_request(self, req, res):
        if self.check_stop_word(req, res):
            return
        program = None
        name = self.session_storage['current_subflow']
        state = self.session_storage['flow_state']
        if name == 'plan_builder':
            program = PlanBuilder(state)
        if name == 'top_up':
            program = TopUper(state)
        if name == 'handle_music':
            program = MusicHandler(state)

        result = program.process_step(req)
        self.generate_response(res, result['title'], result['suggests'])
        result['init'] = result['newstate']
        if result['newstate'] is None:
            self.exit_subflow()
            self.generate_response(res, res['response']['text'] + '\nКакие у тебя ещё есть ко мне вопросы?')

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

    def exit_subflow(self):
        del self.session_storage['current_subflow']
        del self.session_storage['flow_state']

    def check_stop_word(self, req, res):
        if 'остановись' in req['nlu']['tokens']:
            self.exit_subflow()
            res['response']['text'] = 'Хорошо, останавливаюсь. Чем ещё тебе помочь?'
            return True
        return False

    @staticmethod
    def generate_response(res, text, buttons = None):
        res['response']['text'] = text
        res['response']['buttons'] = buttons