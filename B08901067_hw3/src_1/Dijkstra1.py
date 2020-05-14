#!/usr/bin/env python
# coding: utf-8

# In[32]:


import sys
import copy
def GetAdjlist(filename):
    with open(filename,'r') as casefile:
        case = casefile.read()
        graphrows = case.split('\n')
        Adjlist=[]
        for i in range(len(graphrows)):
            a=graphrows[i].split(' ')
            for j in range(len(a)):
                a[j]=int(a[j])
            Adjlist.append(a)
        return Adjlist
    



def findnextnode(dis,inf_dis):
    nextnode={}
    if inf_dis==True:
        for i in range(len(dis)):  #i從0到n-1,node=i+1
            if dis[i]!=0:
                nextnode[i+1]=dis[i]
                
    if inf_dis==False:
        for i in range(len(dis)):  #i從0到n-1,node=i+1
            if dis[i]!=0 and dis[i]!=-1:
                nextnode[i+1]=dis[i]
    return nextnode




def Dijkstra_algorithm(Adjlist):
    Adjlist=copy.deepcopy(Adjlist)
    Graphsize = Adjlist[0][0]
    Q=set(i for i in range(1,Graphsize+1))
    nextrouter=[[None]]+[[i for i in range(1,Graphsize+1)] for j in range(Graphsize)]
    
    while Q:
        nownode = Q.pop()
        dis=Adjlist[nownode]
        c=findnextnode(dis,False)
        
        while c.keys():
            closestnode = min(c, key=c.get)
            closestnodepath = findnextnode(Adjlist[closestnode],False)
            
            for i in closestnodepath.keys():
                
                if closestnodepath[i]+c[closestnode]<dis[i-1] or dis[i-1]==-1:
                    c[i]=closestnodepath[i]+c[closestnode]
                    dis[i-1]=c[i]
                    nextrouter[nownode][i-1]= nextrouter[nownode][closestnode-1]
            
            del c[closestnode]
    
    for i in range(1,Graphsize+1):
        for j in range(Graphsize):
            if Adjlist[i][j]==-1:
                nextrouter[i][j]=-1
    
    return {'Adjlist':Adjlist , 'nextrouter':nextrouter}





def Writetxt(Adjlist, filename,rmrouter):
    Graphsize=Adjlist[0][0]
    D_Adjlist = Dijkstra_algorithm(Adjlist)['Adjlist']
    nextrouter = Dijkstra_algorithm(Adjlist)['nextrouter']
    with open(filename,'w') as f:
        f.write("")
    with open(filename,'a') as f: 
        for i in range(1,Graphsize+1):
            
            if i not in rmrouter:
                
                f.write(f"Routing table of router {i}:\n")
                for j in range(Graphsize):
                    if (j+1) not in rmrouter:
                        f.write(f'{D_Adjlist[i][j]} {nextrouter[i][j]}\n')

def removerouter(Adjlist,router):
    Adjlist = copy.deepcopy(Adjlist)
    Graphsize=Adjlist[0][0]
    for i in range(1,Graphsize+1):  #The distance other router->remove router=-1 
        Adjlist[i][router-1]=-1
    for j in range(len(Adjlist[router])):  #The distance remove router->other router=-1 
        Adjlist[router][j]=-1
    Adjlist[router][router-1]=0  #remove router->remove router=0
    return Adjlist


# In[31]:


def main():    
    if sys.argv[1]=='lf':
        load = GetAdjlist(sys.argv[2])

        with open ('log.txt','w') as logf:
            logf.write(str(load)) #write adjlist into log.txt
        with open ('file_name.txt','w') as fname:
            fname.write(sys.argv[2][:-4])
        with open ('router_rec.txt','w') as f:
            f.write('[]')


    if sys.argv[1]=='rm':
        with open ('log.txt','r') as logf:
            OpAdjlist=eval(logf.read())


        rm = removerouter(OpAdjlist,int(sys.argv[2][1:]))
        with open ('log.txt','w') as logf:
            logf.write(str(rm)) #write adjlist into log.txt
        with open ('router_rec.txt','r') as f:
            a=eval(f.read())
            a.append(int(sys.argv[2][1:]))
        with open ('router_rec.txt','w') as f:
            f.write(str(a))


    if sys.argv[1]=='of':
        with open ('log.txt','r') as logf:
            OpAdjlist=eval(logf.read())
        with open ('router_rec.txt','r') as f:
            rmrouter = eval(f.read())

        with open ('file_name.txt','r') as fname:
            Opfilename = fname.read()+'_out1.txt'

        Writetxt(OpAdjlist,Opfilename,rmrouter)

        
main()


# In[30]:





# In[28]:





# In[ ]:




