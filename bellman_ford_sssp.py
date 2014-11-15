"""
Compute single source shortest paths using the Bellman-Ford algorithm.

Given a networkx graph and one of its nodes as a source node "s" 
compute and return shortest s-t paths for every node "t" in the graph.

We don't have to assume anything about connectedness.

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
import random


__all__ = ['solve', 'bellman_ford_shortest_paths', 'NegativeCycleError', 
           'has_negative_cycle']


class NegativeCycleError(Exception):
    """
    Exception raised in bellman_ford_shortest_paths() if and only if 
    the given graph contains a negative cycle (that is reachable from 
    the source vertex).
    """
    def __init__(self, message=None):
        if message is None:
            message = 'The graph contains a negative cycle!'
        self.message = message


def _init(graph, source):
    """
    Initialize all distances (except the source's) to infinity and 
    all predecessors to None.
    """
    dist, pred = dict(), dict()
    inf = float('inf')
    for node in graph.nodes_iter():
        dist[node] = inf
        pred[node] = None
    dist[source] = 0
    return dist, pred


def bellman_ford_shortest_paths(graph, source, weight_attr_name=None):
    """
    Solves the single source shortest paths problem using the 
    Bellman-Ford algorithm.
    
    Returns a tuple of dictionaries (dist, pred) each with one entry 
    for each node in the graph.
    - dist contains a shortest path distance from the source
    - pred contains the predecessor in a shortest path from the source 
    
    If the graph contains a negative cycle that is reachable from the 
    source vertex, we'll get a NegativeCycleError exception.
    """
    # which of the edges' attributes is going to be the "weight"
    if weight_attr_name is None:
        weight = 'cost'
    else:
        weight = weight_attr_name
    # initialize distances and predecessors
    dist, pred = _init(graph, source)
    # main loop
    for i in range(graph.number_of_nodes()-1):
        for u, v, edge_attrs in graph.edges_iter(data=True):
            if dist[u] + edge_attrs[weight] < dist[v]:
                dist[v] = dist[u] + edge_attrs[weight]
                pred[v] = u
    # one more iteration to check for negative cycles 
    # (reachable from the source)
    for u, v, edge_attrs in graph.edges_iter(data=True):
        if dist[u] + edge_attrs[weight] < dist[v]:
            raise(NegativeCycleError)
    return dist, pred


def has_negative_cycle(graph_):
    """
    Returns True if the graph contains a negative cycle; 
    False otherwise.
    
    We don't have to assume the graph is connected. This will detect 
    a negative cycle (if one exists) even if the graph is disconnected.
    """
    graph = graph_.copy()
    # add a supersource
    assert(not 'supersource' in graph)
    ss = 'supersource'
    graph.add_node(ss)
    for node in graph.nodes_iter():
        graph.add_edge(ss, node, cost=0)
    graph.remove_edge(ss, ss)
    # run Bellman-Ford on the new graph starting at the supersource
    try:
        bellman_ford_shortest_paths(graph, ss)
    except NegativeCycleError:
        return True
    return False


solve = bellman_ford_shortest_paths
