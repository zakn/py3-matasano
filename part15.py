import binascii
from part9 import pkcs


#strips the buffer bytes so it look nice :D
def pkcs_validate(byts):
    s = byts
    x = int(byts[len(byts)-1])
    if (x > 16 or x < 1):
        raise ValueError('Invalid PKCS#7 Padding!')
    for i in range(x):
        y = int(s[len(s)-1])
        s = s[:len(s)-1]
        if (y != x):
            raise ValueError('Invalid PKCS#7 Padding!')
    return s





if __name__=='__main__':


    x = bytearray('ICE ICE BABY', 'utf-8')
    err1 = bytearray('ICE ICE BABY\x05\x05\x05\x05', 'utf-8')
    err2 = bytearray('ICE ICE BABY\x01\x02\x03\x04', 'utf-8')

    z = pkcs(x, 16)
    print(z)

    y = pkcs_validate(z)
    print(y)

    #print(pkcs_validate(err1))
    #print(pkcs_validate(err2))
