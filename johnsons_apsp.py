"""
Compute all pairs shortest paths using Johnson's algorithm.

Given a networkx graph compute and return shortest s-t paths for every 
pair s, t of nodes in the graph.

If the graph contains a negative cycle we'll get a NegativeCycleError 
exception.

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
import bellman_ford_sssp
import dijkstra_sssp


__all__ = ['solve', 'johnsons_all_pairs_shortest_paths', 'NegativeCycleError']


DistAndPred = collections.namedtuple('DistAndPred', ['dist', 'pred'])


NegativeCycleError = bellman_ford_sssp.NegativeCycleError


def _add_supersource(graph):
    """
    This will add a new "supersource" node to the graph as well 
    as zero cost edges from the supersource to every other node.
    
    graph -- a networkx graph
    """
    ss = '_temp_supersource'
    if ss in graph:
        import time
        ss = '_temp_supersource_' + time.asctime()
        if ss in graph:
            raise Exception('Failed to add temporary supersource.')
    graph.add_node(ss)
    for node in graph.nodes_iter():
        graph.add_edge(ss, node, cost=0)
    graph.remove_edge(ss, ss)
    return ss


def _compute_node_weights(graph):
    """
    Compute a weight for each node, such that reweighting each edge (u, v) 
    using the formula: 
    cost'(u, v) = cost(u, v) + weight(u) - weight(v)
    will result in non-negative edge costs.
    
    graph -- a networkx graph
    """
    # add a supersource
    ss = _add_supersource(graph)
    # compute distances from the supersource; 
    # those will become node weights
    node_weight, node_pred = bellman_ford_sssp.solve(graph, ss)
    # remove the supersource
    graph.remove_node(ss)
    del(node_weight[ss])
    return node_weight


def _reweight_edges_using_node_weights(graph, node_weight, 
                                     weight_attr_name=None):
    """
    Reweight each edge (u, v) using the formula:
    cost'[(u, v)] = cost[(u, v)] + node_weight[u] - node_weight[v]
    This will preserve shortest paths.
    
    graph -- a networkx graph
    node_weight -- a dictionary mapping nodes to weights
    weight_attr_name -- the name of the edge attribute we want to 
                        use as weights/costs (default: 'cost')
    
    For suitable node weights, this will get us non-negative edge 
    weights.
    """
    # set name of edge weight attribute
    if weight_attr_name is None:
        weight = 'cost'
    else:
        weight = weight_attr_name
    # use the node weights to assign a new (non-negative) cost 
    # to each edge which preserves shortest paths 
    for u, v, attrs in graph.edges_iter(data=True):
        attrs[weight] = attrs[weight] + node_weight[u] - node_weight[v]


def johnsons_all_pairs_shortest_paths(graph_):
    """
    Compute a shortest path for every pair of nodes in the graph.
    
    graph_ -- a networkx graph
    
    Return a namedtuple of two dictionaries (dist, pred). Both dist and pred
    map each node (source) in the graph to another dict, which in turn maps
    nodes (targets) to distances and predecessors respectively.
    - dist[u][v] contains a shortest path distance from u to v
    - pred[u][v] contains the predecessor of v in a shortest path from u
    
    This will not mutate the graph; we work on a temporary copy.
    Will throw a NegativeCycleError exception if the graph contains a 
    negative cycle.
    """
    # we work on a copy of the graph
    graph = graph_.copy()
    # compute node weights, for the edge reweighting step
    # (this will throw a NegativeCycleError exception if the graph 
    # contains a negative cycle)
    node_weight = _compute_node_weights(graph)
    # reweigh all the graph's edges so that there are no negative edges
    # this operarion preserves shortest paths
    _reweight_edges_using_node_weights(graph, node_weight)
    # call dijkstra's single source shortest paths algorithm once 
    # for each node in the graph, to compute all pairs shortest paths
    dist, pred = dict(), dict()
    for node in graph.nodes_iter():
        # compute shortest paths using the current node as a source
        dist[node], pred[node] = dijkstra_sssp.solve(graph, node)
    # remember that we have reweighted the edges; the actual shortest 
    # paths didn't change but their lengths did, so we now have to 
    # undo the effects of reweighting in the shortest path lengths 
    for u in graph.nodes_iter():
        for v in graph.nodes_iter():
            dist[u][v] = dist[u][v] - node_weight[u] + node_weight[v]
    # return all pairs shortest paths distances and predecessors
    return DistAndPred(dist, pred)


solve = johnsons_all_pairs_shortest_paths
