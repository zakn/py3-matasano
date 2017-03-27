import random
import base64
from part18 import myCTR
from Crypto.Cipher import AES


globalkey = bytes([random.randint(0, 255) for i in range(16)])
globalnonce = random.randint(0, 2**16)


def incrypt(key, nonce):
    txt = base64.b64decode(open('25.txt').read())
    ecbkey = b'YELLOW SUBMARINE'
    c = AES.new(ecbkey, AES.MODE_ECB)
    txt = c.decrypt(txt)
    cipher = myCTR(globalkey, globalnonce)
    return cipher.crypt(txt)


def edit(ctxt, offset, newtxt):
    decipher = myCTR(globalkey, globalnonce)
    newplain = decipher.crypt(ctxt)[:offset]
    newplain += newtxt
    return myCTR(globalkey, globalnonce).crypt(newplain)



def seekbreak(ctxt):
    return edit(ctxt, 0, ctxt)



if __name__ == '__main__':
    x = incrypt(globalkey, globalnonce)

    print(seekbreak(x))

    '''
    y = edit(x, len(x)-4, b'yoo')
    cc = myCTR(globalkey, globalnonce)
    print(cc.crypt(y))
    '''
