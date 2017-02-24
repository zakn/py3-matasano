import base64
import random
import part11
from part10 import myCBC
from part9 import pkcs

random.seed()
cipher = myCBC(part11.getkey(16), bytes(16))

def incrypt_hard(byts):
    app = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
    plain = b''
    for i in range(0, random.randint(0, 100)):
        plain += bytes([random.randint(0, 255)])

    plain += byts
    plain += app
    c_txt = cipher.ECBenc(pkcs(plain, 16))

    return c_txt



def consecutiveCheck(byts, blocksize):
    blocks = [byts[i:i+blocksize] for i in range(0, len(byts), blocksize)]
    prev = bytes([1] * blocksize)
    for current in blocks:
        if (prev == current):
            return True
        prev = current
    return False


#indentify buffer blocks
def getBufferblock(keylen):
    buff = bytes((keylen*3)-1)
    c = incrypt_hard(buff)
    blocks = [c[i:i+keylen] for i in range(0, len(c), keylen)]
    prev = bytes(keylen)
    for k in range(1, len(blocks)):
        if (blocks[k-1] == blocks[k]):
            return blocks[k]




def getTargetlog(known, keylen):
    offset = len(known)-2
    targetlog = []
    buff = bytes((keylen*3)-1)
    buffblock = getBufferblock(keylen)

    #need to log for the (keylen) possible randomizations of the buffered ciphertext
    while (len(targetlog) < keylen):
        c = incrypt_hard(buff)
        blocks = [c[i:i+keylen] for i in range(0, len(c), keylen)]
        cipherblock = blocks[blocks.index(buffblock) + 2 + offset]
        if cipherblock not in targetlog:
            targetlog.append(cipherblock)

    return targetlog




#this works for block increments. 
def nextByte(knownCipher, knownPlain, keylen, targ): 
    buff = bytes((keylen*3)-1)
    buffblock = knownCipher[0]

    #need 16 unique ciphertexts for each guess since only one will match something in targetlog
    matchblock = b''
    for j in range(1, 256):
        guesslog = []
        guessbuff = buff + knownPlain + bytes([j])
        while (len(guesslog)<keylen):
            c = incrypt_hard(guessbuff)
            blocks = [c[i:i+keylen] for i in range(0, len(c), keylen)]
            ###
            #cipherblock_index = blocks.index(buffblock) + 2
            cipherblock = blocks[blocks.index(buffblock) + len(knownCipher)]
            
            #for l in range(len(knownCipher)-2):
             #   if (knownCipher[l+2] == cipherblock):
              #      cipherblock = blocks[cipherblock_index + 1 + l]
            ###
            if cipherblock not in guesslog:
                guesslog.append(cipherblock)
        newlog = []
        for guessblock in targ:
            if guessblock in guesslog:
                matchblock = guessblock
            else:
                if guessblock not in newlog:
                    newlog.append(guessblock)

        if (len(matchblock) > 0):
            return [knownCipher, knownPlain + bytes([j]),  matchblock, newlog]



def nextBlock(keylen, knownblocks = None, knownPlain = b''):
    if knownblocks == None:
        knownblocks = getBufferblock(keylen)
        knownblocks = [knownblocks, knownblocks]
    targetLog = getTargetlog(knownblocks, keylen)
    byteResult = [knownblocks, knownPlain]
    for h in range(keylen):
        byteResult = nextByte(byteResult[0], byteResult[1], keylen, targetLog)
        if (byteResult == None):
            return knownPlain
        targetLog = byteResult[3]
        print(byteResult[:2])
        print(cipher.ECBdec(byteResult[2]))
    newkno = knownblocks
    newkno.append(byteResult[2])
    return nextBlock(keylen, newkno, byteResult[1])

    
    
        
    
    



if __name__=='__main__':

    #find key len
    keylen = 4
    for i in range(4, 100):
        s = bytes([1]*(3*i-1))
        ctxt = incrypt_hard(s)
        #check if two consecutive blocks are the same, if so we have keylen
        if consecutiveCheck(ctxt, i):
            keylen = i
            break
                
    print(keylen)

    

    #check ecb
    current = incrypt_hard('A'.encode()*(keylen*3-1))
    part11.detection_oracle(current)



    #try nextBlock // decrypt this shit
    print (nextBlock(keylen))
    


    '''


    tlg = getTargetlog(b'', keylen)
    x = [b'', tlg]
    b = getBufferblock(keylen)
    for h in range(keylen):
        x = nextByte(x[0], b, keylen, tlg)
        tlg = x[2]
        print(x[:2])
        print(cipher.ECBdec(x[1]))'''
        

    '''
    k = b''
    b = b''
    while (b != None):
        k+=b
        b = nextByte(k, keylen)
    print(k)
    '''
        


    
        

    



