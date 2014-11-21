#!/usr/bin/env python3


import sys
import unittest
import random
# third-party modules:
import networkx as nx
# modules I've written:
import dijkstra_sssp


def make_graph(num_nodes, num_edges, seed=None, directed=True):
    # create the graph 
    # (if we use the same seed every time, we'll get the same graph)
    graph = nx.gnm_random_graph(num_nodes, num_edges, seed=seed,
                                directed=directed)
    # assign edge weights
    # (again we use a seed so we get the same weights every time)
    random.seed(seed)
    for _, _, edge_attrs in graph.edges_iter(data=True):
        edge_attrs['weight'] = random.randint(0, 99)
    return graph
    
class DijkstraSsspOnSmallDirectedStronglyConnectedGraph(unittest.TestCase):
    """
    Test dijkstra_sssp against networkx's dijkstra on a small directed
    strongly connectedgraph.
    
    Will test against networkx.single_source_dijkstra_path_length on a 
    directed and strongly connected networkx graph created using 
    networkx.gnm_random_graph with the same seed every time. The edge weights 
    are drawn using random.randint(0, 99), again with the same seed every time.
    """
    
    def setUp(self):
        num_nodes = 200
        num_edges = 1800
        seed = 0
        # make the graph
        self.graph = make_graph(num_nodes, num_edges, seed)
        assert(nx.is_strongly_connected(self.graph))
        # the source node
        self.source = 0
    
    def test_vs_networkx_single_source_dijkstra(self):
        dist, _ = dijkstra_sssp.solve(self.graph, self.source, weight='weight')
        nx_dist = nx.single_source_dijkstra_path_length(self.graph,
                                            self.source, weight='weight')
        for node in self.graph.nodes_iter():
            self.assertEqual(dist[node], nx_dist[node])


class DijkstraSsspOnUndirectedNotConnectedGraph(unittest.TestCase):
    """
    Test dijkstra_sssp against networkx's dijkstra on an undirected and not
    connected graph. 
    
    Will test against networkx.single_source_dijkstra_path_length on an 
    undirected and not connected networkx graph created using 
    networkx.gnm_random_graph. The edge weights are drawn using 
    random.randint(0, 99). We use a constant seed for both random generators,
    the same seed every time this is run, so we'll always get the same graph.
    
    Not all nodes will be reachable from the source.
    """
    
    def setUp(self):
        num_nodes = 200
        num_edges = 400
        seed = 0
        # make the graph
        self.graph = make_graph(num_nodes, num_edges, seed, directed=False)
        assert(not nx.is_connected(self.graph))
        # the source node
        self.source = 0
    
    def test_vs_networkx_single_source_dijkstra(self):
        dist, _ = dijkstra_sssp.solve(self.graph, self.source, weight='weight')
        nx_dist = nx.single_source_dijkstra_path_length(self.graph,
                                            self.source, weight='weight')
        inf = float('inf')
        for node in self.graph.nodes_iter():
            if dist[node] != inf:
                # node was reachable
                self.assertEqual(dist[node], nx_dist[node])
            else:
                # node was unreachable
                self.assertTrue(node not in nx_dist)
                self.assertEqual(dist[node], inf)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
