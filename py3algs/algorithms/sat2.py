"""
Simple solvers and oracles for the 2-SAT problem.

Author:  
  Christos Nitsas  
  (nitsas)  
  (chrisnitsas)  

Language:  
  Python 3(.4)  

Date:  
  August, 2014
"""


import math
import networkx as nx


__all__ = ['isSatisfiable']


def isSatisfiable(num_vars, clauses):
    """
    isSatisfiable returns True if the 2-SAT problem defined by 
    num_vars and clauses is satisfiable; False otherwise.
    
    The algorithm:
    - transforms the problem to the corresponding implication 
      graph, 
    - computes the graph's strongly connected components and 
    - for each of the problem's variables checks if both the variable 
      and its negation belong to the same connected component. 
    
    The last step will be true for some variable if and only if the 
    problem is unsatisfiable.
    """
    # make the corresponding implication graph
    # the graph has:
    # - two nodes for each variable, one for the positive and 
    #   one for the negative version
    # - two edges/implications for each clause (x1, x2):
    #   * false x1 implies true x2 and 
    #   * false x2 implies true x1
    graph = nx.DiGraph()
    for x1, x2 in clauses:
        graph.add_edge(-x1, x2)
        graph.add_edge(-x2, x1)
    cur_id = 0
    component_id = dict()
    for component in nx.strongly_connected_components(graph):
        cur_id += 1
        for node in component:
            component_id[node] = cur_id
    for var in range(1, num_vars + 1):
        id_var = component_id.get(var)
        id_not_var = component_id.get(-var)
        if id_var is None or id_not_var is None:
            continue
        elif id_var == id_not_var:
            return False
    return True


def _random_assignment(num_variables):
    raise NotImplementedError()


class Sat2ProbabilisticSolver:
    """
    Sat2ProbabilisticSolver uses Papadimitriou's probabilistic 
    algorithm.
    i.e.
    - For an unsatisfiable instance this always returns None.
    - For a satisfiable instance this produces a satisfying assignment 
      with probability >= 1 - 1/n, where n is the number of variables, 
      in polynomial time.
    """
    def __init__(self, num_variables, clauses):
        self.num_variables = num_variables
        self.clauses = clauses
    
    def solve(self):
        for i in range(log(self.num_variables, 2)):
            assignment = _random_assignment(num_variables)
            raise NotImplementedError()
        # claim than the problem is unsatisfiable
        return None

