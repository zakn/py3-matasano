import pickle
import time
from part10 import myCBC
from part33 import diffieHellman

def reset_channelA():
    file = open('part35_Achan', 'wb')
    dh = {'state':0, 'B':0}
    pickle.dump(dh, file)
    file.close()
    print('channel towards A reset')


def reset_channelB():
    file = open('part35_Bchan', 'wb')
    dh = {'state':0, 'p':0, 'g':0}
    pickle.dump(dh, file)
    file.close()
    print('channel towards B reset')


def reset_channels():
    reset_channelA()
    reset_channelB()


def read_channelA():
    file = open('part35_Achan', 'rb')
    dh = pickle.load(file)
    file.close()
    return dh


def read_channelB():
    file = open('part35_Bchan', 'rb')
    dh = pickle.load(file)
    file.close()
    return dh

def listener(gchange):
    dho = diffieHellman()
    if gchange==1:
        dho.s = 1
        Amod = 1
    elif gchange=='p':
        dho.s = 0
        Amod = 0
    elif gchange=='p-1':
        #may need to change
        dho.s = 1
        Amod = 1
        Bmod = 1
    skey = dho.getkey(16)
    aplain = True
    bplain = True
    while True:
        try:
            Achan = read_channelA()
            Bchan = read_channelB()
            if Bchan['state']==1:
                print('intercepted bchan: {}'.format(Bchan))
                dho.p = Bchan['p']
                dho.g = Bchan['g']
                if gchange=='p':
                    gchange = dho.p
                elif gchange=='p-1':
                    gchange = dho.p-1
                file = open('part35_Bchan', 'wb')
                dh = {'state':1, 'p':dho.p, 'g':gchange}
                pickle.dump(dh, file)
                file.close()
                time.sleep(2)
            elif Achan['state']==1:
                print('intercepted achan: {}'.format(Achan))
                time.sleep(1)
            elif Bchan['state']==2:
                print('intercepted bchan 2: {}'.format(Achan))
                file = open('part35_Bchan', 'wb')
                dh = {'state':2, 'A':Amod}
                pickle.dump(dh, file)
                file.close()
                time.sleep(2)
            elif Achan['state']==2:
                print('intercepted achan 2: {}'.format(Achan))
                if Bmod == 1:
                    file = open('part35_Achan', 'wb')
                    dh = {'state':2, 'B':Bmod}
                    pickle.dump(dh, file)
                    file.close()
                else:
                    dho.B = Achan['B']
                time.sleep(2)
            elif (Bchan['state']==3 and bplain):
                print('intercepted bchan 3: {}'.format(Bchan))
                ctxt = Bchan['msg']
                iv = ctxt[-16:]
                cipher = myCBC(skey, iv)
                ptxt = cipher.CBCdec(ctxt[:-16], iv)
                print('intercepted plain: {}'.format(ptxt))
                bplain = False
                time.sleep(2)
            elif (Achan['state']==3 and aplain):
                print('intercepted achan 2: {}'.format(Achan))
                ctxt = Achan['msg']
                iv = ctxt[-16:]
                cipher = myCBC(skey, iv)
                ptxt = cipher.CBCdec(ctxt[:-16], iv)
                print('intercepted plain: {}'.format(ptxt))
                aplain = False
                return True
        except:
            Achan = {}


if __name__=='__main__':
    reset_channels()
    #x = listener(1)
    #x = listener('p')
    x = listener('p-1')
    print(x)

    
 
