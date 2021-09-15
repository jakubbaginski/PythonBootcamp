import requests


class TriviaQuizzerApp:

    # API's URL https://opentdb.com/api_config.php
    # params of the value None are not to be passed through API
    API_PARAMS = {
        'amount': 1,
        'type': 'boolean',
        'category': None,
        'difficulty': None,
        'encode': None
    }

    def __init__(self, **kwargs):
        self.questions = []
        self.api_params = self.API_PARAMS.copy()
        self.update_api_params(**kwargs)
        pass

    def update_api_params(self, **kwargs):
        not_default_params = {key: kwargs[key] for key in kwargs if key in self.API_PARAMS}
        self.api_params.update(not_default_params)
        self.api_params = {key: self.api_params[key] for key in self.api_params if self.api_params[key] is not None}

    def get_new_question(self, **kwargs):
        self.update_api_params(**kwargs)
        print(self.api_params)
        response = requests.get('https://opentdb.com/api.php', params=self.api_params)
        response.raise_for_status()
        self.questions: dict = response.json()['results']
        print(self.questions)


TriviaQuizzerApp(difficulty='hard').get_new_question(amount=10, difficulty=None)
