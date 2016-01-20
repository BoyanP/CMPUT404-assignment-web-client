#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientSocket.connect(host,port)
        # use sockets!
        return None

    def get_code(self, data):
        #get status code
        #parse it from the first line
        return None

    def get_headers(self,data):
        #get response headers
        #probably used most for post
        return None

    def get_body(self, data):
        #get body of the httprequest
        #so add stuff like accept
        #and where you are going
        #or what variables you are posting
        return None

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        #code = 500
        #body = ""
        #--- initial code is above----
        
        #code = args[0]
        #headers = args[1]
        #body = args[2]

        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        #code = 500
        #body = ""
        #--- initial code is above----
        
        #code = args[0]
        #headers = args[1]
        #body = args[2]
        
        return HTTPRequest(code, body)

    def command(self,url ,command="GET" ,args=None):
        #sock = 80
        #self.connect(url,sock)
        #data = self.recvall(sock)
        #code = self.get_code(data)
        #headers=get_headers(data)
        #body = get_body(data)
        #args = [code,headers,body]
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )
