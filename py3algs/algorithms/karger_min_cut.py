"""
Compute a min cut of an undirected graph using Karger's randomized contraction 
algorithm.

Assume an undirected graph with n vertices and m edges.

The single-run version of the algorithm returns a correct min cut of the graph 
with probability at least ``1 / (n choose 2)``, with a running time of
RUNNING_TIME.

By repeating the contraction algorithm ``T = (n choose 2) * ln(n)`` times with
independent random choices and returning the smallest cut, the probability of
not finding a minimum cut is at most ``1 / n``, with a total running time of
TOTAL_RUNNING_TIME.

TODO:
Calculate the running times.

Author:  
  Christos Nitsas  
  (nitsas)  
  (chrisnitsas)

Language:  
  Python 3(.4)

Date:  
  November, 2014
"""


import random
import math
import collections
# modules I've written:
from ..datastructs import union_find


__all__ = ['CutStruct', 'karger_min_cut_single_run', 'single_run', 
           'karger_min_cut_multi_run', 'multi_run']


CutStruct = collections.namedtuple('CutStruct', ['clusters',
                                                 'crossing_edges'])


def karger_min_cut_single_run(graph):
    """
    Attempt to compute a min cut of the graph by running Karger's randomized
    contraction algorithm a single time.
    
    Parameters:
    graph -- a networkx.Graph type undirected graph (can have self-loops)
    
    Assume a graph with n vertices and m edges. 
    
    This usually has a low success probability. Specifically, it will
    correctly return a min cut with probability at least ``1 / (n choose 2)``.
    
    The running time is RUNNING_TIME.
    """
    # no need for a special case for graphs with less than 3 nodes; the
    # following code works
    #
    # initialize a union-find structure with the graph's nodes
    ufs = union_find.UnionFindStructure(graph.nodes_iter())
    # Make a shuffled list of all the edges. Instead of picking a random edge 
    # at each iteration, we will be (reverse) iterating through the list of
    # shuffled edges.
    edges_list = graph.edges()
    random.shuffle(edges_list)
    # contract edges (i.e. merge nodes) until there's only 2 node clusters
    # left; they will be the two parts of the cut
    while ufs.num_clusters() > 2:
        # pop an edge and contract it; if both of the edge's endpoints belong 
        # to the same cluster, the edge will be ignored
        edge = edges_list.pop()
        ufs.union(edge[0], edge[1])
    # we will filter through the remaining edges, deleting edges whose two 
    # endpoints belong to the same cluster; what remains is the crossing edges
    # - first define the filter function
    def endpoints_in_different_clusters(edge):
        """
        Return True if the edge's endpoints lie in different clusters;
        False otherwise.
        
        This is a closure, it includes the variable ufs from its scope.
        """
        if not ufs.joined(edge[0], edge[1]):
            return True
        else:
            return False
    # - now filter the remaining edges
    crossing_edges = list(filter(endpoints_in_different_clusters, edges_list))
    return CutStruct(ufs.clusters(), crossing_edges)


single_run = karger_min_cut_single_run


def karger_min_cut_multi_run(graph, times=None):
    """
    Attempt to compute a min cut of the graph by running Karger's randomized
    contraction algorithm a single time.
    
    Assume a graph with n vertices and m edges. 
    
    Parameters:
    graph -- a networkx.Graph type undirected graph (can have self-loops)
    times -- integer; the number of times to run karger's randomized min cut 
             algorithm; default is ``(n choose 2) * ceil(ln(n))``
    
    Each run has a low success probability. Specifically, each run will 
    correctly return a min cut with probability at least ``1 / (n choose 2)``.
    Runs are independent so the overall success probability of the multiple 
    runs is at least ``times / (n choose 2)``.
    
    The running time is ``times * RUNNING_TIME``.
    """
    if times is None:
        n = graph.number_of_nodes()
        times = math.ceil(n * (n - 1) * math.ceil(math.log(n)) / 2)
    min_cut_size = float('inf')
    min_cut = None
    for i in range(times):
        cut = karger_min_cut_single_run(graph)
        # cut is the namedtuple:
        # (clusters, crossing_edges)
        cut_size = len(cut.crossing_edges)
        if cut_size < min_cut_size:
            min_cut = cut
            min_cut_size = cut_size
    return min_cut


multi_run = karger_min_cut_multi_run

