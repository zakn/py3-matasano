import binascii

def repKeyXOR(byte_str, key):
    result = b''
    for i in range(len(byte_str)):
        result += bytes([byte_str[i] ^ key[i % len(key)]])
    return result



if __name__ == '__main__':
    x = b'''Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal'''
    key = b'ICE'
    y = repKeyXOR(x, key)
    encodedY = binascii.hexlify(y).decode('ascii')
    print(encodedY)
