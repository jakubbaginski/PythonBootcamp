from art import logo
print(logo)

def add(n1, n2):
    return n1 + n2

def substract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

operations = {
    "+": add,
    "-": substract,
    "*": multiply,
    "/": divide
}

continiueFlag = True
newCalculation = True

while continiueFlag:

    result = 0

    if newCalculation:
        n1 = float(input("1st number: "))
    
    op = input(f"Operation {list(operations.keys())} ")
    n2 = float(input("2nd number: "))
    
    result = operations[op](n1, n2)

    print(f"Result of {n1}{op}{n2} = {result}")
    decision = input("[C]ontinue with result, [N]ew calculation, [Q]uit")
    if decision.lower() == "c":
        newCalculation = False
        n1 = result
    elif decision.lower() == "n":
        newCalculation = True
    else:
        continiueFlag = False

