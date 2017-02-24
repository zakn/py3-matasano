import base64
from Crypto.Cipher import AES
from part9 import pkcs


class myCBC:
    def __init__(self, key, initialV):
        self.IV = initialV
        self.ECB = AES.new(key, AES.MODE_ECB)
        self.blen = len(key)

    def ECBdec(self, byts):
        by = self.ECB.decrypt(byts)
        return bytearray(by)

    def ECBenc(self, byts):
        by = self.ECB.encrypt(byts)
        return bytearray(by)

    def CBCdec(self, byts):
        b = bytes(byts)
        blocks = [b[i:i+self.blen] for i in range(0, len(byts), self.blen)]
        current = self.ECB.decrypt(blocks[0])
        result = bytearray([current[h] ^ self.IV[h] for h in range(self.blen)])
        for k in range(1, len(blocks)):
            current = self.ECB.decrypt(blocks[k])
            result += bytearray([current[j] ^ blocks[k-1][j] for j in range(self.blen)])
        return result

    def CBCenc(self, byts):
        blocks = [byts[i:i+self.blen] for i in range(0, len(byts), self.blen)]
        current = bytes([blocks[0][h] ^ self.IV[h] for h in range(self.blen)])
        current = self.ECB.encrypt(current)
        result = current
        for k in range(1, len(blocks)):
            current = bytes([blocks[k][j] ^ current[j] for j in range(self.blen)])
            current = self.ECB.encrypt(current)
            result += current
        return bytearray(result)

    def setIV(self, byts):
        if (len(byts) != self.blen):
            return 0
        self.blen = byts
        return 1
    


if __name__=='__main__':

    exkey = b'YELLOW SUBMARINE'
    ciphertext = base64.b64decode(open('10.txt', 'r').read())
    ciph = myCBC(exkey, bytes(16))

    plaintext = ciph.CBCdec(ciphertext)

    print(plaintext)

    doublecipher = ciph.CBCenc(pkcs(plaintext, 16))

    doubleplain = ciph.CBCdec(doublecipher)
    
    for i in range(len(ciphertext)):
        if (ciphertext[i] != doublecipher[i]):
            print("{} : {}".format(ciphertext[i], doublecipher[i]))


    


    
    #test using pt7
    '''
    x = base64.b64decode(open('7.txt', 'r').read())
    lyrics = ciph.ECBdec(x)
    citxt = ciph.ECBenc(lyrics)

    if (citxt == x):
        print('it worked')
    '''
    
