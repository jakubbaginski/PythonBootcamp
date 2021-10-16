student_scores = {
    "Harry": 81,
    "Ron": 78,
    "Hermione": 99,
    "Draco": 74,
    "Neville": 62,
}

student_grades = {}
grades = {
    91: "Outstanding",
    81: "Exceeds Expectations",
    71: "Acceptable",
    0: "Fail"
}

for student in student_scores:
    found = False
    for grade in grades:
        if student_scores[student] >= grade and found == False:
            student_grades[student] = grades[grade]
            found = True

print(student_grades)

key_country = 'country'
key_cities = 'cities visited'
key_visits = 'number of visits'
key_total_visits = 'total_visits'

travel_log = {
    "France": {
        key_cities: ["Paris", "Lille", "Dijon"],
        key_visits: [1, 2, 3]
    },
    "Germany": {
        key_cities: ["Berlin", "Bonn"],
        key_visits: [3,2]
    }
}

travel_log_2 = [
    {
        key_country: "France",
        key_cities: ["Paris", "Lille", "Dijon"],
        key_visits: [1, 2, 3],
        key_total_visits: 2
    },
    {
        key_country: "Germany",
        key_cities: ["Berlin", "Bonn"],
        key_visits: [3, 2],
        key_total_visits: 1
    }
]


for item in travel_log:
    print (f"{item}: {travel_log[item]}.")

print(travel_log_2)

