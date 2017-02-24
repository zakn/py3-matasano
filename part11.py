import random
import base64
from part8 import isECB
from part9 import pkcs
from part10 import myCBC


random.seed()

def getkey(length):
    return bytes([random.randint(0, 255) for i in range(length)])



def encryption_oracle(byts):
    plain = bytes([random.randint(0, 255) for i in range(random.randint(5, 10))])
    plain += byts
    plain += bytes([random.randint(0, 255) for i in range(random.randint(5, 10))])
    cipher = myCBC(getkey(16), getkey(16))
    if (random.randint(0,1)):
        #CBC
        print('CBC')
        return cipher.CBCenc(pkcs(plain, 16))
    else:
        #ECB
        print('ECB')
        return cipher.ECBenc(pkcs(plain, 16))


def detection_oracle(byts):
    if (isECB(byts) > 0):
        print('its ecb')
        return 1
    else:
        print('its cbc')
        return 0



if __name__=='__main__':
    exkey = b'YELLOW SUBMARINE'
    ciphertext = base64.b64decode(open('10.txt', 'r').read())
    ciph = myCBC(exkey, bytes(16))

    plaintext = ciph.CBCdec(ciphertext)

    y = encryption_oracle(plaintext)

    detection_oracle(y)
