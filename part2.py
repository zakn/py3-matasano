import binascii


#takes 2 hex strings as input, outputs a hex string
def fixedLenXOR(x, y):
    bits1 = binascii.unhexlify(x)
    bits2 = binascii.unhexlify(y)
    result_bits = bytes([(bits1[i] ^ bits2[i]) for i in range(len(bits1))])
    result_final = binascii.hexlify(result_bits)
    return result_final
    
    
    

if __name__ == '__main__':
    x = '1c0111001f010100061a024b53535009181c'
    y = '686974207468652062756c6c277320657965'
    ans = fixedLenXOR(x, y)
    print(ans)
    






