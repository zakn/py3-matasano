import random
import struct
from part28 import SHA1

class diffieHellman:

    def __init__(self, p = 0, g = 0):
        if p!=0:
            self.p = p
            self.g = g
            self.a = random.randint(0, p-1)
            self.b = None
            self.A = pow(g, self.a, p)
            self.B = None
            self.s = None
        else:
            #want to be able to initialize an empty dh object
            self.p = 0
            self.g = 0
            self.a = 0
            self.b = 0
            self.A = 0
            self.B = None
            self.s = None



    def produceB(self):
        self.b = random.randint(0, self.p-1)
        self.B = pow(self.g, self.b, self.p)
        self.s = pow(self.A, self.b, self.p)

    #for Bob
    def receiveB(self, randB):
        self.B = randB
        self.s = pow(self.B, self.a, self.p)
    
    def getkey(self, length):
        x = str(self.s)
        y = b''
        for i in range(0, len(x), 19):
            y += struct.pack('>Q', int(x[i:i+19]))
        return SHA1(y).digest()[:length]




if __name__=='__main__':

    #x = diffieHellman(37, 5)
    bigp = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    smallg = 2
    x = diffieHellman(bigp, smallg)
    x.produceB()

    print(x.a)
    print(x.b)
    print(x.A)
    print(x.B)
    print(x.s)
    print(x.getkey(16))

    
