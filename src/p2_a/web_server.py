#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import socket module
from socket import *
import time
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
# TODO start
HOST, PORT = '140.112.240.13', 80
serverSocket.bind((HOST,PORT))

# TODO in end
while True:
    #Establish the connection
    print('Ready to serve...')
    # TODO start
    serverSocket.listen(5)  
    # TODO end
    try:
        # Receive http request from the clinet
        # TODO start
        connectionSocket, address = serverSocket.accept()
        message = connectionSocket.recv(1024).decode()
    
        # TODO end
        print(message)
        if message == '':
            filename = '  '
        else:
            filename = message.split()[1]
            print(filename)
        f = open(filename[1:],encoding="utf-8")
        
        # Read data from the file that the client requested
        # Split the data into lines for future transmission 
        # TODO start
        outputdata = f.readlines()
        
        # TODO end
        #print(outputdata)

        #Send one HTTP header line into socket
        # TODO start
        
        # send HTTP status to client
        connectionSocket.send('HTTP/1.1 200 OK\n'.encode())
  
        # send content type to client
        connectionSocket.send('Content-Type: text/html\n\n'.encode())
        # TODO end
        
        # Send the content of the requested file to the client  
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        # TODO start
        connectionSocket.send("HTTP/1.1 404 Not Found\n".encode())
        print('404checkpoint')
        # TODO end

        #Close client socket
        # TODO start
        connectionSocket.close()
        # TODO end
serverSocket.close()
sys.exit() #Terminate the program after sending the corresponding data


# In[ ]:




