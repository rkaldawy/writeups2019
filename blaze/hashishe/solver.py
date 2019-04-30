#!/usr/bin/env python2

from pwn import *
from gmpy2 import *
from bytestonum import hexint, numpily

c = remote('chal.420blaze.in', 42003)

d = c.recvuntil('encrypt:\n')

p = int(d.split('p=')[1].split('\n')[0])
g = int(d.split('g=')[1].split('\n')[0])
y = int(d.split('y=')[1].split('\n')[0])

c1 = int(d.split('c1=')[1].split('\n')[0])
target = int(d.split('c2=')[1].split('\n')[0])

#m_str = b'abcd'
m_str = b'a'
m_numeric = hexint(m_str)
print m_numeric

c.send(m_str + '\n')
d = c.recvall()

known = int(d.split('C2=')[1].split('\n')[0])

m_inv = invert(m_numeric, p)
secret = (m_inv * known) % p
secret_inv = invert(secret, p)

flag_numeric = secret_inv * target % p
print(bytes(flag_numeric))
