import binascii
import itertools


#returns the line number(s) where ECB is used
def detectECB(file):
    line_count = 1
    hits = []
    for line in file:
        if (line[-1] == '\n'):
            s = line[:-1]
        else:
            s = line
        bits = binascii.unhexlify(s)
        if (isECB(bits) > 0):
            hits.append(line_count)
        line_count += 1
    return hits
            


#takes a byte string as input and checks if any of its 16 byte blocks are equal
def isECB(s):
    k = 16
    scr = 0
    blocks = [s[i:i+k] for i in range(0, len(s), k)]
    block_pairs = itertools.combinations(blocks, 2)
    for pair in block_pairs:
        if(pair[0] == pair[1]):
            scr += 1
    return scr
        
    


if __name__ == '__main__':

    x = open('8.txt', 'r')
    ans = detectECB(x)

    print(ans)
