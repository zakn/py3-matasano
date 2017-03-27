import binascii
import random
from part18 import myCTR
from part11 import getkey


#for testing purposes have fixed key
#gkey = b'\x14\xad]R\xe5\xa09\xfe\x18\x99\x15\xab\xa5\x90W:'
#gnonce = 6892

gkey = getkey(16)
gnonce = random.randint(0, 2**16)

def ctr_incrypt(user_in):
    badchars = '=;'
    inp = user_in
    cipher = myCTR(gkey, gnonce)
    for b in badchars:
        inp = inp.replace(b, '')
    plain = "comment1=cooking%20MCs;userdata="
    plain += inp
    plain += ";comment2=%20like%20a%20pound%20of%20bacon"
    plain = plain.encode()
    return cipher.crypt(plain)


def admin_check(ciphertxt):
    cipher = myCTR(gkey, gnonce)
    plain = str(cipher.crypt(ciphertxt))
    pairs = plain.split(';')
    if 'admin=true' in pairs:
        return True
    else:
        return False


def bitflips():
    base_input = 'datXadminXtrue'
    # X's at 35 and 41 in ciphertext
    ctxt = ctr_incrypt(base_input)
    for i in range(256):
        guess = ctxt[:35] + bytes([i]) + ctxt[36:]
        for k in range(256):
            guess = guess[:41] + bytes([k]) + guess[42:]
            if (admin_check(guess)):
                return [guess, i, k]



if __name__=='__main__':
    x = bitflips()
    print(x)
