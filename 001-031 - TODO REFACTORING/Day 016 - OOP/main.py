from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

my_menu = Menu()
my_coffee_maker = CoffeeMaker()
my_money_machine = MoneyMachine()


is_the_machine_on = True
while is_the_machine_on:
    command = input(f"What would you like? ({my_menu.get_items()}): ")
    if command == "report":
        my_coffee_maker.report()
        my_money_machine.report()
    elif command == "off":
        is_the_machine_on = False
    else:
        drink = my_menu.find_drink(command)
        if drink is not None:
            if my_coffee_maker.is_resource_sufficient(drink) and my_money_machine.make_payment(drink.cost):
                my_coffee_maker.make_coffee(drink)
