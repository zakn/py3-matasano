import random
import struct
from part11 import getkey
from md4 import MD4


#gkey = getkey(random.randint(1, 80))
gkey = b'YELLOW SUBMARINE'

def send(message):
    return (MD4(gkey + message).digest(), message)


def check(m, digest):
    return send(m)[0] == digest


def pad(msg):
    length = struct.pack('<Q', len(msg) * 8)
    result = msg + b'\x80'
    result += bytes((56 - len(result) % 64) % 64)
    result += length
    return result


def forgeDigest(message, priordig, keylen_guess, ext):
    preForged = pad(bytes(keylen_guess) + message) + ext
    l = len(preForged)*8
    preForged = preForged[keylen_guess:]
    new_register = struct.unpack('<4I', priordig)
    forgeDig = MD4(ext, new_register[0], new_register[1], new_register[2], new_register[3], l).digest()
    return (preForged, forgeDig)




if __name__=='__main__':
    txt = b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
    admin = b';admin=true'
    mac = send(txt)

    x = forgeDigest(txt, mac[0], 16, admin)

    test = pad(gkey + txt) + admin
    print('md4')
    print(MD4(test).digest())

    print(check(x[0], x[1]))

    #print(x[0])
    #print(send(x[0])[1])
    

