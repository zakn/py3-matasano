import pickle
import random
import time
from part10 import myCBC
from part33 import diffieHellman

b = 0
B = 0

def reset_channel():
    file = open('part34_Achan', 'wb')
    dh = {'state':0, 'B':0, 'msg':0}
    pickle.dump(dh, file)
    file.close()
    print('channel towards A reset')


def read_channel():
    file = open('part34_Bchan', 'rb')
    dh = pickle.load(file)
    file.close()
    return dh


def stateSet(statenum):
    dh = read_channel()
    dh['state'] = statenum
    file = open('part34_Bchan', 'wb')
    pickle.dump(dh, file)
    file.close()


def getS(mA, mp):
    return pow(mA, b, mp)


def send_B(mp, mg):
    global b, B
    if (b == 0):
        b = random.randint(0, mp-1)
        B = pow(mg, b, mp)
    file = open('part34_Achan', 'wb')
    dh = {'state':1, 'B':B}
    pickle.dump(dh, file)
    file.close()


def send_msg(msg, key, initial_v):
    cipher = myCBC(key, initial_v)
    m = cipher.CBCenc(msg) + initial_v
    print(m)
    dh = {'state':2, 'msg':m}
    file = open('part34_Achan', 'wb')
    pickle.dump(dh, file)
    file.close()


def listener():
    dho = diffieHellman()
    while True:
        Bchan = read_channel()
        if Bchan['state']==0:
            print('waiting...')
            time.sleep(5)
        elif Bchan['state']==1:
            print('received: {}'.format(Bchan))
            print('sending B...')
            stateSet(0)
            dho.p = Bchan['p']
            dho.g = Bchan['g']
            dho.A = Bchan['A']
            send_B(dho.p, dho.g)
            dho.s = getS(dho.A, dho.p)
            skey = dho.getkey(16)
            time.sleep(5)
        elif Bchan['state']==2:
            print('received at state 2: {}'.format(Bchan))
            stateSet(0)
            ctxt = Bchan['msg']
            iv = ctxt[-16:]
            cipher = myCBC(skey, iv)
            ptxt = cipher.CBCdec(ctxt[:-16], iv)
            send_msg(ptxt, skey, bytes([random.randint(0, 255) for i in range(16)]))
            return True

            

            
        



if __name__=='__main__':
    reset_channel()
    x = read_channel()
    print(x)
    listener()
    #send_B(x['p'], x['g'])

 
