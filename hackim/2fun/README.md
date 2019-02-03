# 2FUN Cryto Challenge

## Challenge Description:

We are given a python script which is executing some sort of primitive-looking block cipher. The cipher gets applied twice to the plaintext, each time with a different key. We are also given a plaintext/ciphertext pair, and the flag ciphertext. We need to find the key, and use it to decrypt the flag ciphertext. The challenge hint is a comment that doubling the key size stops brute force attacks, which definitely points us to the right direction. 

## Lookin' at it

After poking a bit at common block cipher attacks, I realized that this encryption scheme suffers from the same weakness as 2-DES, namely the MITM attack. The following function is key:

'''
def toofun(key, pt):
    assert len(key) == 2 * KEY_LENGTH
    key1 = key[:KEY_LENGTH]
    key2 = key[KEY_LENGTH:]

    ct1 = unhexlify(fun(key1, pt))
    ct2 = fun(key2, ct1)

    return ct2

'''

Here, the designer assumed that by applying the same `fun` encryption scheme a second time with a different key, the cipher would be reslilient to bruteforcing. In actuallity, this scheme is no harder to bruteforce than a single layer of the `fun` scheme.

We can say that for a ciphertext *C*, plaintext* P*, keys *k1* and *k2*, and encryption scheme *enc*,

C = enc(k2, enc(k1, P))

It follows that:

dec(k2, C) = enc(k1, P)

Knowing this, one could take the following steps to bruteforce the keys given a plaintext/ciphertext pair (c, p):

1. Find the encryption of p to the intermediate state between the two layers for ALL possible keys. This costs 2^n tries, where n is thee keysize in bits.
2. Find the decryption of c to the intermediate state between the two layers for ALL possible keys. This costs 2^n tries, where n is the keysize in bits.
3. Find the value shared between the two sets generated above; the keys associated with the valuee in each set are the key for that respective round of encryption/decryption.

As you can see, this is not much harder than bruteforcing a sinle round of the encryption scheme. Since the keys space is just 24 bits, this should be a feasible way to break the system.

### What to do ###

Now that we have some understanding about how to beat the challenge, what are the steps to take? I outline the following:

1. Design a decryptor for the cipher. Since the cipher seems like a Fiestel network, this shouldnt be too tricky.
2. Run the bruteforcers, and build the two sets.
3. Find the intersection between the sets, and leak the key
4. Run our decryptor on the encrypted flag with our new key


## Building the Decryptor

This encryption scheme uses xor rounds, with an S-box and permutation within each round. There are 16 rounds in total. To build our decryption function, all we need to do is reverse the permutation and S-box mechanisms, and then reverse the order of operations in each round. 

Building the inverted S-box and permutation table is not too difficult. The following code sufficees to invert the permutation table:

'''
def reverse_p():
    _p = [0 for i in range(len(p))]
    for idx, elt in enumerate(p):
        _p[elt] = idx
    print(_p)
'''

A similar function was used to swap the inputs and outputs to the S-box. 

Once the inverted tables were generated, the decryption scheme simply reversed the order that the components are applied, over 16 rounds. The fun decryptor is shown below:

'''
def fun_decryptor(key, ct):
    ct = bytearray(ct)
    key = bytearray(unhexlify(md5(key).hexdigest()))
    for _ in range(ROUND_COUNT):
        temp = bytearray(BLOCK_LENGTH)
        for i in range(BLOCK_LENGTH):
            temp[i] = ct[p_rev[i]]
        for i in range(BLOCK_LENGTH):
            ct[i] = sbox_rev[temp[i]]
        ct = xor(ct, key)
    return hexlify(ct)

'''

I also quickly wrote up the two-round deecryptor for the final step:

'''
def toofun_decryptor(key, ct):
    assert len(key) == 2 * KEY_LENGTH
    key1 = key[:KEY_LENGTH]
    key2 = key[KEY_LENGTH:]

    ct1 = unhexlify(fun_decryptor(key2, ct))
    pt = unhexlify(fun_decryptor(key1, ct1))

    return pt
'''

## Bruteforcing the two sets ##

With my decryptor finished, I needeed to bruteforce my two sets. The first one would hold the encryption of the sample plaintext with all possible first-time keys, while the second one would hold the decryption of the ciphertext with all possible second-time keys. I decided to write each set into a file, where each line would have a key and its associateed intermediate output. The following produced my sets:

'''
def bruteforce_collision():
    pt = b"16 bit plaintext"
    ct = unhexlify(b'0467a52afa8f15cfb8f0ea40365a6692')
    print(pt)

    with open("first.txt", "w+") as f:
        for i in range (0, 256):
            for j in range (0, 256):
                for k in range (0, 256):
                    key = chr(i) + chr(j) + chr(k)
                    f.write(str(i) + " " + str(j) + " " + str(k) + " " + fun(key, pt) + "\n")

    with open("second.txt", "w+") as f:
        for i in range (0, 128):
            for j in range (0, 128):
                for k in range (0, 128):
                    key = chr(i) + chr(j) + chr(k)
                    f.write(str(i) + " " + str(j) + " " + str(k) + " " + fun_decryptor(key, ct) + "\n")
'''

This took around 25 minutes for me to run. When finished, I had two files, each which had one of my sets!

## Finding a collision and decrypting the flag##

To find the intermediate entry produced with the correct keys, I needed to find the intersection between my two generated sets. Luckily, Python has a library which finds set intersections very quickly. The following code in my solver finds that intersection, and retroactively discovers the keys associated with that intersection, concatenated into a single 48-bit key:

'''
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

#find the keys associated with that intersection, back in the files
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
'''

With the key discovered, all I had to do was apply my `toofun` decryption function, shown above, on the encrypted flag, and retrieve the plaintext flag!

## Conclusions ##

I had a lot of fun doing this challenge. I don't often see creative block cipher challenges, and this felt like a breath of fresh air from the usual RSA misconfiguration challenge. Thanks to HackIM for making the chal!:
