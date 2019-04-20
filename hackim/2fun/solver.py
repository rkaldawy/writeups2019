import sys

t1 = set()
t2 = set()

with open("first.txt", "r") as f:
    for line in f:
        #print(line.split(" ")[3])
        t1.add(line.split(" ")[3])

with open("second.txt", "r") as f:
    for line in f:
        t2.add(line.split(" ")[3]) 

collision = t1.intersection(t2).pop().split('\n')[0]
print(collision)

key = []
with open("first.txt", "r") as f:
    for line in f:
        if line.split(" ")[3].split("\n")[0] == collision:
            key += [int(x) for x in line.split(" ")[0:3]]
            
with open("second.txt", "r") as f:
    for line in f:
        if line.split(" ")[3].split("\n")[0] == collision:
            key += [int(x) for x in line.split(" ")[0:3]]

key = "".join([chr(val) for val in key])

from 2fun.py import toofun_decryptor

flag = unhexlify(b'04b34e5af4a1f5260f6043b8b9abb4f8')
print(toofun_decryptor(key, flag))





