import random
import binascii

#to be made bigger at some point, also removed any primes where (p-1) % 3 = 0
decent_primes = [196613, 1572869, 3145739, 12582917, 50331653,
                 100663319, 402653189, 805306457, 1610612741,
                 179426549, 179468873, 181563923, 200636549]

#returns k different primes from my list..
#i cheat here and pop them from the list to avoid n's that arent mutually coprime
def bs_randprimes(k):
    result = []
    while (len(result) < k):
        new = decent_primes.pop(random.randint(0, len(decent_primes)-1))
        result.append(new)
    return result

# aka: extended euclidean alg.. really want p to be prime
def invmod(a, p):
    u, v = (a, p)
    x1, x2 = (1, 0)
    while (u != 1) and (u != -1):
        #print('v is {}'.format(v))
        #print('u is {}'.format(u))
        q = v//u
        r = v - (q*u)
        x = x2 - q*x1
        v, u, x2, x1 = (u, r, x1, x)
    if (u == -1):
        print('u is -1 here')
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

def broadcast_attack(plain):
    x = plain_toint(plain)
    ciphers = []
    publix = []
    count = 0

    while count < 3:
        rsa = myRSA()
        k = rsa.getPublic()
        if (k in publix):
            k = 0
        else:
            c = rsa_enc(k, x)
            ciphers.append(c)
            publix.append(k)
            count += 1

    bigM = publix[0][1]*publix[1][1]*publix[2][1]
    M = [publix[1][1]*publix[2][1], publix[0][1]*publix[2][1], publix[1][1]*publix[0][1]]
    N = [invmod(M[i], publix[i][1]) for i in range(3)]
    me = sum([ciphers[k]*M[k]*N[k] for k in range(3)])
    me = me % bigM
    y = int(pow(me, (1/3)))+1
    return int_toplain(y)

if __name__ == '__main__':

    ptxt = b'a try'

    print(broadcast_attack(ptxt))