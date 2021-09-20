import json
import requests
import geocoder
from twilio.rest import Client


class GEOLocation:

    def __init__(self, location: str):
        self.observer: dict = {}
        try:
            g = geocoder.osm(location)
            self.observer = {
                'lon': float(g.geojson['features'][0]['properties']['lng']),
                'lat': float(g.geojson['features'][0]['properties']['lat'])
            }
        except IndexError:
            raise requests.exceptions.ConnectionError


class Weather:

    api_keys = {
        'required': ['lat', 'lon', 'appid'],
        'optional': ['exclude', 'units', 'lang']
    }

    def __init__(self, location: GEOLocation = None, **kwargs):
        try:
            with open('data/secret.json', 'r') as config_file:
                params = json.load(config_file)
                params = params["OWM"]
        except FileNotFoundError:
            pass
        params.update(location.observer)
        params.update(**kwargs)
        url = params['url']
        params = {key: params.get(key) for key in params if key in
                  self.api_keys['required'] + self.api_keys['optional']}
        self.response = requests.get(url, params)

    def is_it_to_rain_in_next_hours(self, hours: int):
        # next 12 hours
        for data in self.response.json()['hourly'][:hours]:
            # print(datetime.datetime.fromtimestamp(data['dt']))
            if data.get('rain') is not None or data.get('snow') is not None:
                # print(data['rain'])
                return True
        return False


class Main:

    def __init__(self, hours):
        location = GEOLocation("London")
        print(Weather(location, lang='pl').is_it_to_rain_in_next_hours(hours))

        with open('data/secret.json', 'r') as config_file:
            param = json.load(config_file)
            param = param['TWILIO']
            client = Client(param['TWILIO_ACCOUNT_SID'], param['TWILIO_AUTH_TOKEN'])
            message = client.messages \
                .create(
                     body=f"Rain in next {hours} hours: {Weather(location, lang='pl').is_it_to_rain_in_next_hours(hours)}",
                     from_=param['FROM'],
                     to=param['TO']
                 )
            print(message.sid)


Main(24)
