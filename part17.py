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

def pad_oracle(ctxt, iv):
    plain = cipher.CBCdec(ctxt, iv)
    return pkcs_validate(plain)



def find_next_byte(ctxt, backfill, iv):
    bpos = len(backfill) + 1
    prevblock = ctxt[-32:-16]
    newbuff = bytearray(b'')
    ivec = iv

    for b in backfill:
        newbuff = newbuff + bytearray([b^bpos])

    for i in range(256):

        if (len(prevblock) >= 16):
            last_byte = prevblock[-bpos]
            imposterblock = bytearray(16-bpos) + bytearray([i]) + newbuff
            payload = ctxt[:-32] + imposterblock + ctxt[-16:]

        #gotta modify the IV
        else:
            last_byte = iv[-bpos]
            ivec = bytearray(16-bpos) + bytearray([i]) + newbuff
            payload = ctxt
            
        try:
            pad_oracle(payload, ivec)
            store = i ^ bpos
            newfill = bytearray([store]) + backfill
            byte_val = store ^ last_byte
        except ValueError:
            guess = ctxt

    return (bytearray([byte_val]), newfill)




def find_next_block(ctxt, known, iv):
    result = known
    step = find_next_byte(ctxt, b'', iv)
    result = step[0] + result
    for h in range(15):
        step = find_next_byte(ctxt, step[1], iv)
        result = step[0] + result
    return result
    
    
    
def pkcs_attack(ctxt, iv):
    plain = find_next_block(ctxt, b'', iv)
    for j in range(1, len(ctxt) // 16):
        plain = find_next_block(ctxt[:-(j*16)], plain, iv)
    return plain
                
    
    
    
    


if __name__ == '__main__':

    ciphertxt = incrypt_rand()
    ora = pad_oracle(ciphertxt, IV)

    result = pkcs_attack(ciphertxt, IV)
    print(result)



    '''
    for i in range(10):
        key = getkey(16)
        cipher = incrypt_rand(key)
    '''

    
