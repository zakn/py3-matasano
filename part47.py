import random
import part39
import base64

rsa = part39.myRSA(128)
e, d, n = rsa.getkeys()


def oracle(msg):
    plain = part39.int_toplain(rsa.decrypt(msg), (n.bit_length()+7)//8)
    return (plain[0] == 0 and plain[1] == 2)


def pkcs15pad(msg, n):
    l = (n.bit_length()+7)//8
    pad = bytes(random.sample(range(1, 256), l - 3 - len(msg)))
    return b'\x00\x02' + pad + b'\x00' + msg


def search_start(c, e, n, B):
    s = (n + 3*B - 1)//(3*B)
    while True:
        newc = (c * pow(s, e, n)) % n
        if oracle(newc):
            return [s, newc]
        s += 1


def update_s(c, s, M, n, B):
    a, b = M[0]
    r = 2*(b*s - 2*B + n - 1)//n
    while True:
        print(r)
        lower = (2*B + r*n + b-1)//b
        upper = (3*B + r*n + a-1)//a
        print( (lower, upper))
        for k in range(lower, upper):
            newc = (c * pow(s, e, n)) % n
            if oracle(newc):
                return [s, newc]
        r += 1


def update_interval(n, M, s, B):
    a, b = M[0]
    rlow = (s*a - 3*B -1 + n + 1)//n
    rhigh = (s*b - 2*B)//n
    if (rlow != rhigh):
        print('uh oh')
    newA = max(a, (2*B + rlow*n + s - 1)//s)
    newB = min(b, (3*B - 1 + rlow*n)//s)
    return [[newA, newB]]


def padding_attack(c, pub):
    e, n = pub
    l = (n.bit_length() + 7) // 8
    B = 2**(8*(l-2))
    M = [(2*B, 3*B - 1)]
    s0, c0 = search_start(c, e, n, B)
    M = update_interval(n, M, s0, B)
    while True:
        print(M)
        if M[0][0] == M[0][1]:
            m = M[0][0]
            return part39.int_toplain(m)
        s0, c0 = update_s(c0, s0, M, n, B)
        M = update_interval(n, M, s0, B)





if __name__ == '__main__':

    ptxt = b'kick it, CC'
    pub = [e, n]
    p = pkcs15pad(ptxt, pub[1])
    c = part39.byte_enc(pub, p)

    print(p)
    print(oracle(c))

    print(padding_attack(c, pub))



