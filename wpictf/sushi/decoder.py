import pprint
from collections import defaultdict

def buildSegments(str):
    segs = str.split('z')
    return [seg.lower() for seg in segs][:-1]

def buildBasicSegs(segs):

    result = []
    for seg in segs:
        d = {k:0 for k in seg}
        for k in seg:
            d[k] += 1
        result += [[k for k, v in d.items() if v % 2 is 1]]

    return result

def printPixels(segs):
    for seg in segs:
        pixel = [[' ' for i in range(0, 5)] for j in range(0, 5)]
        for ch in seg:
            idx = ord(ch) - ord('a')
            pixel[int(idx/5)][idx%5] = 'x'
        pixel = [''.join(row) for row in pixel]

        for row in pixel:
            print(row)
        print()

def readFromFile(name="encoded.txt"):
    f = open(name, 'r')
    return str(f.read())

def decodeString():
    input = readFromFile()
    segs = buildSegments(input)
    segs = buildBasicSegs(segs)
    printPixels(segs)

def main():
    decodeString()

if __name__ == "__main__":
    main()

