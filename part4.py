import binascii
import part3


def findFileXOR(file):
    decoded_lines = []
    for line in file:
        if (line[-1] == '\n'):
            decoded_lines.append(binascii.unhexlify(line[:-1]))
        else:
            decoded_lines.append(binascii.unhexlify(line))

    xoredLines = [part3.singleByteXOR(line) for line in decoded_lines]
    def localKey(num):
        return part3.score(xoredLines[num][1])

    maxIndex = max(range(len(xoredLines)), key = localKey)
            
    return (maxIndex + 1, xoredLines[maxIndex])



if __name__ == '__main__':
    enc = open('exam.txt', 'r')
    ans = findFileXOR(enc)
    print(ans)
    print(ans[1][2].decode('utf-8'))
    





