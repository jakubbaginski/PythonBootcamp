import random
from art import logo
from replit import clear

############### Blackjack Project #####################

# Difficulty Normal 😎: Use all Hints below to complete the project.
# Difficulty Hard 🤔: Use only Hints 1, 2, 3 to complete the project.
# Difficulty Extra Hard 😭: Only use Hints 1 & 2 to complete the project.
# Difficulty Expert 🤯: Only use Hint 1 to complete the project.

############### Our Blackjack House Rules #####################

## The deck is unlimited in size. 
## There are no jokers. 
## The Jack/Queen/King all count as 10.
## The the Ace can count as 11 or 1.
## Use the following list as the deck of cards:
## cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
## The cards in the list have equal probability of being drawn.
## Cards are not removed from the deck as they are drawn.
## The computer is the dealer.

##################### Hints #####################

# Hint 1: Go to this website and try out the Blackjack game: 
#   https://games.washingtonpost.com/games/blackjack/
# Then try out the completed Blackjack project here: 
#   http://blackjack-final.appbrewery.repl.run

# Hint 2: Read this breakdown of program requirements: 
#   http://listmoz.com/view/6h34DJpvJBFVRlZfJvxF
# Then try to create your own flowchart for the program.

# Hint 3: Download and read this flow chart I've created: 
#   https://drive.google.com/uc?export=download&id=1rDkiHCrhaf9eX7u7yjM1qwSuyEk-rPnt

# Hint 4: Create a deal_card() function that uses the List below to *return* a random card.
# 11 is the Ace.
# cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

# Hint 5: Deal the user and computer 2 cards each using deal_card() and append().
# user_cards = []
# computer_cards = []

# Hint 6: Create a function called calculate_score() that takes a List of cards as input 
# and returns the score. 
# Look up the sum() function to help you do this.

# Hint 7: Inside calculate_score() check for a blackjack (a hand with only 2 cards: ace + 10) and return 0 instead of the actual score. 0 will represent a blackjack in our game.

# Hint 8: Inside calculate_score() check for an 11 (ace). If the score is already over 21, remove the 11 and replace it with a 1. You might need to look up append() and remove().

# Hint 9: Call calculate_score(). If the computer or the user has a blackjack (0) or if the user's score is over 21, then the game ends.

# Hint 10: If the game has not ended, ask the user if they want to draw another card. If yes, then use the deal_card() function to add another card to the user_cards List. If no, then the game has ended.

# Hint 11: The score will need to be rechecked with every new card drawn and the checks in Hint 9 need to be repeated until the game ends.

# Hint 12: Once the user is done, it's time to let the computer play. The computer should keep drawing cards as long as it has a score less than 17.

# Hint 13: Create a function called compare() and pass in the user_score and computer_score. If the computer and user both have the same score, then it's a draw. If the computer has a blackjack (0), then the user loses. If the user has a blackjack (0), then the user wins. If the user_score is over 21, then the user loses. If the computer_score is over 21, then the computer loses. If none of the above, then the player with the highest score wins.

# Hint 14: Ask the user if they want to restart the game. If they answer yes, clear the console and start a new game of blackjack and show the logo from art.py.

init_cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4


def get_card(cards):
    card = random.choice(cards)
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
