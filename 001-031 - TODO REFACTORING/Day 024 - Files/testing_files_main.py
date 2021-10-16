file = open("data/content.txt")
content = file.read()
print("##1")
print(content)
file.close()

file_name = 'data/content.txt'
with open(file_name) as file:
    print("##2")
    print(file.readline())

with open(file_name) as file:
    print("##3")
    print(file.read(15))

with open(file_name) as file:
    print("##4")
    print(file.readlines())

file_name = './data/score.txt'
file = open(file_name, 'r')
score = int(file.readlines()[-1].strip())
file.close()

file = open(file_name, 'a')
score += 1
file.write(f"\n{score:03d}")
file.close()
