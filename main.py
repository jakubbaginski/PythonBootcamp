import pythonbootcamp.day032
import os

os.chdir('..')
print(os.getcwd())
print(pythonbootcamp.day032.MotivationQuote().random_quote())
pythonbootcamp.day032.AutomatedBirthdayWisher().run(config_file_name='data/secret.json')
