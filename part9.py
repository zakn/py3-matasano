import part1
import binascii



def pkcs(byts, blocksize):
    b = blocksize - (len(byts) % blocksize)
    result = bytearray(byts)
    result += bytearray([b for i in range(b)])
    return result

#strips the buffer bytes so it look nice :D
def unpkcs(byts):
    x = int(byts[len(byts)-1])
    if (x > 16):
        x = 0
    return byts[:len(byts) - x]





if __name__=='__main__':


    x = b'YELLOW SUBMARINE'

    print(x)

    for i in x:
        print(i)

    z = pkcs(x, 20)
    print(z)

    y = unpkcs(z)
    print(y)
