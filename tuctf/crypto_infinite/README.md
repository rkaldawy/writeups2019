# Crypto Infinite - Cryptography - 500 Points

I wanted to do a brief writeup of this challenge to document some of my work for the CTF. Arguably, this challenge should be a misc.

## Challenge Description:

Unfortunately, I don't have access to the original challenge prompt. However, it directs to a service at *chal.tuctf.com* on port *30102*.

## Lookin' at it

Upon connecting to the service, we are greeted with a prompt that allows us to encrypt a single string. Then we have to decrypt a string using the same encryption scheme. The challenge tells us that we are at Level 0 - we probably will be doing this a few times. The first thing I noticed is that each character of the plaintext maps to exactly one character of ciphertext. Going off of that, I began connecting to the service repeatedly to try encrypting different strings. A few things were immediately apparent:

* There is a one to one mapping between the alphabet and ciphertext characters
* The plaintext characters can only be the uppercase alphabet
* The cipher does not change upon subsequent connections

At this point my strategy is straigt-forward: first, I will use my one free encryption to learn the ciphertext mapping for the entire alphabet. Once I know that mapping, I can simply reverse it to perform the necessary decryptions.

As it turns out, there are 10 levels in this challenge. Each level will be described below.

### Levels 0-4

To learn the ciphertext mapping for the entire alphabet, we simply need to encrypt the entire alphabet, using the string *abcdefghijklmnopqrstuvwxyz*. This mapping can be used to run the decryption for the first 5 levels.

### Level 5

Level 5 uses a slightly different cipher from the previous levels. Each letter's ciphertext output will vary based on its _i mod 8_th position in the string. Therefore, each letter maps to eight ciphertext characters. To get these characters, I encrypted a string which had each character eight times, i.e. "a\*8 b\*8 c\*8...". With the entire space mapped out, the decryptions are again possible.


### Level 6

Level 6 again uses a different cipher from the previous levels. The Level 6 cipher takes a string, parses it into subsequent chunks of four characters, and then interleaves those chunks. For example, the string *abcd|efgh* would become *ae|bf|cg|dh*. Thus, to get the letter to ciphertext mapping, I encrypted a string which had each letter four times, i.e. "a\*4 b\*4 c\*4...", and I examined only the first 26 symbols, which correspond to the alphabet. Using some useful numpy calls to simplify inverting the encryption scheme, I was able to again decrypt the section.

### Level 7

This is a copy of Levels 0-4.

### Level 8

This is a copy of Level 5, except that the letter's ciphertext output will vary based on its *i mod 7*th position in the string.

### Level 9

This is a copy of Level 6.

After passing this level, the service presents us with the flag.

## Conclusions

This really wasn't much of a crypto challenge; it was more of a Python (and specifically pwntools) shittest. I think this would have been better as a medium level misc challenge. With that being said, it was fun to figure out the ciphers were for each level. The probe.py script is what I used to solve the challenge.
