"""
Dijkstra's single source shortest paths algorithm.

Given a networkx graph and one of its nodes as a source node "s" 
compute and return shortest s-t paths for every node "t" in the graph.
We assume that the given graph has non-negative edge weights. If some 
edges have negative weights this algorithm's behavior is undefined.

Currently implemented using a pseudo-heap, which is essentially a python 
dictionary. insert and decrease_key are (amortized) constant time, while 
pop (i.e. pop_min) takes linear time.

Author:
  Christos Nitsas
  (nitsas)
  (chrisnitsas)

Language:
  Python 3(.4)

Date:
  August, 2014
"""


import collections
# Modules I've written:
from ..datastructs import binary_heap


__all__ = ['solve', 'dijkstra_shortest_paths']


DistAndPred = collections.namedtuple('DistAndPred', ['dist', 'pred'])


def _init(graph):
    """
    Initialize nodes' distances and predecessors and return two dicts.
    
    graph -- a networkx graph
    
    Create three dicts, called dist, pred and finalized, mapping nodes to 
    distances, predecessors, and whether or not their distances are final
    respectively, initialize all distances to infinity, all predecessors to 
    None, all nodes as not finalized, and return the tuple:
    (dist, pred, finalized)
    """
    dist, pred, finalized = dict(), dict(), dict()
    inf = float('inf')
    for node in graph.nodes_iter():
        dist[node] = inf
        pred[node] = None
        finalized[node] = False
    return dist, pred, finalized


def dijkstra_shortest_paths(graph, source, weight='weight', 
                            heap_type=binary_heap.BinaryHeap):
    """
    Compute shortest paths from the source using Dijkstra's algorithm.
    
    graph -- a networkx graph
    souce -- the source node
    weight -- the name of the edge attribute we'll use as a weight 
              (default: 'weight')
    heap_type -- the type we'll use as a heap 
                 (default: binary_heap.BinaryHeap, for now)
    
    Careful: 
    All edge weights must be non-negative, for Dijkstra's algorithm to work 
    correctly!
    
    Returns a tuple of dictionaries (dist, pred) each with one entry 
    for each node in the graph.
    - dist contains a shortest path distance from the source
    - pred contains the predecessor in a shortest path from the source 
    """
    # initialize distances and predecessors
    dist, pred, finalized = _init(graph)
    dist[source] = 0
    # initialize the heap
    heap = heap_type()
    heap.insert((dist[source], source))
    # main loop
    num_finalized = 0
    while num_finalized < graph.number_of_nodes() and len(heap) > 0:
        # pop the next candidate for finalization
        _, u = heap.pop()
        if finalized[u]:
            # u has already been finalized; this is an old entry with greater 
            # dist for u; ignore it
            continue
        # u's dist won't get any lower; finalize it
        finalized[u] = True
        num_finalized += 1
        # check if u's neighbors' dist is lower if we pass through u
        for _, v, edge_attrs in graph.edges(u, data=True):
            if dist[u] + edge_attrs[weight] < dist[v]:
                dist[v] = dist[u] + edge_attrs[weight]
                heap.insert((dist[v], v))
                pred[v] = u
    return DistAndPred(dist, pred)


solve = dijkstra_shortest_paths
