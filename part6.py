import base64
import itertools
import part3
import part5
import binascii


def hamming(byts1, byts2):
    count = 0
    for i in range(len(byts1)):
        count += bin(byts1[i] ^ byts2[i]).count('1')
        
    return count



#normalizes hamming distance on all 6 2-combinations of first 4 keylen blocks
#gives the correct key length in the challenge
def veryNormalHamming(byts, keylen):
    blocks = [byts[i:i+keylen] for i in range(0, len(byts), keylen)][0:4]
    shuffle_pairs = list(itertools.combinations(blocks, 2))
    scores = []
    
    for pair in shuffle_pairs:
        scores.append(hamming(pair[0], pair[1])/float(len(pair[0])))
        
    return sum(scores)/float(6)




def decryptRepKey(byts, keylen):
    blocks = [byts[i:i+keylen] for i in range(0, len(byts), keylen)]
    transposed = list(itertools.zip_longest(*blocks, fillvalue=0))
    key = b''
    
    for singleKeyCiphertext in transposed:
        key += bytes([part3.singleByteXOR(singleKeyCiphertext)[0]])
        
    return key
    



if __name__=='__main__':

    '''
    x = b'this is a test'
    y = b'wokka wokka!!!'
    print (hamming(x, y))
    '''

    #x = base64.b64decode(open('6.txt', 'r').read())
    x = binascii.unhexlify(open('exam.txt', 'r').read())

    keysize_guess = min(range(1, 6), key = lambda y: veryNormalHamming(x, y))

    print (keysize_guess)

    the_key = decryptRepKey(x, keysize_guess)

    print(the_key)

    plaintext = part5.repKeyXOR(x, the_key)

    print(plaintext)

    





