import random


class User:

    def __init__(self, first_name="", second_name="", last_name=""):
        print("New user created.")
        self.first_name = first_name
        self.second_name = second_name
        self.last_name = last_name
        self.id = f"{random.SystemRandom().random() * 10e20:.0f}"
        self.followers = 0
        self.following = 0

    def follow(self, user):
        user.followers += 1
        self.following += 1

    def print(self):
        print(self)
        print(self.get_full_name())

    def get_full_name(self):
        return f"ID: {self.id}\nFull Name: {self.first_name} {self.second_name} {self.last_name}\n" + \
               f"Followers: {self.followers}\nFollowing: {self.following}"


user_1 = User("Ann", "Maria", "Hexelson")

# adding specific attributes to objects
user_1.car = "Audi"

print(user_1.get_full_name())
print("User 1 car: ", user_1.car)

user_2 = User(first_name="James", second_name="Henrik", last_name="Bond")
user_2.follow(user_1)

# adding specific attributes to objects
user_2.bike = "Giant"

print(user_2.get_full_name())
print("User 2 bike: ", user_2.bike)

print("\n\nEND:")
user_1.print()
user_2.print()
