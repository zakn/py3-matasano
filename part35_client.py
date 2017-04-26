import pickle
import time
import random
from part10 import myCBC
from part33 import diffieHellman

def reset_channel():
    file = open('part35_Bchan', 'wb')
    dh = {'state':0, 'p':0, 'g':0}
    pickle.dump(dh, file)
    file.close()
    print('channel towards B reset')


def read_channel():
    file = open('part35_Achan', 'rb')
    dh = pickle.load(file)
    file.close()
    return dh


def stateSet(statenum):
    dh = read_channel()
    dh['state'] = statenum
    file = open('part35_Achan', 'wb')
    pickle.dump(dh, file)
    file.close()

    
def send_pg(mp, mg):
    file = open('part35_Bchan', 'wb')
    dh = {'state':1, 'p':mp, 'g':mg}
    pickle.dump(dh, file)
    file.close()


def send_A(mA):
    dh = {'state':2, 'A':mA}
    file = open('part35_Bchan', 'wb')
    pickle.dump(dh, file)
    file.close()  


def send_msg(msg, key, initial_v):
    cipher = myCBC(key, initial_v)
    m = cipher.CBCenc(msg) + initial_v
    dh = {'state':3, 'msg':m}
    file = open('part35_Bchan', 'wb')
    pickle.dump(dh, file)
    file.close()
    

def listener(mp, mg):
    dh_obj = diffieHellman(mp, mg)
    send_pg(dh_obj.p, dh_obj.g)
    iv = bytes([random.randint(0, 255) for i in range(16)])
    mess = b"Money in the bank, pimpin' aint easy"
    while True:
        Achan = read_channel()
        if Achan['state']==0:
            print('waiting...')
            time.sleep(5)
        elif Achan['state']==1:
            print('received: {}'.format(Achan))
            print('sending A...')
            stateSet(0)
            send_A(dh_obj.A)
            time.sleep(5)
        elif Achan['state']==2:
            print('received at state 2: {}'.format(Achan))
            stateSet(0)
            dh_obj.receiveB(Achan['B'])
            skey = dh_obj.getkey(16)
            send_msg(mess, skey, iv)
            time.sleep(5)
        elif Achan['state']==3:
            print('received at state 3: {}'.format(Achan))
            stateSet(0)
            ctxt = Achan['msg']
            niv = ctxt[-16:]
            newcipher = myCBC(skey, niv)
            ptxt = newcipher.CBCdec(ctxt[:-16], niv)
            print(ptxt)
            if (mess == ptxt[:len(mess)]):
                return True
            else:
                return False



if __name__=='__main__':
    reset_channel()
    bigp = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    smallg = 2
    z = listener(bigp, smallg)
    print(z)
 
