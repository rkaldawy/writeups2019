#!/usr/bin/env python2

from pwn import *
import numpy as np

def sub_cipher(conn):
    def generate_mapping(conn):
        m = {}
        t = "".join([chr(pt) for pt in range(ord('a'), ord('z') + 1)])
        conn.recvuntil('Give me text:\n', drop=True)
        conn.send(t + '\n')
        enc = conn.recvline().split("is ")[1].strip().split(' ')
        for idx, ch in enumerate(enc):
            m[ch] = chr(idx + ord('a'))
        return m

    m = generate_mapping(conn)
    for i in range(0, 50):
        _sub_cipher(conn, m)

def _sub_cipher(conn, m):
    conn.recvuntil('Decrypt ')
    ct = conn.recvline().strip().split(' ')
    pt = "".join([m[ch] for ch in ct])
    #print("Decrypted message is: " + pt)
    conn.send(pt + '\n')

def mod_cipher(conn, r):
    def generate_mapping(conn, r):
        m = [{} for i in range(0, r)]
        t = "".join([chr(pt) * r for pt in range(ord('a'), ord('z') + 1)])
        conn.recvuntil('Give me text:\n', drop=True)
        conn.send(t + '\n')
        enc = conn.recvline().split("is ")[1].strip().split(' ')
        for idx, ch in enumerate(enc):
            m[idx % r][ch] = chr(int(idx / r) + ord('a'))
        return m

    m = generate_mapping(conn, r)
    for i in range(0, 50):
        _mod_cipher(conn, m, r)

def _mod_cipher(conn, m, r):
    conn.recvuntil('Decrypt ')
    ct = conn.recvline().strip().split(' ')
    pt = "".join([m[idx % r][ch] for idx, ch in enumerate(ct)])
    #print("Decrypted message is: " + pt)
    conn.send(pt + '\n')

def swap_cipher(conn):
    def generate_mapping(conn):
        m = {}
        t = "".join([chr(pt)*4 for pt in range(ord('a'), ord('z') + 1)])
        conn.recvuntil('Give me text:\n', drop=True)
        conn.send(t + '\n')
        enc = conn.recvline().split("is ")[1].strip().split(' ')
        for i in range(0, 26):
            m[enc[i]] = chr(i + ord('a'))
        return m

    m = generate_mapping(conn)
    for i in range(0, 50):
        _swap_cipher(conn, m)

def _swap_cipher(conn, m):
    conn.recvuntil('Decrypt ')
    ct = conn.recvline().strip().split(' ')
    ct = np.array_split(ct, 4)
    c = np.empty((ct[0].size + ct[1].size + ct[2].size + ct[3].size), dtype=ct[0].dtype)
    c[0::4] = ct[0]
    c[1::4] = ct[1]
    c[2::4] = ct[2]
    c[3::4] = ct[3]
    ct = c

    pt = "".join([m[ch] for ch in ct])
    #print("Decrypted message is: " + pt)
    conn.send(pt + '\n')

conn = remote('chal.tuctf.com', '30102')

#The first 5 levels use a substitution cipher
for i in range(0, 5):
    print("Level " + str(i))
    sub_cipher(conn)

print("Level 5")
mod_cipher(conn, 8)

print("Level 6")
swap_cipher(conn)

print("Level 7")
sub_cipher(conn)

print("Level 8")
mod_cipher(conn, 7)

print("Level 9")
swap_cipher(conn)

conn.interactive()
