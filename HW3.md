---
tags: "電腦網路導論"
title: "HW3"
---
# Homework#3
## Function Used
---
### GetAdjlist(filename)
- Goal: Return the adjacency list from the input file
- Steps:
    1. Open the file and split the lines, and combine these lines into a list.
    ```python=
    with open(filename,'r') as casefile:
        case = casefile.read()
    graphrows = case.split('\n')
    Out:['6',
    '0 3 -1 3 -1 -1',
    '3 0 8 -1 2 5',
    '-1 8 0 1 -1 -1',
    '3 -1 1 0 -1 -1',
    '-1 2 -1 -1 0 -1',
    '-1 5 -1 -1 -1 0']
    ```

    2. for each line in the list, also split it into each numbers(also change them into int) and combine them into a list.
    ```python=
    for i in range(len(graphrows)):
            a=graphrows[i].split(' ')
            for j in range(len(a)):
                a[j]=int(a[j])
    #When i=1, a=[0, 3, -1, 3, -1, -1]
    ```
    3. For each 'a', we append it into adjacency list, finally we get an adjacency list like this
    ```python= 
    #Adjlist
    [[6],
    [0, 3, -1, 3, -1, -1],
    [3, 0, 8, -1, 2, 5],
    [-1, 8, 0, 1, -1, -1], 
    [3, -1, 1, 0, -1, -1], 
    [-1, 2, -1, -1, 0, -1], 
    [-1, 5, -1, -1, -1, 0]]
    
    #[0, 3, -1, 3, -1, -1]is a dis_list
    ```
    
---
### findnextnode(dis,inf_dis)


- Goal: Return a dict from a dis_list which look like {node:the distance to the node...}
    - inf_dis is True: only return the node distance!=0
    - inf_dis is False: only return the node distance!=(0 or -1)
```python=
#Example
S=[0, 3, -1, 3, -1, -1]

findnextnode(S,True)
Out:{2: 3, 3: -1, 4: 3, 5: -1, 6: -1}

findnextnode(S,False) 
Out:{2: 3, 4: 3}
```
- Step
    - Create a dict,then append a (index+1):(distance) for each node satisfied the distance request
---
### Dijkstra_algorithm(Adjlist)
![](https://i.imgur.com/QboLWKn.png)
- Goal: return a dict{'Adjlist':Adjlist , 'nextrouter':nextrouter}.
- Adjlist is a new distance list with the information of the shortest distance.
- nextrouter is a list with the information of the next router. 


- Steps by Python
    
    - Step 1: take a new node from Q and get its distance list
        
        - Adjlist(list): The input
        - Graphsize(int): The number of the routers
        - nextrouter(list): Record the next router to archeive the closest path. The initial value is default to be the target node.
        ```python=
        #Example
            [[None],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6], 
            [1, 2, 3, 4, 5, 6], 
            [1, 2, 3, 4, 5, 6], 
            [1, 2, 3, 4, 5, 6], 
            [1, 2, 3, 4, 5, 6]]
        ```
        - Q(set): The queue contains the nodes that hadn't been changed, the initial value is ```{1,2,..,last router}```
        ```python=
        while Q:
            nownode = Q.pop()
            dis=Adjlist[nownode]

        #Example
        '''
        Q={1,2,3,4,5,6}
        nownode = 2
        dis = [3, 0, 8, -1, 2, 5]
        '''
        ```
    - Step2: Find every node and its distance (without itself)  
        - c(dict): other nodes the nownode can arrive(without inf distance)
        ```python= 
            c=findnextnode(dis,False)
        
        #Example
        '''
        c = {1: 3, 3: 8, 5: 2, 6: 5}
        '''
        ```
    - Step3: Find the closest node in c. Since there isn't any shorter way than directly go to the closest node, so the next router must remain the same (as the nextrouter records)  
        - Explanation: Assume that we already found the shortest path so far from Node7 -> Node5 before, and it looks like Node7 -> Node3 -> ... -> Node5. We have already recorded the next router=3.
        - When we discover the Node7 -> Node5 is the shortest path among the other nodes, than we couldn't find any node X that satisfied **Node7 -> NodeX -> Node5 is shorter** because the distance of Node7 -> NodeX is already more than  Node7 -> Node5. So we can make sure the shortest path from Node7 to Node5 is already found and won't be revised later.
        ```python= 
            while c.keys():
                closestnode = min(c, key=c.get)
                #get the distance from the closestnode to other node
                closestnodepath = findnextnode(Adjlist[closestnode],False)
            '''
            c = {1: 3, 3: 8, 5: 2, 6: 5}
            closestnode = 5
            closestnodepath={2: 2}
            '''    
        ```
    - Step4: Check for every other nodes T, if **dis(nownode -> closestnode ->...-> NodeT) < dis(nownode -> ...->T)**, update the distance that passes through the closestnode, and set the next router to closestnode.(Though this code is not efficient enough: we may repeat compare the distance that we already know it is the shortest, but the benefit is the code can be less complexity)
        ```python=
 
                # Node i should be reachable by closestnode
                for i in closestnodepath.keys():
                # if dis(nownode -> closestnode ->...-> NodeT) < dis(nownode -> ...->T)
                    if closestnodepath[i]+c[closestnode]<dis[i-1] or dis[i-1]==-1:
                        # Update the new distance to c and dis
                        c[i]=closestnodepath[i]+c[closestnode]
                        dis[i-1]=c[i]
                        #Update the closest_node to nextrouter
                        nextrouter[nownode][i-1]= nextrouter[nownode][closestnode-1]
        ```
    - Step5: When finishing the check of the closest node and update all the distance, we can delete it from c and take a new closest node from c and repeat the Step3~5 until c is empty.
        - The reason is "If the closest node can't become one of the routers in every subpath from NodeS to NodeF in its checking loop, then it will never become one of the routers in the every subpath from NodeS to NodeF." So we can exclude it after we finish checking the closest node.
        - How can we promise the statement? We will use the basic logic: If the closest node is one of the routers in the subpaths from NodeS to NodeF, then it must become one of the routers in the subpaths from NodeS to NodeF in its own loop.
        - Suppose the closest node named NodeC, and the closest path contains NodeC
            - Suppose the shortest path look like this 
            - **S ->...-> C -> B1 -> B2 ->...->Bn -> F**
            - Because we have already known the shortest path S->C before its own turn, so we can omit it like this:
            - **S -> C -> B1 -> B2 ->...->Bn -> F**
            - When in NodeC's loop, C will compare dis(S -> C) + dis(C -> B1) < dis(S -> B1)
            - Because dis(S -> C) & dis(C -> B1) is known(C directly go to B1 is the shortest path represents it is already written in adjacency list), so the statement will always be true, and C will be in the S -> B1 subpath
        ```python=
                del c[closestnode]
        ```
    
    
    
    - Step6: When c is empty, take a new node from Q(which is not been checked) ,repeat Step1-5 until Q is empty. 
    
    - Step7: We have finished the algorithm, and the last thing we have to do is check every distance in Adjlist. If we find an distance==-1, it means there is no path to go through these two nodes, so we should set the corresponding element in nextrouter to -1, which means there is no next router to go to the target node.
        ```python=
        for i in range(1,Graphsize+1):
            for j in range(Graphsize):
                if Adjlist[i][j]==-1:
                    nextrouter[i][j]=-1
        return {'Adjlist':Adjlist , 'nextrouter':nextrouter}
        ```

---
### removerouter(Adjlist,router)
- Goal: Reutrn a new adjacency list which removes the target router.
- Steps:
    ```python= 
    #Example remove router2
    [[6],
    [0, 3, -1, 3, -1, -1],
    [3, 0, 8, -1, 2, 5],
    [-1, 8, 0, 1, -1, -1], 
    [3, -1, 1, 0, -1, -1], 
    [-1, 2, -1, -1, 0, -1], 
    [-1, 5, -1, -1, -1, 0]]
    ```
    1. ```Adjlist[i][router-1]=-1```
     (i for every routers)
    ```python= 
    [[6],
    [0,  '-1', -1,  3, -1, -1],
    [3,  '-1',  8, -1,  2,  5],
    [-1, '-1',  0,  1, -1, -1], 
    [3,  '-1',  1,  0, -1, -1], 
    [-1, '-1', -1, -1,  0, -1], 
    [-1, '-1', -1, -1, -1,  0]]
    ```
    2. ```Adjlist[router][j]=-1```
    (j for every routers)
    ```python= 
    [[6],
    [0,  -1, -1,  3, -1, -1],
    ['-1','-1','-1','-1', '-1','-1'],
    [-1, -1,  0,  1, -1, -1], 
    [3,  -1,  1,  0, -1, -1], 
    [-1, -1, -1, -1,  0, -1], 
    [-1, -1, -1, -1, -1,  0]]
    ```
    3. ```Adjlist[router][router-1]=0```
    ```python= 
    [[6],
    [0,  -1, -1,  3, -1, -1],
    [-1, '0', -1, -1, -1, -1],
    [-1, -1,  0,  1, -1, -1], 
    [3,  -1,  1,  0, -1, -1], 
    [-1, -1, -1, -1,  0, -1], 
    [-1, -1, -1, -1, -1,  0]]
    ```
----
### Writetxt(Adjlist, filename,rmrouter)
- Goal: Run the Dijkstra's algorithm to the Adjlist and write a txt file with requested file name and content. 
- Variable:
    - Adjlist = Original adjacency list read from input text file
    - filename = The filename
    - rmrouter = A list records the routers already been removed

- Steps
    1. Get the Adjlist and nextrouter by doing the Dijkstra's algorithm to the original Adjlist.
    2. Open a txt with requested filename and write the content. (Skip the routers that have been removed) 

----
## Input Commands


### 'lf {inputname}.txt'
- Steps
    1. Get the adjacency list(Using **GetAdjlist**) from ==inputname.txt==
    2. Write the adjacency list into ==log.txt==
    3. Write the inputname into  ==filename.txt==
    4. Write an empty list into  ==router_rec.txt==
---
### 'rm r{router number}'
- Steps
    1. read ==log.txt== and eval to get the Adjlist
    2. **removerouter**(Adjlist, router number)
    3. write the ==log.txt== with the new Adjlist
    4. add the remove router number to ==router_rec.txt==
---
### 'of'
- Steps
    1. read ==log.txt== and eval to get the Adjlist
    2. read ==router_rec.txt== and eval to get the rmrouter
    3. read ==filename.txt== to get the filename and  modify it
    4. **Writetxt**(Adjlist,filename,rmrouter)
    
    
    