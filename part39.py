import random
import binascii
import pgen

#to be made bigger at some point, also removed any primes where (p-1) % 3 = 0
decent_primes = [196613, 1572869, 3145739, 12582917, 50331653,
                 100663319, 402653189, 805306457, 1610612741]

#returns k different primes from my list
def bs_randprimes(k):
    result = []
    while (len(result) < k):
        new = decent_primes[random.randint(0, len(decent_primes)-1)]
        if new in result:
            new = 0
        else:
            result.append(new)
    return result


def randprimes_smart(bitlen, numprimes, expected_e):
    res = []
    while (len(res) < numprimes):
        p = pgen.generate_prime(bitlen)
        if ((p-1)%expected_e != 0):
            res.append(p)
    return res

# aka: extended euclidean alg.. really want p to be prime
def invmod(a, p):
    u, v = (a, p)
    if (u == 0):
        return 0
    x1, x2 = (1, 0)
    while (u != 1):
        q = v//u
        r = v - (q*u)
        x = x2 - q*x1
        v, u, x2, x1 = (u, r, x1, x)
    if (x1 < 0):
        x1 = p + x1
    return x1

def plain_toint(byts):
    return int.from_bytes(byts, byteorder='big')

def int_toplain(n, exp_len = None):
    if exp_len == None:
        return n.to_bytes((n.bit_length() + 7) // 8, byteorder='big')
    else:
        byts = n.to_bytes((n.bit_length() + 7) // 8, byteorder='big')
        byts = b'\x00'*(exp_len - len(byts)) + byts
        return byts

class myRSA:

    def __init__(self, keylen, override=None):
        #self.p, self.q = bs_randprimes(2)
        if override == None:
            self.p, self.q = randprimes_smart(keylen, 2, 3)
        else:
            self.p, self.q = override
        self.n = self.p*self.q
        self.et = (self.p-1)*(self.q-1)
        self.e = 3
        self.d = invmod(self.e, self.et)

    def getPublic(self):
        return [self.e, self.n]

    def getkeys(self):
        return self.e, self.d, self.n

    def decrypt(self, ctxt):
        return pow(ctxt, self.d, self.n)

    def byte_dec(self, ctxt):
        x = plain_toint(ctxt)
        return int_toplain(self.decrypt(x))

    #here ctxt is a byte string of arbitrary len
    def decrypt_long(self, ctxt):
        blocks = []
        index = 0
        while (index < len(ctxt)):
            blen = ctxt[index]
            index += 1
            blocks.append(ctxt[index:index+blen])
            index += blen
        print(blocks)
        result = []
        for k in range(len(blocks)):
            m = plain_toint(blocks[k])
            m = self.decrypt(m)
            result.append(m)
        export = b''
        for x in result:
            export += int_toplain(x)
        return export


#pkey expected [e, n] and msg is an int smaller than n
def rsa_enc(pkey, msg):
    return pow(msg, pkey[0], pkey[1])

def byte_enc(pkey, msg):
    x = plain_toint(msg)
    return rsa_enc(pkey, x)

#ptxt is supposed to be a byte string of arbitrary len, returns encrypted byte string
def encrypt_long(pkey, ptxt):
    e, n = pkey
    blen = n.bit_length() // 8
    print(blen)
    blocks = [ptxt[i:i + blen] for i in range(0, len(ptxt), blen)]
    result = []
    for k in range(len(blocks)):
        m = plain_toint(blocks[k])
        m = rsa_enc(pkey, m)
        result.append(m)
    export0 = []
    export = b''
    for x in result:
        print(len(int_toplain(x)))
        export += len(int_toplain(x)).to_bytes(1, byteorder='big')
        export0.append(int_toplain(x))
        export += int_toplain(x)
    print(export0)
    return export




if __name__ == '__main__':

    ptxt = b'heres a try!! this is gonna be a whole lotta bytes i tell you what! uuh huuuh! gonna need a big ol n to encrypt all of THIS!'
    print(len(ptxt))
    x = plain_toint(ptxt)
    rsa = myRSA(1024)

    k = rsa.getPublic()
    z = rsa_enc(k, x)

    s = rsa.decrypt(z)
    print(int_toplain(s))

    #encrypt_long test
    '''
    ptxt = b'a try!2345432 hows about that!!!!!!!!!!!11'
    x = plain_toint(ptxt)
    rsa = myRSA()

    k = rsa.getPublic()
    z = encrypt_long(k, ptxt)

    print(z)
    s = rsa.decrypt_long(z)
    print(s)
    '''

    #testing how the signature protocol works
    '''
    rsa = myRSA()
    ptxt = b'test'
    x = plain_toint(ptxt)
    print(x)
    c = pow(x, rsa.d, rsa.n)
    print(c)
    z = pow(c, rsa.e, rsa.n)
    print(z)
    print(int_toplain(z))
    '''
