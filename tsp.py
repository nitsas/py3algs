"""
A simple dynamic programming algorithm for the Travelling Salesman Problem. 

This needs exponential time of course.

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


__all__ = ['Tour', 'TspSolverDynamicProgrammingWithMemoization', 'Solver']


# a TSP tour
Tour = collections.namedtuple('Tour', ('cost', 'stops'))


# a TSP subproblem
# to_visit -- a list containing the vertices we have to visit
# target -- the target vertex (after to_visit)
# num_edges -- the number of edges we must use
Query = collections.namedtuple('Query', ('to_visit', 'target', 'num_edges'))


def _subqueries(query):
    """Yield all subqueries (subproblems) one by one."""
    for i, u in enumerate(query.to_visit):
        yield Query(query.to_visit[:i] + query.to_visit[i+1:], 
                    u, query.num_edges - 1)


class TspSolverDynamicProgrammingWithMemoization:
    """
    Solve the Travelling Salesman Problem, given a graph.
    
    We use a dynamic programming approach with memoization.
    
    We expect a networkx.Graph type graph.
    """
    def __init__(self, graph):
        """
        Initialize the problem with the given underlying graph.
        
        graph -- a networkx graph
        """
        self.graph = graph
        self._cache = dict()
        
    def _solve_subproblem(self, query, weight):
        """
        Solve the given subproblem.
        
        query.to_visit -- list containing the vertices we have to visit
        query.target -- the target vertex (after to_visit)
        query.num_edges -- the number of edges we must use
        weight -- name of the edge attribute we'll use as edge weights; 
                  (default: 'weight')
        """
        #assert(query.num_edges == len(query.to_visit) + 1)
        #assert(query.num_edges >= 1)
        try:
            return self._cache[query]
        except KeyError:
            min_cost = float('inf')
            best_subtour = None
            # Remember, each tour (Tour type) has the following members:
            # tour.cost
            # tour.stops
            for subquery in _subqueries(query):
                subtour = self._solve_subproblem(subquery, weight)
                last_hop_cost = \
                        self.graph[subtour.stops[-1]][query.target][weight]
                if subtour.cost + last_hop_cost < min_cost:
                    min_cost = subtour.cost + last_hop_cost
                    best_subtour = subtour
            #assert(best_subtour is not None)
            stops = best_subtour.stops + (query.target,)
            tour = Tour(min_cost, stops)
            self._cache[query] = tour
            return tour
    
    def solve(self, weight='weight'):
        """
        Solve the problem, and return a cheapest tour. 
        
        weight -- name of edge attribute we'll use as edge weights;
                  (default: 'weight')
        """
        # take care of the empty graph plus single node graphs:
        if self.graph.number_of_nodes() <= 1:
            # return the empty tour
            return Tour(0, tuple())
        # --- initialization ---
        # arbitrarily select the first vertex as the starting vertex
        # (this won't affect the cost of the cheapest tour)
        s = self.graph.nodes()[0]
        rest = tuple(self.graph.nodes()[1:])
        # initialize the smallest subproblems
        for u in rest:
            cost_su = self.graph[s][u][weight]
            query = Query(tuple(), u, 1)
            self._cache[query] = Tour(cost_su, (s, u))
        # make the initial query and insert it in the query queue
        initial_query = Query(rest, s, self.graph.number_of_nodes())
        tour = self._solve_subproblem(initial_query, weight)
        return tour


Solver = TspSolverDynamicProgrammingWithMemoization
