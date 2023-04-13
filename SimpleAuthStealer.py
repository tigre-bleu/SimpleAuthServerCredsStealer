#!/usr/bin/env python
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import sys
import base64

class AuthHandler(SimpleHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global key
        ''' Present frontpage with user authentication. '''
        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        else:
            print "Authentication data received:"
            print self.headers.getheader('Authorization')
            if self.headers.getheader('Authorization').startswith('Basic '):
                key = self.headers.getheader('Authorization')[6:len(self.headers.getheader('Authorization'))]
                print base64.b64decode(key)
                self.do_AUTHHEAD()
                pass

def test(HandlerClass = AuthHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    if len(sys.argv)<1:
        print "usage SimpleAuthServer.py [port]"
        sys.exit()
    test()
