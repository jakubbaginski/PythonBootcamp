import os
import random
from art import logo, vs
from game_data import data


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def select_next(data_set):
    next_set = random.choice(data_set)
    data_set.remove(next_set)
    return next_set


def decision(item_a, item_b):
    print(f"Compare A: {item_a['name']}, {item_a['description']}, from {item_a['country']}.")
    print(vs)
    print(f"Against B: {item_b['name']}, {item_b['description']}, from {item_b['country']}.")
    answer = input("Who has more followers? Type 'A' or 'B':").lower()

    if answer == "a" and item_a['follower_count'] > item_b['follower_count']:
        return True
    if answer == "b" and item_a['follower_count'] < item_b['follower_count']:
        return True
    return False


def game():
    game_data = data.copy()
    score = 0
    item_a = select_next(game_data)
    item_b = select_next(game_data)

    game_over = False
    while not game_over:

        clear()
        print(logo)

        if score > 0:
            print(f"You're right! Current score: {score}")

        if decision(item_a, item_b):
            score += 1
            if len(game_data) > 0:
                item_a = item_b
                item_b = select_next(game_data)
            else:
                game_over = True
                clear()
                print(logo)
                print(f"Fantastic result - you've got maximum score: {score}")
        else:
            game_over = True
            clear()
            print(logo)
            print(f"Sorry, that's wrong. Final score: {score}")


next_game = True
while next_game:
    game()
    if input("Do you want to play again? [Y/N]").lower() != "y":
        next_game = False
