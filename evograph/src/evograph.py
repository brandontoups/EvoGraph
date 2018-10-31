'''
Created on Oct 30, 2018

@authors: Brandon Toups
'''

def evograph():

# Following two hash functions where H(key) = ((key + 13) x 7)
# h1(y) determines the ID x of a parent edge ex of the edge ey
# Hash Function for U(0, (k−1)·|E|−1)
# h1 :key→[0,...,(k−1)·|E|−1] 
#
# h2(y) determines a direction of the edge ey (direction 0 means towards 
# the inside of the graph, while direction 1 means towards the outside of graph.
# Hash Function for U(0,1)
# h2 : key → [0,1]
# 
# ex: attaching e6 to GSF=2
#     H(6) = ((6+13) x 7) = 133
#     h1(6) = 133mod(2-1) * 6 = 1
#     h2(6) = 133mod2 = 1
# thus e1 = (v0,v2) is picked as a parent edge and e6 is determined as (v0,REFSF=2(v2)) = (v0,v7)
# 
# MEA - Memory-efficient edge attachment
# DETERMINE(ey) :
#     x ∼ U(0, (k−1)·|E|−1) 
#     direction ∼ U(0,1)
# if x < |E|:
#     (vs,vt) = ex
# else:
#     DETERMINE(ex)
# 
# if direction = 0
#     (REFSF=k(vs),vt)
# else:
#     (vs,REFSF=k(vt))

if __name__ == '__main__':
    evograph() 
    
    
    
    
    
    
    
    
    
    
    
    
#===============================================================================
# # BEA - Basic Edge Attachment -- not actually used in this algorithm. This could work
# but this holds new graph in memory rather than using hash map recursive. 
# # DETERMINE(ey ) :
# #     x ∼ U(0, (k−1)·|E|−1) 
# #     direction ∼ U(0,1)
# #     (vs , vt ) ← ex
# #     
# #     if 􏰀direction = 0: 
# #         return (REFSF=k(vs), vt)  
# #     else: 
# #         return (vs, REFSF=k(vt))
#===============================================================================