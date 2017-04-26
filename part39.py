import random
import binascii

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

# aka: extended euclidean alg.. really want p to be prime
def invmod(a, p):
    u, v = (a, p)
    x1, x2 = (1, 0)
    while (u != 1):
        q = v//u
        r = v - (q*u)
        x = x2 - q*x1
        v, u, x2, x1 = (u, r, x1, x)
    if (x1 < 0):
        x1 = p + x1
    return x1


class myRSA:

    def __init__(self):
        self.p, self.q = bs_randprimes(2)
        self.n = self.p*self.q
        self.et = (self.p-1)*(self.q-1)
        self.e = 3
        self.d = invmod(self.e, self.et)

    def getPublic(self):
        return [self.e, self.n]

    def decrypt(self, ctxt):
        return pow(ctxt, self.d, self.n)


#pkey expected [e, n] list and msg is and int
def rsa_enc(pkey, msg):
    return pow(msg, pkey[0], pkey[1])


def plain_toint(byts):
    return int.from_bytes(byts, byteorder='big')

def int_toplain(n):
    return n.to_bytes((n.bit_length() + 7) // 8, byteorder='big')

if __name__ == '__main__':

    ptxt = b'a try'
    x = plain_toint(ptxt)

    rsa = myRSA()
    #x = 42
    k = rsa.getPublic()
    c = rsa_enc(k, x)
    s = rsa.decrypt(c)

    print(int_toplain(s))

    '''
    for p in decent_primes:
        print(p)
        p0 = p-1
        if (p0 % 3 == 0):
            print('is bad')
        else:
            print('is good')
    '''