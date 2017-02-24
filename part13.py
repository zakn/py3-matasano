from part9 import pkcs, unpkcs
from part10 import myCBC
from part11 import getkey

key = getkey(16)

def parseCookie(s):
    pairs = s.split('&')
    dat = {}
    for p in pairs:
        x = p.split('=')
        if (len(x)!=2):
            break
        dat[x[0]] = x[1]
    return dat

def profile_for(email_address):
    badChars = '&='
    email = email_address
    for b in badChars:
        email = email.replace(b, '')
    encoded = 'email=%s&uid=10&role=user' % email
    return encoded

def ecrypt(cookie):
    cipher = myCBC(key, bytes(16))
    return cipher.ECBenc(pkcs(cookie.encode(), 16))

def decrypt(ciphertext):
    cipher = myCBC(key, bytes(16))
    print(cipher.ECBdec(ciphertext))
    cookie = parseCookie(unpkcs(cipher.ECBdec(ciphertext)).decode('utf-8'))
    return cookie
    
    

if __name__ == '__main__':
    c = myCBC(key, bytes(16))
    #want 12 bytes of buffer
    x = ecrypt(profile_for('muss@fuss.com'))
    till_user = x[:len(x)-16]
    #print(till_user)
    #print(c.ECBdec(till_user))

    #want block to start at 'admin'
    y = ecrypt(profile_for('0000000000admin'))
    rest = y[16:32]
    payload = till_user + rest
    #print(c.ECBdec(payload))

    print(decrypt(payload))



    #single out the '=admin' cyphertext at the [6:11] part of the block
    #x = ecrypt(profile_for('admin'))
    #adminbytes = x[6:11] + last5bytes
    #ready a valid block of ciphertext (with 6 bytes of buffer)
    #x = ecrypt(profile_for('nineteenbyte@dog.tv'))
    #payload = x[:len(x)-10] + adminbytes

    #print(decrypt(payload))




    #test = 'foo=bar&baz=qux&zap=zazzle'
    #print(parseCookie(test))
    '''
    x = profile_for('gaah=&&@email.com')
    y = ecrypt(x)
    print(y)
    z = decrypt(y)
    print(z)
    '''
