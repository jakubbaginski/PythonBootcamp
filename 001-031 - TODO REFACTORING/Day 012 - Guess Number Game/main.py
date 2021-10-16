from art import logo
from replit import clear
from secrets import choice

NUMBER_OF_GUESSES_EXPERT = 7
NUMBER_OF_GUESSES_BEGGINER = 10


def game():

    clear()
    print(logo)

    number_of_guesses = NUMBER_OF_GUESSES_EXPERT
    level = input("Wybierz Poziom: [P]oczątkujący, [E]kspert: ")
    if level == "P":
        number_of_guesses = NUMBER_OF_GUESSES_BEGGINER

    number = choice(range(1, 101))
    guess = 0

    while number_of_guesses > 0 and guess != number:
        guess = int(input("Podaj liczbę: "))
        if guess > number:
            print(f"Liczba {guess} jest zbyt duża.")
        elif guess < number:
            print(f"Liczba {guess} jest zbyt mała.")
        else:
            print(f"BRAWO!")
            return
        number_of_guesses -= 1
        if number_of_guesses == 0:
            print(f"Nie udało się.")
            return
        else:
            print(f"Pozostała liczba prób: {number_of_guesses}.")
            

game()
while input("Czy chcesz zagrać jeszcze raz [T/N]").lower() == "t":
    game()         
