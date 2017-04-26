import random
import hashlib
import pickle
import time
import hmac

N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2
k = 3

b = random.randint(0, N)
B = pow(g, b, N)

email = 'zak@example.com'
pw = 'pass123$'

salt = random.getrandbits(64)

sha = hashlib.sha256()
sha.update((str(salt)+pw).encode('ascii'))
x = int.from_bytes(sha.digest(), byteorder='big')
v = pow(g, x, N)
x, sha = (0,0)
B = k*v + B


def reset_channel():
    file = open('part36_Achan', 'wb')
    dh = {'state':0}
    pickle.dump(dh, file)
    file.close()
    print('channel towards A reset')

def read_channel():
    file = open('part36_Bchan', 'rb')
    dh = pickle.load(file)
    file.close()
    return dh

def stateSet(statenum):
    dh = read_channel()
    dh['state'] = statenum
    file = open('part36_Bchan', 'wb')
    pickle.dump(dh, file)
    file.close()

def send_B():
    d = {'state':1, 'B':B, 'salt':salt}
    file = open('part36_Achan', 'wb')
    pickle.dump(d, file)
    file.close()

def send_Confirmation():
    d = {'state':2, 'confirm':True}
    file = open('part36_Achan', 'wb')
    pickle.dump(d, file)
    file.close()

def compute_uH(receivedA):
    ss = hashlib.sha256()
    ss.update((str(receivedA) + str(B)).encode('ascii'))
    uH = str(ss.digest())
    u = int.from_bytes(ss.digest(), byteorder='big')
    return (u, uH)


def generate_K(receivedA, you):
    S = receivedA * pow(v, you, N)
    S = pow(S, b, N)
    sha = hashlib.sha256()
    sha.update(str(S).encode('ascii'))
    return sha.digest()


def get_HMAC(key):
    hmac_fn = hmac.new(str(key).encode('ascii'), msg=str(salt).encode('ascii'), digestmod=hashlib.sha256)
    hmac_fn = hmac_fn.digest()
    return hmac_fn
    

def listener():
    while True:
        Bchan = read_channel()
        if Bchan['state']==0:
            print('waiting...')
            time.sleep(5)
        elif Bchan['state']==1:
            print('received: {}'.format(Bchan))
            print('sending B...')
            send_B()
            stateSet(0)
            A = Bchan['A']
            res = compute_uH(A)
            K = generate_K(A, res[0])
            time.sleep(5)
        elif Bchan['state']==2:
            print('received: {}'.format(Bchan))
            check_mac = get_HMAC(K)
            if (check_mac == Bchan['hmac']):
                print('macs match')
                send_Confirmation()
                return True
            else:
                print('unexpected')
                return False
                
            

if __name__=='__main__':
    reset_channel()
    listener()
    #hmac_fn = hmac.new(str(salt).encode('ascii'), msg=str(b).encode('ascii'), digestmod=hashlib.sha256)
    #x = str(hmac_fn.digest())
    #print(x)
