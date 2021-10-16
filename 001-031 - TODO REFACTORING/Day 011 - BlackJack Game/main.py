import secrets
from art import logo
from replit import clear

init_cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4


def get_card(cards):
    card = secrets.choice(cards)
    cards.remove(card)
    return card


def calc_result(cards):
    result = 0
    num_of_as = 0
    for card in cards:
        result += card
        if card == 11:
            num_of_as += 1

    while result > 21 and num_of_as > 0:
        num_of_as -= 1
        result -= 10

    return result


def get_two_cards(cards):
    two_cards = []
    for _ in range(2):
        two_cards.append(get_card(cards))
    return two_cards


def blackjack(cards):
    if len(cards) == 2 and calc_result(cards) == 21:
        return True
    return False


def get_dealer_cards(cards):
    dealer_cards = get_two_cards(cards)
    while calc_result(dealer_cards) < 17:
        dealer_cards.append(get_card(cards))
    return dealer_cards


continueFlag = True

while continueFlag:
    clear()
    print(logo)
    cards = init_cards.copy()

    dealer_cards = get_dealer_cards(cards)
    your_cards = get_two_cards(cards)

    getNextCardFlag = True
    while getNextCardFlag:
        your_score = calc_result(your_cards)
        print(f"You cards: {your_cards}, current score: {your_score}")
        print(f"Dealer first card: {dealer_cards[0]}")
        if blackjack(your_cards) or blackjack(dealer_cards):
            getNextCardFlag = False
        elif input("Type 'y' to get another card, other key means no: ") == "y":
            your_cards.append(get_card(cards))
            if calc_result(your_cards) >= 21:
                getNextCardFlag = False
        else:
            getNextCardFlag = False

    your_score = calc_result(your_cards)
    dealer_score = calc_result(dealer_cards)
    print(f"Your final score hand: {your_cards}, final_score: {your_score}")
    print(f"Dealer final score hand: {dealer_cards}, final_score: {dealer_score}")

    if blackjack(your_cards) and your_score != dealer_score:
        print("BlackJack! You win! 🚀🚀🚀🚀🚀🚀🚀")
    elif your_score > 21 or (your_score < dealer_score <= 21):
        if blackjack(dealer_cards):
            print("Dealer's BlackJack. You lost. 👿👿👿👿👿👿👿")
        else:
            print("You lost. 👿")
    elif your_score == dealer_score:
        print("Draw. 😃")
    else:
        print("You win! 🚀🚀")

    if input("Type 'y' to play again, other key means no: ") != "y":
        continueFlag = False
