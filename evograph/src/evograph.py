'''
Created on Oct 30, 2018

@authors: Brandon Toups
'''

import sys as sys
sys.setrecursionlimit(8)

# Algorithm 1 EvoGraph
# Input G = (V, E) // original graph
#       k // scale factor
# 
# parallel for y in [|E|:k * |E| - 1] do
#     (vs,vt) <- DETERMINE(ey)
#     WRITE (vs , vt );
# ---------------------------------
# MEA - Memory-efficient edge attachment
# DETERMINE(ey) :
#     x ~ U(0, (k-1)*|E|-1)
#     direction ~ U(0,1)
# if x < |E|:
#     (vs,vt) = ex
# else:
#     DETERMINE(ex)
# 
# if direction = 0
#     (REFSF=k(vs),vt)
# else:
#     (vs,REFSF=k(vt))
# ----------------------------------
# Analysis:
# Following two hash functions where H(key) = ((key + 13) x 7)
# h1(y) determines the ID x of a parent edge ex of the edge ey
# Hash Function for U(0, (k-1)*|E|-1)
# h1 :key->[0,...,(k-1)*|E|-1]
#
# h2(y) determines a direction of the edge ey (direction 0 means towards 
# the inside of the graph, while direction 1 means towards the outside of graph.
# Hash Function for U(0,1)
# h2 : key -> [0,1]
# 
# ex: attaching e6 to GSF=2
#     H(6) = ((6+13) x 7) = 133
#     h1(6) = 133mod(2-1) * 6 = 1
#     h2(6) = 133mod2 = 1
# thus e1 = (v0,v2) is picked as a parent edge and e6 is determined as (v0,REFSF=2(v2)) = (v0,v7)
# 

# Program Code 
class EdgeInstance(object):
    currentGraph = {}
    currentNumEdges = 0
    currentNumNodes = 0
    initialNumEdges = 0
    initialNumNodes = 0
    y = 0
    x = 0
    direction = 0
    vs = 0
    vt = 0
    initialKVal = 0
    currentKVal = 2

# Algorithm 1 EvoGraph
# Input G = (V, E) // original graph
#       k          // scale factor
# 
# parallel for y in [|E|:k*|E|-1] do 
#     (vs,vt) <- DETERMINE(ey);
#     WRITE (vs , vt );
def evograph():
    readGraph('../data/sf=1.txt')
    EdgeInstance.initialKVal = 3
    EdgeInstance.initialNumNodes = EdgeInstance.initialNumEdges - 1
    
    # initialized to 6 to make sure there is 
    rangeEdges = EdgeInstance.initialNumEdges
    for EdgeInstance.currentNumEdges in range(EdgeInstance.initialNumEdges, (EdgeInstance.initialKVal * rangeEdges)):
        readGraph('../data/sf=1.txt')
        refvsvt = DETERMINE(EdgeInstance.currentNumEdges)
        print 'About to write ' + str(refvsvt)
        WRITE(refvsvt, EdgeInstance.currentNumEdges)
    
        
def WRITE(refvsvt, y):
    with open('../data/sf=1.txt','a') as openFile:
        print 'Writing now ' + str(refvsvt) + ' to the file \n'
        openFile.write( str(refvsvt[0]) + '\t' + str(refvsvt[1])  + '\t#e' + str(y) + '\n')
        

        
# DETERMINE(ey) :
#     x ~ U(0, (k-1)*|E|-1)
#     direction ~ U(0,1)
# if x < |E|:
#     (vs,vt) = ex
# else:
#     DETERMINE(ex)
# 
# if direction = 0
#     (REFSF=k(vs),vt)
# else:
#     (vs,REFSF=k(vt))
def DETERMINE(y):
    
    if EdgeInstance.currentNumEdges == EdgeInstance.initialNumEdges*EdgeInstance.currentKVal:
        print 'incrementing k at ' + str(y)
        EdgeInstance.currentKVal+=1
        print 'k is now at k='+str(EdgeInstance.currentKVal)
    
    # x ~ U(0, (k-1)*|E|-1)
    EdgeInstance.x = h1(y)
    
    
    # direction ~ U(0,1)
    EdgeInstance.direction = h2(y)

    # if x < |E|:
    if EdgeInstance.x < EdgeInstance.initialNumEdges:
        # (vs,vt) = ex        
        EdgeInstance.vs = EdgeInstance.currentGraph['e' + str(EdgeInstance.x)][0]
        EdgeInstance.vt = EdgeInstance.currentGraph['e' + str(EdgeInstance.x)][1]
    else:
        # (vs,vt) = DETERMINE(ex)
        print '\nRECURSION HAPPENING\n'     
        vsvt = DETERMINE(EdgeInstance.x)
        print 'After recursion call, vsvt is ' + str(vsvt)
        EdgeInstance.vs = vsvt[0]
        EdgeInstance.vt = vsvt[1]
        
    
    # if direction == 0
    if EdgeInstance.direction == 0:
        # (REFSF=k(vs), vt)
        refvsvt = [ int(REFSF(1)), int(EdgeInstance.vt) ]
    else:
        # (vs,REFSF=k(vt))        
        refvsvt = [ int(EdgeInstance.vs) , int(REFSF(2)) ]
    print 'Program writing ' + str(refvsvt) + ' to the file'
    return refvsvt
    
def readGraph(inputFile):
    with open(inputFile) as f:
        edges = {}
        lines = f.readlines()
        edgeNum = 0
        for line in lines:
            vs = line.split()[0]
            vt = line.split()[1]
            edges['e' + str(edgeNum)] = (vs,vt)
            edgeNum+=1
    if EdgeInstance.currentNumEdges == 0:
        EdgeInstance.initialNumEdges = edgeNum
    EdgeInstance.currentGraph = edges
    #EdgeInstance.currentNumEdges = edgeNum
    
    
   
# H(key) = ((key + 13) x 7)
# h1(y) determines the ID x of a parent edge ex of the edge ey
# Hash Function for U(0, (k-1)*|E|-1)
# h1 :key->[0,...,(k-1)*|E|-1] 
def h1(key):
    
    print 'key ' + str(key)
    print 'currentkval ' + str(EdgeInstance.currentKVal)
    #===========================================================================
    print 'calculating'
    print 'h1 calculated as ' + str(H(key) % ((EdgeInstance.currentKVal-1) * (6)))
    return H(key) % ((EdgeInstance.currentKVal-1) * (6))
    
    
# h2(y) determines a direction of the edge ey (direction 0 means towards 
# the inside of the graph, while direction 1 means towards the outside of graph.
# Hash Function for U(0,1)
# h2 : key -> [0,1]
def h2(key):
    return H(key) % 2

def H(key):
    return ((key + 13) * 7)


def REFSF(whichIndex):
    refIs = 0
    nodesOnLevel = EdgeInstance.initialNumNodes
    if whichIndex == 2:
        print '\nindex' + str(whichIndex)
        refIs = int(EdgeInstance.vt)
        print str(EdgeInstance.vs) + ' ' + str(EdgeInstance.vt)
        print 'current num edges ' + str(EdgeInstance.currentNumEdges)
        print 'Nodes on level ' + str(nodesOnLevel)
        print 'Current k val: ' + str(EdgeInstance.currentKVal)
        print 'initiallly refIs: ' + str(refIs)
        print 'calculated' + str(refIs + int(nodesOnLevel* (EdgeInstance.currentKVal-1)))
        
        return refIs + int(nodesOnLevel* (EdgeInstance.currentKVal-1))
    else:
        print '\nindex' + str(whichIndex)
        refIs = int(EdgeInstance.vs)
        print str(EdgeInstance.vs) + ' ' + str(EdgeInstance.vt)
        print 'current num edges ' + str(EdgeInstance.currentNumEdges)
        print 'Nodes on level ' + str(nodesOnLevel)
        print 'Current k val: ' + str(EdgeInstance.currentKVal)
        print 'initiallly refIs: ' + str(refIs)
        print 'calculated ' + str(refIs + int(nodesOnLevel* (EdgeInstance.currentKVal-1)))
    
        return refIs + int(nodesOnLevel* (EdgeInstance.currentKVal-1))
    
    return refIs



def outputGraph():
    with open('../data/sf=1.txt', 'r') as fin:
        print fin.read()

def returnSF1ToOriginal():
    # opens original file
    file1 = open("../data/original.txt" , "r")
    # opens new file
    file2 = open("../data/sf=1.txt" , "w")
    #for each line in old file
    for line in file1:
        #write that line to the new file
        file2.write(line)
    #close file 1
    file1.close()
    #close file2
    file2.close()
    
if __name__ == '__main__':
    returnSF1ToOriginal()
    evograph() 
    outputGraph()
    
    

    