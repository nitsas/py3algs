#!/usr/bin/env python3


import sys
import random
import argparse
import cProfile
# third-party modules:
import networkx as nx
# modules I've written:
import dijkstra_sssp


class DijkstraSsspOnRandomUndirectedGraph:
    """
    Test dijkstra_sssp against networkx's dijkstra on a small graph.
    
    Will test against networkx.single_source_dijkstra_path_length on an
    undirected networkx graph created using networkx.gnm_random_graph with
    the same seed every time. The edge weights are drawn using 
    random.randint(0, 99), again with the same seed every time.
    """
    
    def __init__(self, num_nodes, num_edges, seed):
        """
        Create the graph.
        
        num_nodes -- number of nodes 
        num_edges -- number of edges 
        seed -- the random number generator seed 
        
        Edge weights will be random integers in the range [0, 99] inclusive.
        The first node (id: 0) will be set as the source (self.source).
        """
        # create the graph 
        # (if we use the same seed every time, we get the same graph)
        self.graph = nx.gnm_random_graph(num_nodes, num_edges, seed=seed,
                                         directed=False)
        # assign edge weights
        # (again we use a seed so we get the same weights every time)
        random.seed(seed)
        for _, _, edge_attrs in self.graph.edges_iter(data=True):
            edge_attrs['weight'] = random.randint(0, 99)
        # the source node
        self.source = 0
    
    def run_dijkstra(self):
        self.result = dijkstra_sssp.solve(self.graph, self.source, 
                                          weight='weight')
    
    run = run_dijkstra


Experiment = DijkstraSsspOnRandomUndirectedGraph


def parse_args():
    desc = 'Profile dijkstra_sssp on a random graph.'
    parser = argparse.ArgumentParser(description='Profile dijkstra_sssp.')
    parser.add_argument('-n', '--num-nodes', default=10000, type=int, 
                        help='number of nodes in the graph (default 10000)')
    parser.add_argument('-m', '--num-edges', default=100000, type=int, 
                        help='number of edges in the graph (default 100000)')
    parser.add_argument('-s', '--seed', default=0, type=int, 
                        help='the random number generator seed (default 0)')
    args = parser.parse_args()
    return args


def main(args):
    experiment = Experiment(args.num_nodes, args.num_edges, args.seed)
    locals_ = {'experiment': experiment}
    cProfile.runctx('experiment.run()', globals={}, locals=locals_,
                    sort='cumtime')
    return 0


if __name__ == "__main__":
    status = main(parse_args())
    sys.exit(status)
