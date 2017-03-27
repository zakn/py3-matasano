from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from part18 import myCTR
import base64
import binascii

#40 of these
strings = [
    b'SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==',
    b'Q29taW5nIHdpdGggdml2aWQgZmFjZXM=',
    b'RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==',
    b'RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=',
    b'SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk',
    b'T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
    b'T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=',
    b'UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
    b'QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=',
    b'T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl',
    b'VG8gcGxlYXNlIGEgY29tcGFuaW9u',
    b'QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==',
    b'QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=',
    b'QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==',
    b'QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=',
    b'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=',
    b'VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==',
    b'SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==',
    b'SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==',
    b'VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==',
    b'V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==',
    b'V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==',
    b'U2hlIHJvZGUgdG8gaGFycmllcnM/',
    b'VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=',
    b'QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=',
    b'VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=',
    b'V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=',
    b'SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==',
    b'U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==',
    b'U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=',
    b'VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==',
    b'QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu',
    b'SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=',
    b'VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs',
    b'WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=',
    b'SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0',
    b'SW4gdGhlIGNhc3VhbCBjb21lZHk7',
    b'SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=',
    b'VHJhbnNmb3JtZWQgdXR0ZXJseTo=',
    b'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=',
]

#key randomized once
key = b'\x11\xf4\xdec\xd25G\x17\x1a\xe9\xc0i\x8b\x15\x0fp'

#for guessing
expected_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,-'

def encrypt_strings(str_array):
    result = []
    for s in str_array:
        cipher = myCTR(key, 0)
        result.append(cipher.crypt(base64.b64decode(s)))
    return result


#idea here is to guess as the first byte of the keystream 
def byte_sized(estrings, place):
    possibles = []
    for i in range(256):
        score = 0
        for s in estrings:
            test = s[place] ^ i
            if (chr(test) in expected_chars):
                score += 1
        if (score >= 39):
            #most characters are expected and this may be a keystream byte
            possibles.append(bytes([i]))

    return possibles
        



if __name__ == '__main__':

    x = encrypt_strings(strings)

    streamguess = []

    for h in range(20):
        y = byte_sized(x, h)
        print(y)
        streamguess.append(y[len(y)-1])


    for j in range(40):
        maybeplain = bytes([x[j][b] ^ streamguess[b][0] for b in range(len(streamguess))])
        print(maybeplain)
    
    



