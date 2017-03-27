from Crypto.Util.strxor import strxor
from part18 import myCTR
from part19 import encrypt_strings
import part3
import base64
import binascii

#key randomized once
key = b'\x11\xf4\xdec\xd25G\x17\x1a\xe9\xc0i\x8b\x15\x0fp'

#for guessing
expected_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,-///'

'''
def encrypt_strings(str_array):
    result = []
    for s in str_array:
        cipher = myCTR(key, 0)
        result.append(cipher.crypt(base64.b64decode(s)))
    return result
'''


def find_shortest(str_array):
    result = 5000
    for s in str_array:
        if (len(s) < result):
            result = len(s)
    return result


def trunc(str_array):
    shortest = find_shortest(str_array)
    result = []
    for s in str_array:
        result.append(s[:shortest])
    return result


def decrypt_repeated_stream(str_array):
    transposed = list(zip(*str_array))
    key = b''
    for samekeyChars in transposed:
        key += bytes([part3.singleByteXOR(samekeyChars)[0]])
    return key


def override(oldkey, indexchange, expchar, cipherbyte):
    newkey = b''
    for i in range(len(oldkey)):
        if (i == indexchange):
            newkey += bytes([ord(expchar) ^ cipherbyte])
        else:
            newkey += bytes([oldkey[i]])
    return newkey


def guess_next_keybytes(oldkey, ciphertext, guess):
    nextbytes = bytes([ord(guess[i]) ^ ciphertext[len(oldkey)+i] for i in range(len(guess))])
    return oldkey + nextbytes


if __name__ == '__main__':

    file = open('20.txt', 'r')
    line = file.readline()
    lines = []
    while (line != ''):
        lines.append(line)
        line = file.readline()

    ctxt = encrypt_strings(lines)

    t_cipher = trunc(ctxt)

    #prepare full keystream by guessing at the rest of words piecemeal
    keystream = decrypt_repeated_stream(t_cipher)
    keystream = override(keystream, 0, 'I', t_cipher[0][0])
    keystream = guess_next_keybytes(keystream, ctxt[1], 'ike light')
    keystream = guess_next_keybytes(keystream, ctxt[3], ' ')
    keystream = guess_next_keybytes(keystream, ctxt[5], 'n')
    keystream = guess_next_keybytes(keystream, ctxt[1], 'n')
    keystream = guess_next_keybytes(keystream, ctxt[6], 'lty')
    keystream = guess_next_keybytes(keystream, ctxt[34], 'tation')
    keystream = guess_next_keybytes(keystream, ctxt[30], 'ery')
    keystream = guess_next_keybytes(keystream, ctxt[39], 'ent')
    keystream = guess_next_keybytes(keystream, ctxt[47], 'st')
    keystream = guess_next_keybytes(keystream, ctxt[52], 'me')
    keystream = guess_next_keybytes(keystream, ctxt[44], 'dents')
    keystream = guess_next_keybytes(keystream, ctxt[35], 'ury')
    keystream = guess_next_keybytes(keystream, ctxt[4], 'uick')
    keystream = guess_next_keybytes(keystream, ctxt[12], 'nk')
    keystream = guess_next_keybytes(keystream, ctxt[26], 've')
    keystream = guess_next_keybytes(keystream, ctxt[21], ' peace')
    keystream = guess_next_keybytes(keystream, ctxt[26], 'hole scenery')

    for j in range(len(ctxt)):
        if (len(keystream) < len(ctxt[j])):
            maybeplain = bytes([ctxt[j][k] ^ keystream[k] for k in range(len(keystream))])
        else:
            maybeplain = bytes([ctxt[j][k] ^ keystream[k] for k in range(len(ctxt[j]))])
        print(maybeplain)



    

    




