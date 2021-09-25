student_scores = {
    "Harry": 81,
    "Ron": 78,
    "Hermione": 99,
    "Draco": 74,
    "Neville": 62,
}
# 🚨 Don't change the code above 👆

#TODO-1: Create an empty dictionary called student_grades.

student_grades = {}
grades = {
    91: "Outstanding",
    81: "Exceeds Expectations",
    71: "Acceptable",
    0: "Fail"
}

#TODO-2: Write your code below to add the grades to student_grades.👇

for student in student_scores:
    found = False
    for grade in grades:
        if student_scores[student] >= grade and found == False:
            student_grades[student] = grades[grade]
            found = True

        # 🚨 Don't change the code below 👇
print(student_grades)


travel_log = {
    "France": {
        "cities visited": ["Paris", "Lille", "Dijon"],
        "number of visits": [1,2,3]
    },
    "Germany": {
        "cities visited": ["Berlin", "Bonn"],
        "number of visits": [3,2]
    }
}

travel_log_2 = [
    {
        "country": "France",
        "cities visited": ["Paris", "Lille", "Dijon"],
        "number of visits": [1,2,3],
        "total visits": 2
    },
    {
        "country": "Germany",
        "cities visited": ["Berlin", "Bonn"],
        "number of visits": [3,2],
        "total visits": 1
    }
]


for item in travel_log:
    print (f"{item}: {travel_log[item]}.")

print(travel_log_2)

