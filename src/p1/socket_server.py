#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket
import copy

class matrix():
    def __init__(self,rows):
        self.rows = rows
       
        self.columns = []
        for i in range(len(self.rows[0])):
            column=[]
            for j in range(len(self.rows)):
                column.append(self.rows[j][i])
            self.columns.append(column)
        self.rownum = len(rows)
        self.columnnum = len(self.columns)
        if self.rownum == self.columnnum:
            self.square = True
        else: self.square = False
        
    def __str__(self):
        return str(self.rows)
    
    def slicem(self,remrow,remcolumn):
        r=copy.deepcopy(self.rows)
        
        for i in range(len(r)):
            
            del r[i][remcolumn]
        del r[remrow]
        
        
        
        return matrix(r)
    
    def __mul__(self,other):
        
        if self.columnnum!=other.rownum:
            return 'The row and column numbers are not correct.'

        def dot(v1,v2):
            c=0
            for i in range(len(v1)):
                c+=v1[i]*v2[i]
            return c        
        m=[]
        for i in range(len(self.rows)):
            a=[]
            for j in range(other.columnnum):
                num=dot(self.rows[i],other.columns[j])
                a.append(num)
            m.append(a)
        return matrix(m)

    
    def det(self):
        if self.square == False:
            return 'It is not a square matrix.'
        if self.rownum == 1:
            return self.rows[0][0]
        c=0
        for i in range(len(self.rows[0])):
    
            comp=self.slicem(0,i)
            c+=(-1)**i * self.rows[0][i] * comp.det()
        return c
    
    def adj(self):
        if self.square == False:
            return 'It is not a square matrix.'
        if self.rownum == 1:
            return 'The order is 1.'
        
        #ad=[[None]*self.rownum]*self.rownum
        ad=[]
        for i in range(self.rownum):
            a=[]
            for j in range(self.rownum):
                a.append((-1) ** (i+j) * self.slicem(j,i).det())
            ad.append(a)    
        

        return matrix(ad)
    
    def inverse(self):
        if self.square == False:
            return 'It is not a square matrix.'
        if self.rownum == 1:
            return 'The order is 1.'
        r=self.adj().rows
        for i in range(len(r)):
            for j in range(len(r)):
                r[i][j] /= self.det()
                r[i][j] = float('%.3f' %r[i][j])
        return matrix(r)
    
    def rep(self):
        r=copy.deepcopy(self.rows)
        for i in range(len(r)):
            r[i]=str(r[i])
            
        s='\n'.join(r)
        return s
        
    

def math_function(mode, string):
    if mode == 'basic':
        ##"5 * 3" 
        comp = string.split(" ")
        fn = eval(comp[0])
        op = comp[1]
        sn = eval(comp[2])
        if op == '+': return fn+sn
        if op == '-': return fn-sn
        if op == '*': return fn*sn
        if op == '/': return fn/sn
    
    if mode == 'det':
        return matrix(eval(string)).det()
    if mode == 'adj':
        return matrix(eval(string)).adj()
    if mode == 'inv':
        return matrix(eval(string)).inverse()
    if mode == 'mul':
        t=string.split('*')
        
        a=matrix(eval(t[0]))
        b=matrix(eval(t[1]))
        
        return a*b
    
    if mode == 'power':
        t = string.split('**')
        a = matrix(eval(t[0]))
        power = eval(t[1])
        if type(power) != int or power<=0:
            return 'non positive power is not allowed'
        c=matrix(a.rows)
        for i in range(power-1):
            c*=a
        return c
   

# Specify the IP addr and port number 
# (use "127.0.0.1" for localhost on local machine)
# Create a socket and bind the socket to the addr
# TODO start
HOST, PORT = '127.0.0.1', 7777
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
# TODO end

while(True):
    # Listen for any request
    # TODO start
    s.listen(1)
    # TODO end
    print("The Grading server for HW2 is running..")

    while(True):
        # Accept a new request and admit the connection
        # TODO start
        client, address = s.accept()
        # TODO end
        print(str(address)+" connected")
        try:
            while (True):
                client.send(b"Welcome to the calculator server. Input your problem ?\n")
                # Recieve the data from the client and send the answer back to the client
                # Ask if the client want to terminate the process
                # Terminate the process or continue
                # TODO start
                data = client.recv(1024).decode()
                
                if data == 'matrix':
                    client.send(f"Please input the code to choose the mode:\ndet mul adj inv power\n".encode())
                    
                    mode = client.recv(1024).decode()
                    
                    client.send(f"Please input the problem\n".encode())
                    
                    data = client.recv(1024).decode()
                    print(data)
                    try:
                        answer = math_function(mode, data)
                        print(answer)
                        if type(answer) == matrix:
                            answer = answer.rep()
                        
                        client.send(f'{answer}\nDo you have any question?(Y/N)\n'.encode())
                    except:
                        
                        client.send(f'Error!\nDo you have any question?(Y/N)\n'.encode())
                
                else: 
                    try:
                        answer = math_function('basic', data)
                        client.send(f'{answer}\nDo you have any question?(Y/N)\n'.encode())
                    except:
                        client.send(f'Error!\nDo you have any question?(Y/N)\n'.encode())
                
                
                data = client.recv(1024)
                check = data.decode()
                
                if check == 'Y' or check == 'y':
                    continue
                elif check == 'N' or check == 'n':
                    print(f'the connection from {address} is closed')
                    client.close()
                    break
                # TODO end
    
        except ValueError:
            print("except")


# In[ ]:





# In[ ]:




