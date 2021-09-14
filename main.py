import pythonbootcamp.day032
import os

os.chdir('..')
# print(pythonbootcamp.day032.MotivationQuote().random_quote())
pythonbootcamp.day032.AutomatedBirthdayWisher().run(config_file_name='data/secret.json', sender_name='Kuba')
