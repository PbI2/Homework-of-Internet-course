#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from socket import *
import sys
import time
import threading


if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server & Web server.')
    sys.exit(2)
# Environment : Python 3.8
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
tcpSerSock.bind(('140.112.240.13', 8080))
tcpSerSock.listen(5)
# Fill in end.
def routine(tcpCliSock):
    # Strat receiving data from the client
    message = tcpCliSock.recv(1024).decode('utf-8')
    print(message)
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "r", encoding = 'utf8')
        outputdata = f.read()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type: text/html\r\n\r\n".encode())
        # Fill in start.
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())
        tcpCliSock.send("\r\n".encode())
        tcpCliSock.close()
        # Fill in end.
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        print('IOError')
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            try:
                # Connect to the socket to port 80
                c.connect((sys.argv[1],80))

                # ask port 127.0.0.1:80 for the file requested by the client
                request = "GET " + "/" + filename + " HTTP/1.1\n\n"
                c.send(request.encode())
                # receive the response 
                # Fill in start.
                response = '123'
                content = ''
                
                while response!='':
                    response = c.recv(1024).decode()
                    content += response
                contentlist = content.split('\n')
                
                
                if contentlist[0] == 'HTTP/1.1 404 Not Found':
                    tcpCliSock.send("HTTP/1.1 404 Not Found\n".encode())
                    print('404')
                
                else:
                    for i in range(len(contentlist)):
                        if contentlist[i]=='':
                            contentlist = contentlist[i+1:]
                            break

                    html_content = '\n'.join(contentlist)

                    # Fill in end.
                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket and the corresponding file in the cache
                    tmpFile = open("./" + filename,"w",encoding = 'utf8')
                    # Fill in start.

                   
                    # Fill in end.

                    tmpFile.write(html_content)
                    tmpFile.close()
                    tmpFile = open("./" + filename,"r",encoding = 'utf8')

                    outputdata = tmpFile.read()

                    response = 'HTTP/1.0 200 OK\r\n\r\n' + outputdata
                    tcpCliSock.send(response.encode())

            except:
                print("Illegal request")
            c.close()
        else:
            # HTTP response message for file not found
            # Fill in start.
            tcpCliSock.send("HTTP/1.1 404 Not Found\n".encode())
            # Fill in end.
    # Close the client and the server sockets. For testing multi-user, you should comment the tcpCliSock.close()
    tcpCliSock.close()

# Fill in start. Change this part, such that multi-users can connect to this proxy server
'''
while True:
    print('Ready to serve...')
    t=[0]*5
    for i in range(5):
        tcpCliSock, addr = tcpSerSock.accept()
        print('Received a connection from:', addr)
        t[i] = threading.Thread(target = routine(tcpCliSock))
        t[i].start()
    for i in range(5):
        t[i].join()
    print('OK')
tcpSerSock.close()
'''
# Fill in end.
while True:
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    tcpThread = threading.Thread(target = routine, args=(tcpCliSock,))
    #routine(tcpCliSock)
    tcpThread.start()
tcpSerSock.close()


# In[ ]:





# In[ ]:





# In[ ]:




