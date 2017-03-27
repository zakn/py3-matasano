import random
import struct
from part11 import getkey
from part28 import SHA1

gkey = getkey(random.randint(1, 80))
#gkey = b'YELLOW SUBMARINE'

def send(message):
    return (SHA1(gkey + message).digest(), message)

def pad(msg):
    l = len(msg) * 8
    msg += b'\x80'
    msg += bytes((56 - (len(msg) % 64)) % 64)
    msg += struct.pack('>Q', l)
    return msg

def check(m, digest):
    return send(m)[0] == digest


def forgeDigest(message, priordig, keylen_guess, ext):
    preForged = pad(bytes(keylen_guess) + message) + ext
    l = len(preForged)*8
    preForged = preForged[keylen_guess:]
    new_register = struct.unpack('>5I', priordig)
    forgeDig = SHA1(ext, new_register[0], new_register[1], new_register[2], new_register[3], new_register[4], l).digest()
    return (preForged, forgeDig)


def bruteForge(message, ext):
    base_mac = send(message)
    #assuming max keylen 80
    for i in range(1, 81):
        z = forgeDigest(message, base_mac[0], i, ext)
        if (check(z[0], z[1])):
            return z


if __name__=='__main__':
    txt = b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
    admin = b';admin=true'
    mac = send(txt)

    x = bruteForge(txt, admin)

    print(x)
    print(check(x[0], x[1]))

    print(SHA1(pad(gkey + txt) + admin).digest())
