import urllib.request
import time
import binascii


def try_sign(filename, signature):
    start = time.time()
    try:
        response = urllib.request.urlopen('http://localhost:8081/test?file=' + filename + '&signature=' + signature)
        end = time.time()
        return (True, end - start)

    except urllib.error.HTTPError as err:
        end = time.time()
        return (False, end - start)


def find_sign(filename):
    known_bytes = b''
    for k in range(20):
        known_bytes += next_byte(known_bytes, filename)
        print(known_bytes)
    return known_bytes


def find_sign_continue(filename, known):
    known_bytes = known
    for k in range(20-len(known)):
        known_bytes += next_byte(known_bytes, filename)
        print(known_bytes)
    return known_bytes
    


def next_byte(known, filename):
    buff = known + bytes(20-len(known))
    last_time = try_sign(filename, binascii.hexlify(buff).decode('utf8'))[1]
    cmax = last_time
    for i in range(256):
        sign_guess = known + bytes([i]) + buff[len(known)+1:]
        attempt = try_sign(filename, binascii.hexlify(sign_guess).decode('utf8'))
        #print(i, attempt[1])
        if (attempt[1] > cmax):
            cmax = attempt[1]
            print(binascii.hexlify(sign_guess).decode('utf8'))
            print(cmax)
            iguess = i
        #if (attempt[1] > (last_time + 0.08)):
            #print('the next byte is {}'.format(bytes([i])))
            #return bytes([i])
    return bytes([iguess])




if __name__=='__main__':
    print(try_sign('bargers', '8ff7b1a85191fb4385c08e9f05a18bac8132a5fa'))
    print(find_sign_continue('bargers', b'\x8f\xf7\xb1\xa8Q\x91\xfbC\x85\xc0\x8e\x9f\x05\xa1'))
