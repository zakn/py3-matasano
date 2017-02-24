import binascii
import base64


def hexTo64(string):
    bits = binascii.unhexlify(string)
    result = base64.b64encode(bits)
    result = bytearray(result)
    return result
    
    

if __name__ == '__main__':
    enc = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    ans = hexTo64(enc)
    print(ans)
    
    






