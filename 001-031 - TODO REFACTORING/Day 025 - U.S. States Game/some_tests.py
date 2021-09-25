# import logging
#
# import prettytable
# import csv
#
# with open("weather_data.csv") as file:
#     data = prettytable.from_csv(file)
# print(data)
#
# data = []
# temperatures = []
#
# with open("weather_data.csv") as file:
#     data_from_file = csv.reader(file)
#     for row in data_from_file:
#         if data_from_file.line_num == 1:
#             headers = ['line'] + row
#         else:
#             data.append([data_from_file.line_num-1] + row)
#             try:
#                 data[-1][2] = int(data[-1][2])
#                 temperatures.append(data[-1][2])
#             except ValueError:
#                 logging.error("Expected int in second column")
#                 exit(1)
#
# table = prettytable.PrettyTable(headers)
# table.add_rows(data)
# print(table)
# print(temperatures)
# import time
# import datetime

# import pandas
# import json
# import sys
# from matplotlib import pyplot

# data = pandas.read_csv("weather_data.csv")
# print(data.info(verbose=True))
# print(data)
# data = data[data["temp"] > 12].astype({'temp': 'float64'}).sort_values(by='condition', ascending=False)
# data = data.set_index(pandas.date_range(start=datetime.date.today(), periods=len(data)))
# print(data.to_json())
# print(data["temp"].tolist())
#
# print(data["temp"].aggregate({'temp': 'average'}).values)
# print(data["temp"].mean())
# print(data["temp"].median())
# print(data["temp"].min())
# print(data.temp.min())
#
# print(data[data.condition == "Sunny"].temp.max())
# print(data[data.temp == data.temp.max()].temp.tolist()[0])
#
# data["temp"] = data["temp"] * 9/5 + 32
# data = data.rename(columns={"temp":"temp F"})
# print(data)
#
# x = {"Name": ["Ala", "Ela", "Ola"],
#      "Age": [21, 22, 32]
#      }
# y = pandas.DataFrame(x)
# y = y.set_index("Name")
# print(y)
# y.to_csv("girls.csv")

import pandas
data = pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
data = pandas.DataFrame(data["Primary Fur Color"]).reset_index().set_index("Primary Fur Color")
data = data.rename(columns={"index": "Count"}).groupby(level="Primary Fur Color").nunique(dropna=False)
data.to_csv("./new_data.csv")
