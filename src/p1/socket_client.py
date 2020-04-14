#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket

HOST, PORT = '127.0.0.1', 7777
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    response = input(s.recv(1024).decode()).encode()
    
    s.send(response)
    


# In[3]:





# In[ ]:




