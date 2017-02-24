import base64
import random
import part11
from part10 import myCBC
from part9 import pkcs

random.seed()
cipher = myCBC(part11.getkey(16), bytes(16))

def incrypt(byts):
    app = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")

    plain = byts
    plain += app
    c_txt = cipher.ECBenc(pkcs(plain, 16))

    return c_txt



def nextByte(known, keylen):
    buff = bytes(keylen - 1 - (len(known) % keylen))
    log = {}
    for i in range(256):
        crypted = incrypt(buff + known + bytes([i]))
        log[crypted[:len(buff+known)+1]] = i
    crypted = incrypt(buff)
    unknown = crypted[:len(buff+known)+1]
    if unknown in log:
        return bytes([log[unknown]])
    return None




if __name__=='__main__':

    #find key len
    s = b''
    prev = bytes(3)
    keylen = 0
    while True:
        s+='A'.encode()
        current = incrypt(s)
        if (current[:3] == prev):
            break
        prev = current[:3]
        keylen +=1

    print(keylen)

    #check ecb
    current = incrypt('A'.encode()*keylen*2)
    part11.detection_oracle(current)

    k = b''
    b = b''
    while (b != None):
        k+=b
        b = nextByte(k, keylen)
    print(k)
        


    
        
    
    

    '''

    x = open('ice.txt', 'r')
    s = ''
    for char in x:
        if char!='\\':
            s+=char
    '''

'''
    while True:
        s = input("string to be encrypted: ")
        print(incrypt(s))'''
        

    



