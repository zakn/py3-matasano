import urllib.request
import time
import binascii
import pickle


def try_sign(filename, signature):
    start = time.time()
    try:
        response = urllib.request.urlopen('http://localhost:8080/test?file=' + filename + '&signature=' + signature)
        end = time.time()
        return (True, end - start)

    except urllib.error.HTTPError as err:
        end = time.time()
        return (False, end - start)


def reset_file():
    file = open('part32_avg', 'wb')
    times_avg = [(0,0)]*256
    pickle.dump(times_avg, file)
    file.close()
    print('file reset')
       

def avg_handler(tup, newtime):
    newnum = tup[0] + 1
    newav = (tup[1]*tup[0] + newtime)/newnum
    return (newnum, newav)

def get_top10():
    top5 = [[0, (0,0)]]*10
    file = open('part32_avg', 'rb')
    arr = pickle.load(file)
    file.close()
    for i in range(len(arr)):
        if (arr[i][1] > top5[0][1][1]):
            top5[9] = top5[8]
            top5[8] = top5[7]
            top5[7] = top5[6]
            top5[6] = top5[5]
            top5[5] = top5[4]
            top5[4] = top5[3]
            top5[3] = top5[2]
            top5[2] = top5[1]
            top5[1] = top5[0]
            top5[0] = [bytes([i]), (0 , arr[i][1])]
        elif (arr[i][1] > top5[1][1][1]):
            top5[9] = top5[8]
            top5[8] = top5[7]
            top5[7] = top5[6]
            top5[6] = top5[5]
            top5[5] = top5[4]
            top5[4] = top5[3]
            top5[3] = top5[2]
            top5[2] = top5[1]
            top5[1] = [bytes([i]), (0 , arr[i][1])]
        elif (arr[i][1] > top5[2][1][1]):
            top5[9] = top5[8]
            top5[8] = top5[7]
            top5[7] = top5[6]
            top5[6] = top5[5]
            top5[5] = top5[4]
            top5[4] = top5[3]
            top5[3] = top5[2]
            top5[2] = [bytes([i]), (0 , arr[i][1])]
        elif (arr[i][1] > top5[3][1][1]):
            top5[9] = top5[8]
            top5[8] = top5[7]
            top5[7] = top5[6]
            top5[6] = top5[5]
            top5[5] = top5[4]
            top5[4] = top5[3]
            top5[3] = [bytes([i]), (0 , arr[i][1])]
        elif (arr[i][1] > top5[4][1][1]):
            top5[9] = top5[8]
            top5[8] = top5[7]
            top5[7] = top5[6]
            top5[6] = top5[5]
            top5[5] = top5[4]
            top5[4] = [bytes([i]), (0 , arr[i][1])]
        elif (arr[i][1] > top5[5][1][1]):
            top5[9] = top5[8]
            top5[8] = top5[7]
            top5[7] = top5[6]
            top5[6] = top5[5]
            top5[5] = [bytes([i]), (0 , arr[i][1])]
        elif (arr[i][1] > top5[6][1][1]):
            top5[9] = top5[8]
            top5[8] = top5[7]
            top5[7] = top5[6]
            top5[6] = [bytes([i]), (0 , arr[i][1])]
        elif (arr[i][1] > top5[7][1][1]):
            top5[9] = top5[8]
            top5[8] = top5[7]
            top5[7] = [bytes([i]), (0 , arr[i][1])]
        elif (arr[i][1] > top5[8][1][1]):
            top5[9] = top5[8]
            top5[8] = [bytes([i]), (0 , arr[i][1])]
        elif (arr[i][1] > top5[9][1][1]):
            top5[9] = [bytes([i]), (0 , arr[i][1])]
    return top5


def test_top10(known, tops, filename):
    results = []
    for i in range(len(tops)):
        sign_guess = known + tops[i][0] + bytes(19-len(known))
        time = try_sign(filename, binascii.hexlify(sign_guess).decode('utf8'))[1]
        results.append([tops[i][0], avg_handler(tops[i][1], time)])
    return results
        

def next_byte_avgs(known, filename):
    buff = known + bytes(20-len(known))
    times = [0]*256
    try:
        file = open('part32_avg', 'rb')
    except:
        reset_file()
        file = open('part32_avg', 'rb')
        
    times_avg = pickle.load(file)
    file.close()


    for i in range(256):
        sign_guess = known + bytes([i]) + buff[len(known)+1:]
        times[i] = try_sign(filename, binascii.hexlify(sign_guess).decode('utf8'))[1]
        times_avg[i] = avg_handler(times_avg[i], times[i])
    
    file = open('part32_avg', 'wb')
    #print(times_avg)
    pickle.dump(times_avg, file)
    file.close()
    #print(times)
    return sum(times[50:100])/50


def backtrack_check(sign, filename, last_avg):
    reset_file()
    count = 1
    while True:
        current_avg = next_byte_avgs(sign, filename)
        if (current_avg > (last_avg + 0.001)):
            return True
        else:
            return False



def byte_wrapper(known, filename, last_avg = 0, lastlast_avg = 0):
    reset_file()
  
    #populate the avgs file
    for i in range(3):
        current_avg = next_byte_avgs(known, filename)
        print(current_avg)
        if (current_avg < (last_avg + 0.001)):
            print('backtrack to {}'.format(known[:-1]))
            return (known[:-1], lastlast_avg, lastlast_avg)

    
    #top10 testing
    t10 = get_top10()
    count = 0
    while (count < 10):
        t10 = test_top10(known, t10, filename)
        count +=1
    t10 = sorted(t10, key = lambda x: x[1][1], reverse=True)
    print(t10)
    for k in range(len(t10)):
        best_guess = t10[k][0]
        attempt = backtrack_check(known + best_guess, filename, current_avg)
        if attempt==True:
            return (known + best_guess, current_avg, last_avg)
    return (known + best_guess, current_avg, last_avg)
        

def find_sign(filename, known=b'', lavg = 0):
    sign = known
    llavg = 0
    while len(sign) < 20:
        print(sign)
        result = byte_wrapper(sign, filename, lavg, llavg)
        print('sign and last avg: {}'.format(result))
        sign = result[0]
        lavg = result[1]
        llavg = result[2]
        if len(sign)==0:
            return None
    return sign



if __name__=='__main__':
    #print(next_byte(b'', 'bargers'))
    x = find_sign('bargers', b'')
    print(x)

    #b')t\x0b\xff\xa5\x80\xd4\xc4\xacV\x00\x89t\x91\xda\xc7iC\x05r'

    
    
