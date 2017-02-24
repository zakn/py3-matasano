import random
import base64
from part9 import pkcs
from part10 import myCBC
from part15 import pkcs_validate


rand_str = [b'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
            b'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
            b'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
            b'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
            b'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
            b'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
            b'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
            b'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
            b'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
            b'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93']


random.seed()

def getkey(length):
    return bytes([random.randint(0, 255) for i in range(length)])

key = getkey(16)
IV = getkey(16)
cipher = myCBC(key, IV)


def incrypt_rand():
    chosen = pkcs(base64.b64decode(rand_str[random.randint(0, 9)]), 16)
    print(chosen)
    return cipher.CBCenc(chosen)

def pad_oracle(ctxt):
    plain = cipher.CBCdec(ctxt)
    return pkcs_validate(plain)



def pkcs_attack(ctxt, known):
    blocks = [ctxt[k:k+16] for k in range(0, len(ctxt), 16)]
    prevblock = blocks[len(blocks)-2]
    
    for i in range(256):
        prevblock = blocks[len(blocks)-2]
        last_byte = prevblock[15]

        #dont want to use the plaintext byte
        if (i != last_byte):
            imposterblock = bytearray(15) + bytearray([i])
            payload = ctxt[:-32] + imposterblock + ctxt[-16:]
            try:
                pad_oracle(payload)
                flips = i ^ last_byte
                byte_val = flips ^ 1
                print(flips)
                print(byte_val)
            except ValueError:
                guess = ctxt
    
        
                
    
    
    
    


if __name__ == '__main__':

    ciphertxt = incrypt_rand()
    ora = pad_oracle(ciphertxt)


    print('last byte of key is: %d' % key[len(key)-1])
    known = pkcs_attack(ciphertxt, b'')
    last = ciphertxt[len(ciphertxt)-1]



    '''
    for i in range(10):
        key = getkey(16)
        cipher = incrypt_rand(key)
    '''

    
