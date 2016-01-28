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
    print "httpclient.py [URL] [GET/POST] \n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def parseURL(self,url):
        stripped = re.sub('(http://|https://)?',"",url)
        path = ""
        host = ""
        port = 80
        maybePort=""
        lookForPathFlag = False
        #print "stripped: " + str(stripped)
        for char in stripped:
            #print char
            if char != '/' and lookForPathFlag == False:
                host+=char

            else:
                #host+='/'
                lookForPathFlag = True

            if(lookForPathFlag):
                path+=char
        try:
            host,maybePort = host.split(':')
        except:
            print "port not specified using default: 80"
        if path == '':
            path = '/'
        if maybePort != "":
            port = int(maybePort)
        #print "HOST IS :" + host
        #print "PATH IS : " + path
        return [path,host,int(port)]
        
    def createRequestHeader(self,path,host,command="GET"):
        header = command + " " + path + " HTTP/1.1 \r\n"
        header+= "Accept: */* \r\n"
        header+= "Host: " + host + "\r\n"
        header+= "Connection: close \r\n"

        #print "HEADER IS : " + header
        return header

    def parseResponse(self,response):
        #parse the same way as the test lol
        code = ""
        body = ""
        responseParts = response.split('\n')

        bodyFlag = False
        body = []
        for element in responseParts:
                    
            if element == "":
                bodyFlag = True
                continue # skip \n 
            if bodyFlag:
                body.append(element)

        joinedBody = "".join(body)

        code = responseParts[0].split(" ")[1]

        return [code,joinedBody]
        
    def connect(self, host, port):
	#print"\n hey whats up \n"
	#print("host in connect: ") + str(host)
	#print("port in connect: " + str(port))

        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientSocket.connect((host,port))
        #print "connected to " + host + "at port: " + port + "\n" 
        # use sockets!
        return clientSocket
        #probably return clientSocket

    def get_code(self, data):
        #get status code
        #parse it from the first line
	code = '500'
        response = data.split('\n')
	try:
        	code = response[0].split(" ")[1]
	except IndexError:
		'no body returned'        
	return code

    def get_headers(self,data):
        #get response headers
        #probably used most for post
        response = data.split("\r\n")
        headers=[]
        for element in response:
            if element in ['','\r']:
                break
            else:
                headers.append(element)
        #print "headers: " + headers
        return headers

    def get_body(self, data):
        #get body of the httprequest
        #so add stuff like accept
        #and where you are going
        #or what variables you are posting
        response = data.split('\n')
        #print "response: " + str(response)
        bodyFlag = False
        body = []
        for element in response:
            if element in ["",'\r']:
                bodyFlag = True
                continue # skip \n
            if bodyFlag:
                body.append(element)
        joinedBody = "".join(body)
        #print "body in get: " + str(joinedBody)
        return joinedBody

    # read everything from the socket
    def recvall(self, sock):
	#print "am i in recvall?"
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
		#print str(buffer)
            else:
                done = not part
	#print "am i stuck in the loop?"
        return str(buffer)

    def GET(self, url, args=None):

        path,host,port = self.parseURL(url)
	#print "host in GET: " + host
        headerToSend = self.createRequestHeader(path,host,"GET")
        clientSocket = self.connect(host,port)
        clientSocket.sendall(headerToSend + "\r\n\r\n")
        httpResponse = self.recvall(clientSocket)
        #print httpResponse

        #data = self.recvall(clientSocket)
        code = self.get_code(httpResponse)
        headers= self.get_headers(httpResponse)
        body = self.get_body(httpResponse)

        #print "code: " + str(code)
        #print "headers: " + str(headers)
        #print "body: " + str(body)



        return HTTPResponse(int(code), body)

    def POST(self, url, args=None):

	contentLength = 0 	
        postBody = None

	if (args != None):
            postBody = urllib.urlencode(args)
            #postBody = str(args)
            print "postBody: " + postBody
            contentLength = len(postBody)
            print "content-length: " + str(contentLength)

        path,host,port = self.parseURL(url)
        headerToSend = self.createRequestHeader(path,host,"POST")
        headerToSend+=('Content-Length: '+ str(contentLength) + '\r\n')
        headerToSend+=('Content-Type: application/x-www-form-urlencoded\r\n')
            
        clientSocket = self.connect(host,port)
        if (postBody != None):
            print "message sent: " + headerToSend + "\r\n" +postBody
            clientSocket.sendall(headerToSend + "\r\n" + postBody)
        else:
            clientSocket.sendall(headerToSend + "\r\n\r\n")
        httpResponse = self.recvall(clientSocket)
        #print httpResponse

        #data = self.recvall(clientSocket)
        code = self.get_code(httpResponse)
        headers= self.get_headers(httpResponse)
        body = self.get_body(httpResponse)

        #print "code: " + str(code)
        #print "headers: " + str(headers)
        #print "body: " + str(body)
        
        return HTTPResponse(int(code), body)

    def command(self,url ,command="GET" ,args=None):
        #path,host = self.parseURL(url)
        #headerToSend = self.createRequestHeader(path,host,command)
        #clientSocket = self.connect(host,80)
        #clientSocket.sendall(headerToSend + "\r\n\r\n")
        #httpResponse = self.recvall(clientSocket)
        #print httpResponse

        #data = self.recvall(clientSocket)
        #code = self.get_code(httpResponse)
        #headers= self.get_headers(httpResponse)
        #body = self.get_body(httpResponse)

        #print "code: " + str(code)
        #print "headers: " + str(headers)
        #print "body: " + str(body)


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
