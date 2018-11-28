'''
Created on Oct 30, 2018
@authors: Brandon Toups
'''

import datetime
import math
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
def evograph(kValToUpscaleTo):
    readGraph('../data/sf=1.txt')

    EdgeInstance.initialKVal = kValToUpscaleTo
    EdgeInstance.initialNumNodes = EdgeInstance.initialNumEdges - 1
    rangeEdges = EdgeInstance.initialNumEdges
    maxNumEdges = EdgeInstance.initialKVal * rangeEdges
    for EdgeInstance.currentNumEdges in range(EdgeInstance.initialNumEdges, maxNumEdges):
        readGraph('../data/sf=1.txt')
        vsvt = DETERMINE(EdgeInstance.currentNumEdges)
        WRITE(vsvt, EdgeInstance.currentNumEdges)
    
        
def WRITE(refvsvt, y):
    with open('../data/sf=1.txt','a') as openFile:
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
    # next k value if multiple of initial number of edges
    if EdgeInstance.currentNumEdges == EdgeInstance.initialNumEdges*EdgeInstance.currentKVal:
        EdgeInstance.currentKVal+=1
        
    if (EdgeInstance.currentKVal != int(y/EdgeInstance.initialNumEdges) + 1):
        EdgeInstance.currentKVal = int(y/EdgeInstance.initialNumEdges) + 1
    # x ~ U(0, (k-1)*|E|-1)
    EdgeInstance.x = h1(y)
    
    # if x < |E|:
    if EdgeInstance.x < EdgeInstance.initialNumEdges:
        # (vs,vt) = ex        
        EdgeInstance.vs = EdgeInstance.currentGraph['e' + str(EdgeInstance.x)][0]
        EdgeInstance.vt = EdgeInstance.currentGraph['e' + str(EdgeInstance.x)][1]
    else:
        # (vs,vt) = DETERMINE(ex)    
        vsvt = DETERMINE(EdgeInstance.x)
        if (EdgeInstance.currentKVal != int(y / EdgeInstance.initialNumEdges) + 1):
            EdgeInstance.currentKVal = int(y / EdgeInstance.initialNumEdges) + 1
        EdgeInstance.vs = vsvt[0]
        EdgeInstance.vt = vsvt[1]
    # if direction == 0
    # direction ~ U(0,1)
    if h2(y) == 0:
        # (REFSF=k(vs), vt)
        refvsvt = [ int(REFSF(1)), int(EdgeInstance.vt) ]
    else:
        # (vs,REFSF=k(vt))        
        refvsvt = [ int(EdgeInstance.vs) , int(REFSF(2)) ]
        
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
    EdgeInstance.currentNumEdges = edgeNum
    
    
   
# H(key) = ((key + 13) x 7)
# h1(y) determines the ID x of a parent edge ex of the edge ey
# Hash Function for U(0, (k-1)*|E|-1)

# h1 :key->[0,...,(k-1)*|E|-1] 
def h1(key):
    
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
        refIs = int(EdgeInstance.vt)
        return refIs + int(nodesOnLevel* (EdgeInstance.currentKVal-1))
    else:
        refIs = int(EdgeInstance.vs)
        return refIs + int(nodesOnLevel* (EdgeInstance.currentKVal-1))
    return refIs



def outputGraph():
    with open('../data/sf=1.txt', 'r') as fin:
        print (fin.read())

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
    
    
def runtimek2():
    print ('Running evograph(2) on sf=1.txt to test time complexity of a 2x upscale.')
    k2TimeTotal = 0
    numExecutions = 10 
    iterationTime = 0
    for iteration in range(0,numExecutions):
        startK2 = datetime.datetime.now()
        evograph(2)
        finishK2 = datetime.datetime.now()
        returnSF1ToOriginal()
        iterationTime = (finishK2 - startK2).microseconds
        print ('Run #' + str(iteration + 1) + '\ttook ' + str(iterationTime) + ' microseconds')
        k2TimeTotal += iterationTime
         
    print ('Total time executing ' + str(iteration+1) + ' runs upscaling to k=2: ' + str(k2TimeTotal) + ' microseconds')
    print ('Ave   time executing ' + str(iteration+1) + ' runs upscaling to k=2: ' + str(k2TimeTotal / (iteration+1)) + '  microseconds\n')
     
def runtimek3():
    print ('Running evograph(3) on sf=1.txt to test time complexity of a 3x upscale.')
    k3TimeTotal = 0
    numExecutions = 10 
    iterationTime = 0
    for iteration in range(0,numExecutions):
        startK3 = datetime.datetime.now()
        evograph(3)
        finishK3 = datetime.datetime.now()
        returnSF1ToOriginal()
        iterationTime = (finishK3 - startK3).microseconds
        print ('Run #' + str(iteration + 1) + '\ttook ' + str(iterationTime) + ' microseconds')
        k3TimeTotal += iterationTime
         
    print ('Total time executing ' + str(iteration+1) + ' runs upscaling to k=3: ' + str(k3TimeTotal) + ' microseconds')
    print ('Ave   time executing ' + str(iteration+1) + ' runs upscaling to k=3: ' + str(k3TimeTotal / (iteration+1)) + '  microseconds\n')

def runtimek4():
    print ('Running evograph(4) on sf=1.txt to test time complexity of a 4x upscale.')
    k4TimeTotal = 0
    numExecutions = 10 
    iterationTime = 0
    for iteration in range(0,numExecutions):
        startK4 = datetime.datetime.now()
        evograph(4)
        finishK4 = datetime.datetime.now()
        returnSF1ToOriginal()
        iterationTime = (finishK4 - startK4).microseconds
        print ('Run #' + str(iteration + 1) + '\ttook ' + str(iterationTime) + ' microseconds')
        k4TimeTotal += iterationTime
         
    print ('Total time executing ' + str(iteration+1) + ' runs upscaling to k=4: ' + str(k4TimeTotal) + ' microseconds')
    print ('Ave   time executing ' + str(iteration+1) + ' runs upscaling to k=4: ' + str(k4TimeTotal / (iteration+1)) + '  microseconds\n')
    
if __name__ == '__main__':
    returnSF1ToOriginal()
    
    print ('Running evograph.py\n')
    
    # print out original file 
    print ('Original graph (Gsf=1) is: ')
    with open('../data/original.txt', 'r') as fin:
        print (fin.read())
    
    print ('----------------------------------------\n')
    
    # Upscale to k=2
    print ('Upscaling original graph from k=1 to k=2: ')
    evograph(2) 
    outputGraph()
    
    print ('Compare this to the expected values in k=2 graph (../data/sf=2.txt):')
    print ('(tabs in this file used to more easily delineate between levels)')
    with open('../data/sf=2.txt', 'r') as fin:
        print (fin.read())
    
    print ('----------------------------------------\n')
    
    # Upscale to k=3
    print ('Upscaling original graph from k=1 to k=3: ')
    returnSF1ToOriginal()
    evograph(3)
    outputGraph()
    
    print ('Compare this to the expected values in k=3 graph (../data/sf=3.txt):')
    print ('(tabs in this file used to more easily delineate between levels)')
    with open('../data/sf=3.txt', 'r') as fin:
        print (fin.read())
    
    returnSF1ToOriginal()
    
    
    #Below is used to analyze time complexity 
    returnSF1ToOriginal()
    print ('\n\nNow testing time complexity. Averaging multiple runs.')
      
    # Runtime time complexity analysis
    print ('\t------------------------------------------')
    print ('\t\tAnalyzing Time Complexity')
    print ('\t------------------------------------------')
    runtimek2()
     
    runtimek3()

    
    runtimek4()

