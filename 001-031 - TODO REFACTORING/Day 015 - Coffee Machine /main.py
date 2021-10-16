MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18
        },
        "cost": 1.5
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24
        },
        "cost": 2.5
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24
        },
        "cost": 3.0
    }
}

resources = {
    "ingredients": {
        "water": 300,
        "milk": 200,
        "coffee": 100
    },
    "money": 0
}

coins = {
    "quarters": 0.25,
    "dimes": 0.10,
    "nickles": 0.05,
    "pennies": 0.01
}

meters = {
    "water": "ml",
    "milk": "ml",
    "coffee": "g"
}


def print_report():
    """
    Prints report from the coffee machine, example:
    Water: 100ml
    Milk: 50ml
    Coffee: 76g
    Money: $2.5
    :return: None
    """
    for resource_key in resources['ingredients']:
        print(f"{resource_key.title()}: {resources['ingredients'][resource_key]}{meters[resource_key]}")
    print(f"Money: ${resources['money']:.2f}")


def check_resources(type_of_coffee):
    """
    Checks is there is enough resources to produce specific type of coffee
    :param type_of_coffee: can be "latte", "cappuccino" or "espresso"
    :return: A table where first element is True if coffee can be produced.
             Otherwise, first element of the table is False and second contains name of missing ingredient
    """
    for resource_key in resources['ingredients']:
        if resource_key in MENU[type_of_coffee]['ingredients'] and \
                resources['ingredients'][resource_key] < MENU[type_of_coffee]['ingredients'][resource_key]:
            return [False, resource_key]
    return [True, None]


def process_coins(type_of_coffee):
    """
    Asks customer for coins and calculates if it's enough to produce specific type of coffee
    :param type_of_coffee: can be "latte", "cappuccino" or "espresso"
    :return: A table where first element is False if given amount is lower than cost of the coffee.
             Otherwise, first element of the table is True and second contains value of the change.
    """
    money = 0
    value = MENU[type_of_coffee]['cost']
    print("Please insert coins.")
    for coin_key in coins:
        try:
            amount = int(input(f"How many {coin_key}?: ")) * coins[coin_key]
            if amount > 0:
                money += amount
        except ValueError:
            money += 0
    if money < value:
        print("Sorry that's not enough money. Money refunded.")
        return [False, None]
    else:
        return [True, money - value]


def update_resources(type_of_coffee):
    """
    Updates resources of the coffee machine after specific type of coffee is produced
    :param type_of_coffee: can be "latte", "cappuccino" or "espresso"
    :return: None
    """
    for ingredient_key in MENU[type_of_coffee]['ingredients']:
        resources['ingredients'][ingredient_key] -= MENU[type_of_coffee]['ingredients'][ingredient_key]
    resources['money'] += MENU[type_of_coffee]['cost']


turn_machine_in_service_mode = False
while not turn_machine_in_service_mode:
    command = input("What would you like? (espresso/latte/cappuccino): ")

    if command == "report":
        # hidden command: print report from the coffee machine
        print_report()
    elif command == "off":
        # hidden command: switch-off the coffee machine
        turn_machine_in_service_mode = True
    elif command in MENU:
        # process the order
        # 1. check available resources
        enough_resources = check_resources(command)
        if enough_resources[0]:
            # 2. accept coins and validate the amount
            transaction_result = process_coins(command)
            if transaction_result[0]:
                # 3. update available resources
                update_resources(command)
                # 4. finalize the order
                print(f"Here is ${transaction_result[1]:.2f} in change.")
                print(f"Here is your {command}. Enjoy! ☕️")
        else:
            print(f"Sorry there is not enough {enough_resources[1]}.")
    else:
        print("Wrong command.")
