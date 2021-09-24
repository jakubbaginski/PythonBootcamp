import json

import requests


class StockData:

    def __init__(self):
        super(StockData, self).__init__()
        with open('data/secret.json', 'r') as config_file:
            config = json.load(config_file)["ALPHA"]
        params = {
            'function': 'DIGITAL_CURRENCY_DAILY',
            'symbol': 'XRP',
            'market': 'EUR',
            'apikey': config['key']
        }
        result = requests.get(config['url'], params)
        print(result.json())


StockData()