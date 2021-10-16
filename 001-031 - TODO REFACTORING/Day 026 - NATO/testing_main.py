import random

numbers = [2, 3, 4]
new_numbers = [n + 1 for n in numbers]
print(new_numbers)

name = "Kuba"
letter: str
new_name = [letter.title() for letter in name]
print(new_name)

new_range = [x * 2 for x in range(1, 5)]
print(new_range)

new_range = [x * 2 for x in range(1, 5) if x % 2 == 0]
new_range += [x / 2 for x in range(1, 5) if x % 2 == 1]
print(new_range)

names = ["Ala", "Ola", "Aleksandra", "Patrycja"]
new_names = [n for n in names if len(n) <= 3]
print(new_names)
new_names = [n.upper() for n in names if len(n) > 3]
print(new_names)

# Exercise 1 - Squaring Numbers
numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
squared_numbers = [n**2 for n in numbers]
print(squared_numbers)

# Exercise 2 - Even Numbers
result = [n for n in numbers if n % 2 == 0]
print(result)

# Exercise 3 - Data Overlap


def my_func(file_name: str) -> []:
    with open(file_name) as file:
        return [int(x.strip()) for x in file.readlines()]


result = [x for x in my_func("file1.txt") if x in my_func("file2.txt")]
print(result)


# Exercise 4 - Dictionary Comprehension Start

students = ["Ala", "Ela", "Ola", "Ula", "Zuza", "Kasia", "Asia", "Gosia"]
students_and_scores = {student: random.SystemRandom().randint(1, 100) for student in students}
students_passed = {student: score for (student, score) in students_and_scores.items() if score > 60}
print(students_and_scores)
print(students_passed)


# Exercise 5 - Dictionary Comprehension 1

sentence = "What is the Airspeed Velocity of an Unladen Swallow?"
result = {word: len(word) for word in sentence.split(" ")}
print(result)


# Exercise 6 - Dictionary Comprehension 2

weather_c = {
    "Monday": 12,
    "Tuesday": 14,
    "Wednesday": 15,
    "Thursday": 14,
    "Friday": 21,
    "Saturday": 22,
    "Sunday": 24,
}
weather_f = {day: temp*9/5+32 for (day, temp) in weather_c.items()}
print(weather_f)
