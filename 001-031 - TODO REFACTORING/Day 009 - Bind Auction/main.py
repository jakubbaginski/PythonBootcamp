from replit import clear
# HINT: You can call clear() to clear the output in the console.

from art import logo

auction = {}

clear()
print(logo)


def bind():
    name = input("Please provide your name: ")
    auction[name] = int(input("Please provide your bid: $"))


answer = "yes"
while answer == "yes":
    bind()
    answer = input("Is there anybody else in the action? [yes/no]:")
    clear()

win_value = 0
win_key = ""

for key in auction:
    if auction[key] > win_value:
        win_key = key
        win_value = auction[key]

print(f"The winner is {win_key} with bid ${win_value}")
