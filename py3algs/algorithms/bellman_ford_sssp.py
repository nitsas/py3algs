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


__all__ = ['NegativeCycleError', 'DistAndPred', 'solve', 
           'bellman_ford_shortest_paths', 'has_negative_cycle']


class NegativeCycleError(Exception):
    """
    Exception raised if and only if the given graph contains a negative 
    cycle that is reachable from the source vertex.
    """
    def __init__(self, message=None):
        if message is None:
            message = 'The graph contains a negative cycle!'
        self.message = message


DistAndPred = collections.namedtuple('DistAndPred', ['dist', 'pred'])


def _init(graph, source):
    """
    Initialize node distances and predecessors and return two dicts.
    
    Makes two dicts, one for node distances, and one for node predecessors,
    and initializes all distances (except the source's) to infinity and all 
    predecessors to None.
    
    graph -- a networkx graph
    source -- the source node
    """
    dist, pred = dict(), dict()
    inf = float('inf')
    for node in graph.nodes_iter():
        dist[node] = inf
        pred[node] = None
    dist[source] = 0
    return dist, pred


def bellman_ford_shortest_paths(graph, source, weight='weight'):
    """
    Compute shortest paths from the source using the Bellman-Ford algorithm.
    
    graph -- a networkx graph
    source -- the source node
    weight -- the name of the edge attribute we'll use as a weight 
              (default: 'weight')
    
    Return a namedtuple of two dictionaries (dist, pred), each with one entry 
    for each node in the graph.
    - dist contains a shortest path distance from the source
    - pred contains the predecessor in a shortest path from the source 
    
    If the graph contains a negative cycle that is reachable from the 
    source vertex, we'll get a NegativeCycleError exception.
    """
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
    return DistAndPred(dist, pred)


def has_negative_cycle(graph_, weight='weight'):
    """
    Returns True if the graph contains a negative cycle; False otherwise.
    
    graph_ -- a networkx graph
    weight -- the name of the edge attribute we'll use as edge weights
              (default: 'weight')
    
    We don't have to assume the graph is connected. This will detect 
    a negative cycle (if one exists) even if the graph is disconnected.
    
    Won't mutate the graph, operates on a copy.
    
    TODO:
    Make this not copy the graph; but don't mutate the graph either.
    """
    graph = graph_.copy()
    # add a supersource
    ss = '_supersource'
    if ss in graph:
        # there's already a node called '_supersource', try appending the
        # current date to the name
        import time
        ss = '_supersource_' + time.asctime()
        if ss in graph:
            raise Exception('Failed to add supersource.')
    graph.add_node(ss)
    # add edges from the supersource to every other node
    for node in graph.nodes_iter():
        graph.add_edge(ss, node, {weight: 0})
    graph.remove_edge(ss, ss)
    # run Bellman-Ford on the new graph starting at the supersource
    try:
        bellman_ford_shortest_paths(graph, ss, weight=weight)
    except NegativeCycleError:
        return True
    return False


solve = bellman_ford_shortest_paths
