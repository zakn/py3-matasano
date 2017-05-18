import random
import hashlib
import part39
import base64

#just to make testing take less time generatin primes
prepro_primes = (
    91071813174401404173455049717527321587613785878096961084530594408844135513472352574091533145858152678143873019310222166014880508900627350578419955047329168862587124268270298098045908336871655432196427438426004030924929486438704527462979958857173690737807248366883590469504741862048599261595259008575869091777,
    155517098120418219361926920032280632272201454862461738423687465846086057653670310860294909909305371265755997160487002779230587095487788696797490561629576475899908696637347253025227855630037432866074912340794470442020393251352206822777360956631307594053921826665139323452889821079193976175832887680763974046061
)

def parity_oracle(msg, rsa_obj):
    plain = rsa_obj.decrypt(msg)
    return plain % 2


def attack(ctxt, rsa_obj):
    e, n = rsa_obj.getPublic()
    dubla = pow(2, e, n)
    bound = [0, n]
    x = ctxt

    for i in range(len(bin(n))-2):
        x = (x * dubla) % n
        odd = parity_oracle(x, rsa_obj)
        if (odd == 0):
            bound[1] = (bound[1]+bound[0])//2
        else:
            bound[0] = (bound[1]+bound[0])//2
        print(part39.int_toplain(bound[1]))

    return bound

'''
def testattack():
    rsa_obj = part39.myRSA(16, (7, 11))
    pub = 8
    plain = 32
    ctxt = part39.rsa_enc(pub, plain)

    e, n = (3, 77)
    dubla = pow(2, e, n)
    bound = [0, n]
    x = ctxt

    for i in range(len(bin(n))-2):
        x = (x * dubla) % n
        odd = parity_oracle(x, rsa_obj)
        if (odd == 0):
            bound[1] = (bound[1]+bound[0])//2 + 1
        else:
            bound[0] = (bound[1]+bound[0])//2
        print(part39.int_toplain(bound[1]))

    return bound
'''

if __name__ == '__main__':

    ptxt = b'VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ=='
    ptxt = base64.b64decode(ptxt)

    rsa = part39.myRSA(1024, prepro_primes)
    pub = rsa.getPublic()

    x = part39.plain_toint(ptxt)
    print(x)
    c = part39.rsa_enc(pub, x)
    print(c)
    z = attack(c, rsa)
    print(z)



