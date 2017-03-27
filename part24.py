import random
import time
from part21 import myMT

bit16_key = 51116

class streamMT:

    def __init__(self, seedkey):
        self.key = seedkey


    def encrypt(self, plain):
        ctxt = b''
        rng = myMT(self.key)
        for byt in plain:
            ctxt = ctxt + bytes([byt ^ rng.randbits(8)])
        return ctxt

    def decrypt(self, crypted):
        ptxt = b''
        rng = myMT(self.key)
        for b in crypted:
            ptxt = ptxt + bytes([b ^ rng.randbits(8)])
        return ptxt
    


def incrypt(p):
    newplain = b''
    for i in range(random.randint(5, 20)):
        newplain += bytes([random.randint(0,255)])
    newplain += p
    return streamMT(bit16_key).encrypt(newplain)


def find_seed(Acipher):
    seed_guess = 0
    for k in range(65536):
        if (streamMT(k).decrypt(Acipher)[-14:] == b'AAAAAAAAAAAAAA'):
            seed_guess = k
            break
    return seed_guess


def reset_token():
    timeseed = int(time.time())
    print(timeseed)
    plain = b'A' * random.randint(15, 35)
    cipher = streamMT(timeseed)
    return cipher.encrypt(plain)


def token_test(ctxt):
    basetime = int(time.time())
    print(basetime)
    guessplain = b'A' * len(ctxt)
    for second in range(5):
        timeseed = basetime - second
        c = streamMT(timeseed)
        if (c.decrypt(ctxt) == guessplain):
            return True



if __name__ == '__main__':

    plain = b'AAAAAAAAAAAAAA'
    oracle = incrypt(plain)
    print(oracle)
    print(streamMT(bit16_key).decrypt(oracle))

    tok = reset_token()
    time.sleep(2)
    print(token_test(tok))

    #this is commented because it takes a while
    #print(find_seed(oracle))


        
        
