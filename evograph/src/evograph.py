'''
Created on Oct 30, 2018

@authors: Brandon Toups
'''


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


# Algorithm 1 EvoGraph
# Input G = (V, E) // original graph
#       k          // scale factor
# 
# parallel for y in [|E|:k*|E|-1] do 
#     (vs,vt) <- DETERMINE(ey);
#     WRITE (vs , vt );
def evograph():
    graph, numberInitialEdges = edgesFromFile('../data/sf=1.txt')
    kScalar = 2
    upscaledGraph = {}
    
    for y in range(numberInitialEdges, ((kScalar * numberInitialEdges) - 1)):
        ey = graph['e'+y]
        upscaledGraph['e' + y] = DETERMINE(graph, numberInitialEdges, graph['e' + y])
    
    print upscaledGraph
    
def edgesFromFile(inputFile):
    with open(inputFile) as f:
        edges = {}
        lines = f.readlines()
        edgeNum = 0
        for line in lines:
            vs = line.split()[0]
            vt = line.split()[1]
            edges['e' + str(edgeNum)] = (vs,vt)
            edgeNum+=1
    return edges, edgeNum
   
   
# H(key) = ((key + 13) x 7)
# h1(y) determines the ID x of a parent edge ex of the edge ey
# Hash Function for U(0, (k-1)*|E|-1)
# h1 :key->[0,...,(k-1)*|E|-1] 
def h1(key, k):
    return H(key) % ((k-1) * 6)
    
def h2(key):
    return H(key) % 2

def H(key):
    return ((key + 13) * 7)
    

    
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
def DETERMINE(graph, numberInitialEdges, ey):
    # x ~ U(0, (k-1)*|E|-1)
    
    x = h1(6, 2)
    # direction ~ U(0,1)
    direction = h2(6)

    vsvt = []
    if x < numberInitialEdges:
        vsvt = graph['e' + x]
    else:
        vsvt = DETERMINE(graph, numberInitialEdges, graph['e'+x])
    
    
    
    refvsvt = []
    if direction == 0:
        refvsvt = [  ,  ]
        return 
    else:
        refvsvt = [  ,  ]

if __name__ == '__main__':
    evograph() 
    
    
    
    
    
    
    
    
    
    
    
    