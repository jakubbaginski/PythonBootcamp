import tkinter
import tkinter.ttk
import pkg_resources
import requests


class KanyeApp(tkinter.Tk):

    def __init__(self):
        super(KanyeApp, self).__init__()
        self.title('Kanye Says...')
        self.config(padx=50, pady=50)

        self.canvas = tkinter.Canvas(width=300, height=414)
        self.background_img = tkinter.PhotoImage(file=pkg_resources.
                                                 resource_filename(__name__, 'img/background.png'))
        self.canvas.create_image(150, 207, image=self.background_img)
        self.quote_text = self.canvas.create_text(150, 207, text='Kanye Quote Goes HERE', width=250,
                                                  font=("Arial", 25, 'bold'), fill='white')
        self.canvas.grid(row=0, column=0)

        self.kanye_img = tkinter.PhotoImage(file=pkg_resources.
                                            resource_filename(__name__, 'img/kanye.png'))
        kanye_button = tkinter.Button(image=self.kanye_img, highlightthickness=0, command=self.get_quote)
        kanye_button.grid(row=1, column=0)

    def get_quote(self):
        response = requests.get('https://api.kanye.rest/')
        response.raise_for_status()

        self.canvas.itemconfig(self.quote_text, text=response.json()['quote'])


