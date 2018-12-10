# EvoGraph: An Effective and Efficient Graph Upscaling Method for Preserving Graph Properties.

## Background
Implementation of KDD '18 accepted paper, EvoGraph. This graph upscaling method paper can be found in the `Citations` section at the bottom.

Implementations of both [normal](/evograph/src/evograph.py) and [parallel computing](/evograph/src/evographParallel.py) are present.



## Algorithm
![algorithm](/evograph/images/code-images/xevograph.png)

Basic Edge Attachment: non-recursive edge attachment

![BEA](/evograph/images/code-images/BEA.png)

Memory-efficient Edge Attachment: recursive edge attachment

![MEA](/evograph/images/code-images/MEA.png)



## Parallel Computation 
It is possible to multi-process the main for-loop of the algorithm. 
Why is parallel computing allowed?
* EvoGraph does not store the currently-upscaling graph in main memory
* The graph is both read and written from the same file, on disk
* Each newly added edge is read by a different thread, and placed back into the file when the parent edge calculation is finished
* Experimental results led to conclusion that ~100-110 threads is optimal

Why are the writes out of order? 
* Some of the parent-edge calculations require recursion
* Earlier reads might be written back into the file later
* Out of order does not matter, as all threads read/write their own unique thread

Normal for-loop
```
for EdgeInstance.currentNumEdges in range(EdgeInstance.initialNumEdges, maxNumEdges):
    vsvt = DETERMINE(EdgeInstance.currentNumEdges)
    WRITE(vsvt, EdgeInstance.currentNumEdges, fileToUpscale)
```

Parallelized for-loop
```
def parallel(fileToUpscale, kValToUpscaleTo, processes):
    p = Pool(processes=processes)
    iterRange = list(range(EdgeInstance.initialNumEdges, maxNumEdges))
    p.map(EvoGraph, iterRange)
    p.close()

def EvoGraph(currentNumEdges):
    vsvt = DETERMINE(currentNumEdges)
    WRITE(vsvt, currentNumEdges, fileToUpscale)
```
## Experiments

Initial graph: 

![initial graph](/evograph/images/code-images/1graph.png)

Initial graph representation: 

![initial graph](/evograph/images/code-images/1actual.png)



## Citation

Himchan Park and Min-Soo Kim. 2018. EvoGraph: An Effective and Efficient Graph Upscaling Method for Preserving Graph Properties. In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (KDD '18). ACM, New York, NY, USA, 2051-2059. DOI: https://doi.org/10.1145/3219819.3220123

Original Implementation GitHub: https://github.com/chan150/EvoGraph
