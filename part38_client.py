import random
import hashlib
import pickle
import time
import hmac

N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2
k = 3

a = random.randint(0, N)
A = pow(g, a, N)

email = 'zak@example.com'
pw = 'aardvark'

def reset_channel():
    file = open('part38_Bchan', 'wb')
    dh = {'state':0}
    pickle.dump(dh, file)
    file.close()
    print('channel towards B reset')

def read_channel():
    file = open('part38_Achan', 'rb')
    dh = pickle.load(file)
    file.close()
    return dh

def stateSet(statenum):
    dh = read_channel()
    dh['state'] = statenum
    file = open('part38_Achan', 'wb')
    pickle.dump(dh, file)
    file.close()

def send_email(newA):
    dh = {'state':1, 'A':newA, 'email':email}
    file = open('part38_Bchan', 'wb')
    pickle.dump(dh, file)
    file.close()


def generate_K(bigB, salty, you, override=A):
    sha = hashlib.sha256()
    sha.update((str(salty)+pw).encode('ascii'))
    x = int.from_bytes(sha.digest(), byteorder='big')
    aa = (a + you*x) % N
    S = pow(bigB, aa, N)
    sha = hashlib.sha256()
    sha.update(str(S).encode('ascii'))
    return sha.digest()


def send_HMAC(key, msgg):
    hmac_fn = hmac.new(str(key).encode('ascii'), msg=str(msgg).encode('ascii'), digestmod=hashlib.sha256)
    hmac_fn = hmac_fn.digest()
    dh = {'state':2, 'hmac':hmac_fn}
    file = open('part38_Bchan', 'wb')
    pickle.dump(dh, file)
    file.close()
    return hmac_fn

def listener():
    send_email(A)
    while True:
        Achan = read_channel()
        if Achan['state']==0:
            print('waiting...')
            time.sleep(5)
        elif Achan['state']==1:
            print('received: {}'.format(Achan))
            print('sending HMAC...')
            stateSet(0)
            B, salt, u = (Achan['B'], Achan['salt'], Achan['u'])
            K = generate_K(B, salt, u, A)
            check_mac = send_HMAC(K, salt)
            time.sleep(5)
        elif Achan['state']==2:
            print('received: {}'.format(Achan))
            stateSet(0)
            if Achan['confirm']:
                return True
            else:
                return False



if __name__=='__main__':
    reset_channel()
    print(listener())

