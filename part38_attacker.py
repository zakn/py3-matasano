import random
import hashlib
import pickle
import time
import hmac

N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2
k = 3

b = 420
B = pow(g, b, N)

salt = 0
u = 69

def reset_channel():
    file = open('part38_Achan', 'wb')
    dh = {'state': 0}
    pickle.dump(dh, file)
    file.close()
    print('channel towards A reset')


def read_channel():
    file = open('part38_Bchan', 'rb')
    dh = pickle.load(file)
    file.close()
    return dh


def stateSet(statenum):
    dh = read_channel()
    dh['state'] = statenum
    file = open('part38_Bchan', 'wb')
    pickle.dump(dh, file)
    file.close()


def send_B():
    d = {'state': 1, 'B': B, 'salt': salt, 'u':u}
    file = open('part38_Achan', 'wb')
    pickle.dump(d, file)
    file.close()


def send_Confirmation():
    d = {'state': 2, 'confirm': True}
    file = open('part38_Achan', 'wb')
    pickle.dump(d, file)
    file.close()


def generate_K(receivedA, v):
    S = (receivedA * pow(v, u, N)) % N
    S = pow(S, b, N)
    sha = hashlib.sha256()
    sha.update(str(S).encode('ascii'))
    return sha.digest()


def get_HMAC(key):
    hmac_fn = hmac.new(str(key).encode('ascii'), msg=str(salt).encode('ascii'), digestmod=hashlib.sha256)
    hmac_fn = hmac_fn.digest()
    return hmac_fn


def cracker(check, A):
    file = open('words.txt').readlines()
    for word in file:
        w = word.strip().lower()
        sha = hashlib.sha256()
        sha.update((str(salt)+w).encode('ascii'))
        x = int.from_bytes(sha.digest(), byteorder='big')
        vee = pow(g, x, N)
        K = generate_K(A, vee)
        my_hmac = get_HMAC(K)
        if (check == my_hmac):
            print('Password is: {}'.format(w))
            return w


def listener():
    while True:
        Bchan = read_channel()
        if Bchan['state'] == 0:
            print('waiting...')
            time.sleep(5)
        elif Bchan['state'] == 1:
            print('received: {}'.format(Bchan))
            print('sending B...')
            send_B()
            stateSet(0)
            A = Bchan['A']
            time.sleep(5)
        elif Bchan['state'] == 2:
            print('received: {}'.format(Bchan))
            print('macs match')
            client_hmac = Bchan['hmac']
            send_Confirmation()
            return cracker(client_hmac, A)


if __name__ == '__main__':
    reset_channel()
    listener()
