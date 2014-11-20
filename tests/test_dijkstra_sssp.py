#!/usr/bin/env python3


import sys
import unittest
import random
# third-party modules:
import networkx as nx
# modules I've written:
import dijkstra_sssp


class DijkstraSsspOnSmallRandomUndirectedGraph(unittest.TestCase):
    """
    Test dijkstra_sssp against networkx's dijkstra on a small graph.
    
    Will test against networkx.single_source_dijkstra_path_length on an 
    undirected networkx graph created using networkx.gnm_random_graph with
    the same seed every time. The edge weights are drawn using 
    random.randint(0, 99), again with the same seed every time.
    """
    
    def setUp(self):
        num_nodes = 200
        num_edges = 1800
        seed = 0
        # create the graph 
        # (we use the same seed every time so we get the same graph)
        # the graph will be connected, we checked
        self.graph = nx.gnm_random_graph(num_nodes, num_edges, seed=seed)
        # assign edge weights
        # (again we use a seed so we get the same weights every time)
        random.seed(seed)
        for _, _, edge_attrs in self.graph.edges_iter(data=True):
            edge_attrs['weight'] = random.randint(0, 99)
        # the source node
        self.source = 0
    
    def test_vs_networkx_single_source_dijkstra(self):
        dist, _ = dijkstra_sssp.solve(self.graph, self.source, 
                                      weight_attr_name='weight')
        nx_dist = nx.single_source_dijkstra_path_length(self.graph,
                                            self.source, weight='weight')
        for node in self.graph.nodes_iter():
            self.assertEqual(dist[node], nx_dist[node])


def main():
    unittest.main()


if __name__ == "__main__":
    main()
