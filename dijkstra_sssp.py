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
import dict_heap


__all__ = ['solve', 'dijkstra_shortest_paths']


def _init(graph, source):
    """
    Initialize nodes' distances and predecessors and return two dicts.
    
    graph -- a networkx graph
    source -- the source node
    
    Create two dicts, called dist and pred, mapping nodes to distances and
    predecessors respectively, initialize all distances (except the source's) 
    to infinity and all predecessors to None, and return the tuple 
    (dist, pred).
    """
    dist, pred = dict(), dict()
    inf = float('inf')
    for node in graph.nodes_iter():
        dist[node] = inf
        pred[node] = None
    dist[source] = 0
    return dist, pred


def dijkstra_shortest_paths(graph, source, weight_attr_name=None, 
                            heap_type=None):
    """
    Compute shortest paths from the source using Dijkstra's algorithm.
    
    graph -- a networkx graph
    souce -- the source node
    weight_attr_name -- the name of the edge attribute we'll use as a weight
    heap_type -- the type we'll use as a heap, default dict_heap (for now)
    
    Careful: 
    All edge weights must be non-negative, for Dijkstra's algorithm to work 
    correctly!
    
    Returns a tuple of dictionaries (dist, pred) each with one entry 
    for each node in the graph.
    - dist contains a shortest path distance from the source
    - pred contains the predecessor in a shortest path from the source 
    """
    # which of the edges' attributes is going to be the "weight"?
    if weight_attr_name is None:
        weight = 'cost'
    else:
        weight = weight_attr_name
    # what type of heap will we use?
    if heap_type is None:
        heap_type = dict_heap.DictHeap
    # initialize distances and predecessors
    dist, pred = _init(graph, source)
    # insert all nodes into the heap
    heap = heap_type()
    for node in graph.nodes_iter():
        heap.insert(node, dist[node])
    # main loop
    while len(heap) > 0:
        u = heap.pop()
        for _, v, edge_attrs in graph.edges(u, data=True):
            if dist[u] + edge_attrs[weight] < dist[v]:
                dist[v] = dist[u] + edge_attrs[weight]
                heap.decrease_key(v, dist[v])
                pred[v] = u
    return dist, pred


solve = dijkstra_shortest_paths
