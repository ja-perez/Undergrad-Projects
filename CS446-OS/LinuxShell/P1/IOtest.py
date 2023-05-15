import os
file = open('test.txt', 'a')
with open('disk.txt') as f:
    lines = f.read().split()
file.close()
os.system("echo Hello World > test.txt")
file = open('test.txt', 'a')
sum = 0
for i in range(6, len(lines), 4):
    sum += int(lines[i])
text = str(sum)
file.write(text)
file.close()
