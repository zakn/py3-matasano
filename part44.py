import random
import hashlib
import part39


p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b
g = 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291

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

def get_x(s, r, k, H):
    x = (s*k - H) % q
    return (part39.invmod(r, q)*x) % q

def hashnum(msg):
    sha = hashlib.sha1()
    sha.update(msg)
    return int.from_bytes(sha.digest(), byteorder='big')

def unpack_messages():
    linelist = list(open('44.txt', 'r'))
    msg_groups = [linelist[i:i+4] for i in range(0, len(linelist), 4)]
    result = []
    for z in msg_groups:
        msg = z[0].lstrip('msg: ').rstrip('\n').encode('ascii')
        H = int(z[3].lstrip('m: ').rstrip('\n'), 16)
        if (H != hashnum(msg)):
            raise ValueError('peggy, that hash aint right')
        s = int(z[1].lstrip('s: ').rstrip('\n'))
        r = int(z[2].lstrip('r: ').rstrip('\n'))
        result.append((msg, s, r, H))
    return result


def find_repeatr(msg_list):
    observed_rs = []
    for i in range(len(msg_list)):
        r = msg_list[i][2]
        if r in observed_rs:
            j = observed_rs.index(r)
            break
        else:
            observed_rs.append(r)
    return (msg_list[j], msg_list[i])


def get_k(b1, b2):
    w = (b1[1] - b2[1]) % q
    if w < 0:
        w = q - w
    w = part39.invmod(w, q)
    k = (b1[3] - b2[3]) % q
    if k < 0:
        k = q - k
    k = (k*w) % q
    return k


if __name__ == '__main__':
    y = 0x2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821
    xcheck = 0xca8f6f7c66fa362d40760d135b763eb8527d3d52

    msgs = unpack_messages()
    print(msgs)

    pair = find_repeatr(msgs)
    mess, s, r, H = pair[0]
    k = get_k(pair[0], pair[1])
    print(k)

    x = get_x(s, r, k, H)
    print(x)

    sha = hashlib.sha1()
    sha.update(hex(x)[2:].encode('ascii'))
    Hx = part39.plain_toint(sha.digest())
    if xcheck != Hx:
        raise ValueError('waaaaaaah, u got the wrong private key!')





