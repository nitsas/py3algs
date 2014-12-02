"""
Compute the strongly connected components (SCCs) of a directed graph using
Kosaraju's two pass algorithm.

This assumes the given graph is a networkx.DiGraph.

Author:
  Christos Nitsas
  (nitsas)
  (chrisnitsas)

Language:
  Python 3(.4)

Date:
  November, 2014
"""


import collections


__all__ = ['SccFinder']


class SccFinder:
    
    """
    Computes the strongly connected components (SCCs) of a directed graph.
    """
    
    def __init__(self, graph):
        """
        Initialize.
        
        graph -- a networkx.DiGraph
        """
        self.graph = graph
    
    def get_sccs(self):
        """
        Compute the strongly connected components (SCCs) of the graph, and
        return a list of lists of nodes, each inner list being an SCC.
        """
        # first loop of dfs's:
        # - on the reverse graph
        # - remember the order you finished exploring the nodes (use a queue)
        self._unmark_nodes()
        self.finish_queue = []
        for node in self.graph.nodes_iter():
            if not self.marked[node]:
                self._reverse_dfs_compute_finish_order(node)
        # second loop of dfs's:
        # - normal direction
        # - dfs from nodes in the reverse order you finished 
        #   exploring them before
        self._unmark_nodes()
        sccs = []
        for node in reversed(self.finish_queue):
            if not self.marked[node]:
                scc = self._dfs_carve_out_scc(node)
                sccs.append(scc)
        return sccs
    
    def _unmark_nodes(self):
        """Unmark all nodes."""
        self.marked = collections.defaultdict(lambda: False)
    
    def _reverse_dfs_compute_finish_order(self, source):
        """
        An iterative implementation of the depth first search algorithm,
        traversing reverse edges and remembering the nodes' finish order.
        """
        # define a helper class
        class StackCommandAppendNodeToFinishQueue:
            """
            A simple class representing a command (reminder if you will) to
            add the included node to the finish_queue.
            
            We had to use this because our implementation is iterative and not
            recursive. How else can we remember when exactly a node should be
            added to the finish_queue? (there are other alternatives but they
            didn't seem much more elegant than this)
            """
            def __init__(self, node):
                self.node = node
        # start
        stack = [source]
        while len(stack) > 0:
            v = stack.pop()
            # if the top item a command or a node?
            if isinstance(v, StackCommandAppendNodeToFinishQueue):
                # top item is a command
                self.finish_queue.append(v.node)
            else:
                # top item is a node
                if not self.marked[v]:
                    self.marked[v] = True
                    # leave a command on top of the stack to add node v to the 
                    # finish queue after all its "children" are examined
                    stack.append(StackCommandAppendNodeToFinishQueue(v))
                    # add "children" on top of the stack, to be examined
                    for w in self.graph.predecessors_iter(v):
                        if not self.marked[w]:
                            stack.append(w)
    
    def _dfs_carve_out_scc(self, source):
        """
        An iterative implementation of the depth first search algorithm,
        finding one SCC at a time, if run from a suitable source node.
        """
        stack = [source]
        scc = []
        while len(stack) > 0:
            v = stack.pop()
            if not self.marked[v]:
                self.marked[v] = True
                scc.append(v)
                for w in self.graph.successors_iter(v):
                    stack.append(w)
        return scc
