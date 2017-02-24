import binascii
from part9 import pkcs
from part10 import myCBC
from part11 import getkey

'''
idea here is to produce have user input something like '55555XadminXtrue'
where 55555 is buffer to make this a full block

with this ciphertext, flip bits randomly in the 6th (21st) and 12th (27th) byte
positions in the second block until the first decrypts to ';' and the second
decrypts to '=' O(256^2) not too bad...
'''

cipher = myCBC(getkey(16), bytes(16))

def cbc_incrypt(user_in):
    badchars = '=;'
    inp = user_in
    for b in badchars:
        inp = inp.replace(b, '')
    plain = "comment1=cooking%20MCs;userdata="
    plain += inp
    plain += ";comment2=%20like%20a%20pound%20of%20bacon"
    plain = pkcs(plain.encode(), 16)
    return cipher.CBCenc(plain)


def admin_check(ciphertxt):
    plain = str(cipher.CBCdec(ciphertxt))
    pairs = plain.split(';')
    if 'admin=true' in pairs:
        return True
    else:
        return False



def breakit():
    uin = '55555XadminXtrue'
    ciphertext = cbc_incrypt(uin)
    for i in range(256):
        guesstext = ciphertext[:21] + bytes([i]) + ciphertext[22:]
        #guesstext = ciphertext[:7] + bytes([i]) + ciphertext[8:]
        for k in range(256):
            guesstext = guesstext[:27] + bytes([k]) + guesstext[28:]
            #guesstext = guesstext[:13] + bytes([k]) + guesstext[14:]
            result = admin_check(guesstext)
            if (result == True): #found the two byte flips i need
                return [guesstext, i, k]
    




if __name__=='__main__':


    print(breakit())
    
    '''
    x = 'admin=true'
    y = cbc_incrypt(x)
    print(y)
    z = admin_check(y)
    print(z)
    '''
    
