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


class DijkstraSsspTestCase(unittest.TestCase):
    """
    Test dijkstra_sssp against networkx's dijkstra implementation.
    
    Will test against networkx.single_source_dijkstra_path_length on graphs
    we create using a random graph generator (networkx.gnm_random_graph) but 
    with the same seed every time. The edge weights are drawn using 
    random.randint(0, 99), again with the same seed every time. This means
    each time test_A is run it will always get graph_A to work on.
    
    Different tests will have different graphs though.
    """
    
    def test_on_directed_strongly_connected_graph(self):
        """
        Test on a small directed strongly connected graph.
        """
        # make the strongly connected directed graph:
        params_dscg = {'num_nodes': 200, 'num_edges': 1800, 'seed': 0, 
                       'directed': True}
        graph = make_graph(**params_dscg)
        assert(nx.is_strongly_connected(graph))
        # first run dijkstra_sssp
        dist, _ = dijkstra_sssp.solve(graph, source=0, weight='weight')
        # then networkx's dijkstra
        nx_dist = nx.single_source_dijkstra_path_length(graph, source=0, 
                                                        weight='weight')
        # finally, compare results
        inf = float('inf')
        for node in graph.nodes_iter():
            if dist[node] != inf:
                # node was reachable
                self.assertEqual(dist[node], nx_dist[node])
            else:
                # node was unreachable
                self.assertTrue(node not in nx_dist)
                self.assertEqual(dist[node], inf)
    
    def test_on_undirected_not_connected_graph(self):
        """
        Test on an undirected and not connected graph. 
        
        Not all nodes will be reachable from the source.
        """
        # make the undirected not connected graph
        params_uncg = {'num_nodes': 200, 'num_edges': 400, 'seed': 0, 
                       'directed': False}
        graph = make_graph(**params_uncg)
        assert(not nx.is_connected(graph))
        # first run dijkstra_sssp 
        dist, _ = dijkstra_sssp.solve(graph, source=0, weight='weight')
        # then run networkx's dijkstra
        nx_dist = nx.single_source_dijkstra_path_length(graph, source=0, 
                                                        weight='weight')
        # finally, compare results
        inf = float('inf')
        for node in graph.nodes_iter():
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
