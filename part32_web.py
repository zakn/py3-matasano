import http.server
import socketserver
import urllib.parse
import time
import binascii
from part11 import getkey
from part28 import SHA1
from Crypto.Util.strxor import strxor_c

gkey = getkey(80)
#gkey = b'YELLOW SUBMARINEYELLOW SUBMARINEYELLOW SUBMARINEYELLOW SUBMARINE'
blen = 64
wait = 0.005

def shaHMAC(key, message):
    if (len(key)>blen):
        key = SHA1(key).digest()
    if (len(key)<blen):
        key += bytes(blen - len(key))

    opad = strxor_c(key, 0x5c)
    ipad = strxor_c(key, 0x36)

    return SHA1(opad + SHA1(ipad + message).digest()).digest()


def insecure_compare(a, b):
    if (len(a) > len(b)):
        b += bytes(len(a)-len(b))
    for i in range(len(a)):
        if (a[i] != b[i]):
            return False
        else:
            time.sleep(wait)
            print(b[i])
    return True
    

class reqHandler(http.server.BaseHTTPRequestHandler):

    #GET
    def do_GET(self):
        urlvars = urllib.parse.urlparse(self.path)
        if (urlvars.path == '/test'):
            q = urllib.parse.parse_qs(urlvars.query)
            sign = binascii.unhexlify(q['signature'][0])
            txt = q['file'][0].encode('utf-8')
            truesign = shaHMAC(gkey, txt)
            #truesign = b"d\xbe\x96\x81;\x83'\xc7>#\x12m\xc7\xa0Zb\xb1\xb4\xc6\x86"

            if insecure_compare(truesign, sign):
                #status code
                self.send_response(200)
                #headers
                self.send_header('Content-type','text/html')
                self.end_headers()
            
                #message
                m = 'hello intranet! \n'
                #write message
                self.wfile.write(bytes(m, 'utf-8'))
            else:
                self.send_error(500)
        else:
            self.send_error(500)

        
        

def run():
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('', 8080)
  httpd = http.server.HTTPServer(server_address, reqHandler)
  print('running server...')
  print(shaHMAC(gkey, b'bargers'))
  httpd.serve_forever()




if __name__=='__main__':

    run()
    

