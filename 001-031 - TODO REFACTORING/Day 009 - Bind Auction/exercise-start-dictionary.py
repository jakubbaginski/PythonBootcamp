programming_dictionary = {
    "Bug": "An error in a program that prevents the program from running as expected.",
    "Function": "A piece of code that you can easily call over and over again."
}

programming_dictionary["Test"] = "Test is a test"
programming_dictionary["Bug"] = "Bug is a bug"
programming_dictionary["Function"] = False

print(programming_dictionary)

for item in programming_dictionary:
    print(f"Key:{item} Value:{programming_dictionary[item]}")