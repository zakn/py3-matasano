import binascii
from part9 import pkcs
from part10 import myCBC
from part11 import getkey

gkey = getkey(16)
cipher = myCBC(gkey, gkey)

def cbc_incrypt(user_in):
    badchars = '=;'
    inp = user_in
    for b in badchars:
        inp = inp.replace(b, '')
    plain = "comment1=cooking%20MCs;userdata="
    plain += inp
    plain += ";comment2=%20like%20a%20pound%20of%20bacon"
    plain = pkcs(plain.encode(), 16)
    return bytes(cipher.CBCenc(plain))


def compliance(ctxt):
    ptxt = cipher.CBCdec(ctxt)
    #ptxt += b'\xfa'
    for byt in ptxt:
        if byt > 127:
            #could raise error but easier to return bytes for automation
            #raise ValueError(ptxt)
            return ('error', ptxt)
    return 'success'
            


def iv_attack(ctxt):
    attackertxt = ctxt[:16] + bytes(16) + ctxt[:16] + ctxt[48:]
    blocks = compliance(attackertxt)[1]
    blocks = [blocks[k:k+16] for k in range(0, len(blocks), 16)]
    print(blocks)
    return bytes([blocks[0][j] ^ blocks[2][j] for j in range(16)])



if __name__=='__main__':
    print(gkey)
    x = cbc_incrypt('')

    y = iv_attack(x)
    print(y)
