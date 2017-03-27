import random
import base64
import struct
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor



class myCTR:
    def __init__(self, key, newnonce):
        self.nonce = newnonce
        self.ctr = 0
        self.ECB = AES.new(key, AES.MODE_ECB)
        self.prior_keystream = b''
        self.blen = 16 #assuming 16 byte keylen

    def prepare_keystream(self, length):
        newstream = self.prior_keystream
        while (len(newstream) < length):
            newstream += self.ECB.encrypt(struct.pack('<QQ', self.nonce, self.ctr))
            self.ctr += 1

        self.prior_keystream = newstream[length:]
        return newstream[:length]
        

    def crypt(self, ctxt):
        l = len(ctxt)
        keystream = self.prepare_keystream(l)
        return strxor(ctxt, keystream)        


if __name__=='__main__':

    ctxt = base64.b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
    exkey = b'YELLOW SUBMARINE'
    ciph = myCTR(exkey, 0)

    print(ciph.crypt(ctxt))

    

