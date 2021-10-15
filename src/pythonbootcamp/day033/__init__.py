import time
import tkinter
import tkinter.ttk
import pkg_resources
import requests
import geocoder
from datetime import datetime as dt
import pythonbootcamp.day032


class KanyeApp(tkinter.Tk):

    def __init__(self):
        super(KanyeApp, self).__init__()
        self.title('Kanye Says...')
        self.config(padx=50, pady=50)

        self.canvas = tkinter.Canvas(width=300, height=414)
        self.background_img = tkinter.PhotoImage(file=pkg_resources.
                                                 resource_filename(__name__, 'images/background.png'))
        self.canvas.create_image(150, 207, image=self.background_img)
        self.quote_text = self.canvas.create_text(150, 207, text='Kanye Quote Goes HERE', width=250,
                                                  font=("Arial", 25, 'bold'), fill='white')
        self.canvas.grid(row=0, column=0)

        self.kanye_img = tkinter.PhotoImage(file=pkg_resources.
                                            resource_filename(__name__, 'images/kanye.png'))
        kanye_button = tkinter.Button(image=self.kanye_img, highlightthickness=0, command=self.get_quote)
        kanye_button.grid(row=1, column=0)

    def get_quote(self):
        response = requests.get('https://api.kanye.rest/')
        response.raise_for_status()

        self.canvas.itemconfig(self.quote_text, text=response.json()['quote'])


class ISSTracker:
    subject = 'ISS is Visible!'
    delay = 20

    def __init__(self, location: str):
        # geolocation API
        try:
            g = geocoder.osm(location)
            self.observer = {
                'longitude': float(g.geojson['features'][0]['properties']['lng']),
                'latitude': float(g.geojson['features'][0]['properties']['lat'])
            }
        except IndexError:
            raise requests.exceptions.ConnectionError

        self.sunset_times: dict = {}
        self.iss_position: dict = {}
        # time formatted to YYYY:MM:SS hh:mm:ss+ZONE
        self.curr_datetime: dt = dt.fromisoformat(dt.utcnow().astimezone().
                                                  isoformat(sep=' ', timespec='seconds'))

    def get_sunset_times(self):
        # sunrise/sunset API
        response = requests.get('https://api.sunrise-sunset.org/json', {
            'lat': self.observer['latitude'],
            'lng': self.observer['longitude'],
            'formatted': 0
        })
        response.raise_for_status()
        self.sunset_times: dict = response.json()['results']

        # time formatted to YYYY:MM:SS hh:mm:ss+ZONE
        local_time_result = {key: dt.fromisoformat(self.sunset_times[key]).astimezone()
                             for key in self.sunset_times if key != 'day_length'}
        self.sunset_times.update(local_time_result)

    def get_iss_position(self):
        # ISS API
        response = requests.get('http://api.open-notify.org/iss-now.json')
        response.raise_for_status()
        self.iss_position: dict = response.json()['iss_position']
        self.iss_position['latitude'] = float(self.iss_position['latitude'])
        self.iss_position['longitude'] = float(self.iss_position['longitude'])

    def is_iss_overhead(self) -> bool:
        # has to be night
        if (self.sunset_times['sunset'] > self.curr_datetime or
            self.sunset_times['sunrise'] < self.curr_datetime) and \
                - 5 < self.iss_position['latitude'] - self.observer['latitude'] < 5 and \
                - 5 < self.iss_position['longitude'] - self.observer['longitude'] < 5:
            pythonbootcamp.day032.EmailSender(config_file_name='data/secret.json').send(
                subject=self.subject,
                message_text_plain=self.format_data_to_print())
            return True
        return False

    def format_data_to_print(self):
        def format_position(**kwargs):
            return {key: f"{kwargs[key]:0.08f}".rjust(13) for key in kwargs if key in ['latitude', 'longitude']}

        return f"ISS:{format_position(**self.iss_position)}\nYou:{format_position(**self.observer)}"

    def run_check(self) -> bool:
        self.get_sunset_times()
        self.get_iss_position()
        return self.is_iss_overhead()

    def main_loop(self):
        while True:
            try:
                text = ''
                if self.run_check():
                    print(self.subject)
            except requests.exceptions.ConnectionError:
                text = "Connection error ."
            else:
                print(self.format_data_to_print())
                text = "Waiting ."
            finally:
                for i in range(self.delay):
                    print(text if i == 0 else '.', end='')
                    time.sleep(1)
                print('.')
