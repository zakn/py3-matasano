import pickle
import time
from part10 import myCBC
from part33 import diffieHellman

def reset_channelA():
    file = open('part34_Achan', 'wb')
    dh = {'state':0, 'B':0, 'msg':0}
    pickle.dump(dh, file)
    file.close()
    print('channel towards A reset')


def reset_channelB():
    file = open('part34_Bchan', 'wb')
    dh = {'state':0, 'p':0, 'g':0, 'A':0, 'msg':0}
    pickle.dump(dh, file)
    file.close()
    print('channel towards B reset')


def reset_channels():
    reset_channelA()
    reset_channelB()


def read_channelA():
    file = open('part34_Achan', 'rb')
    dh = pickle.load(file)
    file.close()
    return dh


def read_channelB():
    file = open('part34_Bchan', 'rb')
    dh = pickle.load(file)
    file.close()
    return dh

def listener():
    dho = diffieHellman()
    dho.s = 0
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
                file = open('part34_Bchan', 'wb')
                dh = {'state':1, 'p':dho.p, 'g':dho.g, 'A':dho.p}
                pickle.dump(dh, file)
                file.close()
                time.sleep(2)
            elif Achan['state']==1:
                dho.B = Achan['B']
                print('intercepted achan: {}'.format(Achan))
                file = open('part34_Achan', 'wb')
                dh = {'state':1, 'B':dho.p}
                pickle.dump(dh, file)
                file.close()
                time.sleep(2)
            elif (Bchan['state']==2 and bplain):
                print('intercepted bchan 2: {}'.format(Bchan))
                ctxt = Bchan['msg']
                iv = ctxt[-16:]
                cipher = myCBC(skey, iv)
                ptxt = cipher.CBCdec(ctxt[:-16], iv)
                print('intercepted plain: {}'.format(ptxt))
                bplain = False
                time.sleep(2)
            elif (Achan['state']==2 and aplain):
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
        '''

        elif Bchan['state']==2:
            print('received at state 2: {}'.format(Bchan))
            ctxt = Bchan['msg']
            iv = ctxt[-16:]
            cipher = myCBC(skey, iv)
            ptxt = cipher.CBCdec(ctxt[:-16], iv)
            send_msg(ptxt, skey, bytes([random.randint(0, 255) for i in range(16)]))
            return True
        '''


if __name__=='__main__':
    reset_channels()
    x = listener()
    print(x)

    
 
