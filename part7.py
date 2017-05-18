import base64
from Crypto.Cipher import AES


x = base64.b64decode(open('7.txt', 'r').read())

key = b'YELLOW SUBMARINE'
cipherText = AES.new(key, AES.MODE_ECB)
y = cipherText.decrypt(x)
print(y)

