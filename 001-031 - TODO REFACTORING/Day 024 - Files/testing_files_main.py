file = open("data/content.txt")
content = file.read()
print("##1")
print(content)
file.close()

with open("data/content.txt") as file:
    print("##2")
    print(file.readline())

with open("data/content.txt") as file:
    print("##3")
    print(file.read(15))

with open("data/content.txt") as file:
    print("##4")
    print(file.readlines())

file = open("./data/score.txt", 'r')
score = int(file.readlines()[-1].strip())
file.close()

file = open("./data/score.txt", 'a')
score += 1
file.write(f"\n{score:03d}")
file.close()
