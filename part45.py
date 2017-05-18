import random
import hashlib
import part39


p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b
g = 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291

def g_override(n):
    global g
    g = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
    g += n
    return


def skeleton_sign(msg):
    z, x = (random.randint(1, q-1), random.randint(1, q-1))
    y = pow(g, x, p)
    r = pow(y, z, p) % q
    s = (part39.invmod(z, q)*r) % q

    return [msg, (r, s), y]


def signit(msg):
    x, k = (random.randint(1, q-1), random.randint(1, q-1))
    y = pow(g, x, p)
    r = pow(g, k, p) % q

    sha = hashlib.sha1()
    sha.update(msg)
    hm = part39.plain_toint(sha.digest())
    s = (hm + x*r) % q
    s = (s*part39.invmod(k, q)) % q

    return [msg, (r, s), y]


def server_check(msg, rs, why):
    w = part39.invmod(rs[1], q)
    sha = hashlib.sha1()
    sha.update(msg)
    u1 = (part39.plain_toint(sha.digest())*w) % q
    u2 = (rs[0]*w) % q
    v = (pow(g, u1, p)*pow(why, u2, p) % p) % q
    return v==rs[0]




if __name__ == '__main__':

    ptxt = b'Hello, world'
    g_override(0)

    x = signit(ptxt)
    print(server_check(b'to hurgle', x[1], x[2]))

    g_override(1)
    x = skeleton_sign(ptxt)
    print(server_check(x[0], x[1], x[2]))

    print(server_check(b'goodbye, world', x[1], x[2]))





