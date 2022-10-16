file = open("text.txt", "r")
number = [0] * 256
for i in range(256):
    number[i] = [chr(i), 0]
f = file.read()
for i in f:
    number[ord(i)][1] += 1
j = 0
count = []
for i in range(0, 256):
    if number[i][1] != 0:
        count.append(number[i])
print(count)
