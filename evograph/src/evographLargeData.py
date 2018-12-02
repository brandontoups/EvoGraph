'''
Created on Oct 30, 2018
@authors: Brandon Toups
'''

import datetime
from multiprocessing import Pool
import sys


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
def parallel(kValToUpscaleTo, processes):
    readGraph('../data/toy.txt')

    EdgeInstance.initialKVal = kValToUpscaleTo
    EdgeInstance.initialNumNodes = EdgeInstance.initialNumEdges - 1
    rangeEdges = EdgeInstance.initialNumEdges
    maxNumEdges = EdgeInstance.initialKVal * rangeEdges
        
    # parallelized for-loop using multiprocessing functionality
    p = Pool(processes=processes)
    iterRange = list(range(EdgeInstance.initialNumEdges, maxNumEdges))
    p.map(EvoGraph, iterRange)
    p.close()

# What is inside the parallelized for loop
def EvoGraph(currentNumEdges):
    readGraph('../data/toy.txt')
    vsvt = DETERMINE(currentNumEdges)
    WRITE(vsvt, currentNumEdges)
    
def parallelToy(kValue, processes):
    
    #===========================================================================
    # print 'Original graph (Gsf=1) is: ' # print out original file
    # with open('../data/toy.txt', 'r') as fin:
    #     print fin.read()
    # print '----------------------------------------\n'
    #===========================================================================
    
    # Upscale to k=2
    startK2 = datetime.datetime.now()
    parallel(kValue, processes)
    finishK2 = datetime.datetime.now()
    iterationTime = (finishK2 - startK2).seconds
    print str(processes) + ' thread(s)\t' + 'Execution time: ' + str(iterationTime) + ' seconds'
    returnToyToOriginal()
        
def WRITE(refvsvt, y):
    with open('../data/toy.txt','a') as openFile:
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
    
    return H(key) % ((EdgeInstance.currentKVal-1) * (EdgeInstance.initialNumEdges))
    
    
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



def outputGraphToy():
    with open('../data/toy.txt', 'r') as fin:
        print (fin.read())


def returnToyToOriginal():
    #print 'For repeatability, the file toy is now being returned to its original state'
    # opens original file
    file1 = open("../data/toyOriginal.txt" , "r")

    # opens new file
    file2 = open("../data/toy.txt" , "w")
    #for each line in old file
    for line in file1:
        #write that line to the new file
        file2.write(line)
    #close file 1
    file1.close()
    #close file2
    file2.close()
    

    
def outputOriginalToy():
    print ('Running evograph.py\n')
    
    # print out original file 
    print ('Original graph (Gsf=1) is: ')
    with open('../data/toyOriginal.txt', 'r') as fin:
        print (fin.read())
    
    print ('----------------------------------------\n')

if __name__ == '__main__':
    
    # make sure that sf=1.txt is a clean, original before running
    returnToyToOriginal()
    
    print '----------------'
    print 'Upscaling from k=1 to k=2'
    # run evograph with a parallelized for loop
    # parallel( kValue, numProcesses)
    parallelToy(2,1)
    parallelToy(2,2)
    # parallelToy(2,4)
    # parallelToy(2,8)
    # parallelToy(2,16)
    # parallelToy(2,32)
    # parallelToy(2,64)
    # parallelToy(2,128)
    # parallelToy(2,256)
    # parallelToy(2,511)    
    #===========================================================================

    print '----------------'
    