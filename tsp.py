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
Query = collections.namedtuple('Query', ('to_visit', 'target', 'num_edges'))


def _subqueries(query):
    """Yield all subqueries (subproblems) one by one."""
    for i, u in enumerate(query.to_visit):
        yield Query(query.to_visit[:i] + query.to_visit[i+1:], 
                    u, query.num_edges - 1)


class TspSolverDynamicProgrammingWithMemoization:
    """
    Solves the Travelling Salesman Problem a given graph.
    
    We use a dynamic programming approach with memoization.
    
    We expect a networkx.Graph type graph.
    """
    def __init__(self, graph):
        """Initialize the problem with the given underlying graph."""
        self.graph = graph
        self.cache = dict()
        
    def _solve_subproblem(self, query, weight):
        """
        Solves the given subproblem.
        
        Remember:
        query.to_visit contains the vertices we have to visit
        query.target contains the target vertex (after to_visit)
        query.num_edges is the number of edges we must use
        """
        assert(query.num_edges == len(query.to_visit) + 1)
        assert(query.num_edges >= 1)
        try:
            return self.cache[query]
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
            assert(best_subtour is not None)
            stops = best_subtour.stops + (query.target,)
            tour = Tour(min_cost, stops)
            self.cache[query] = tour
            return tour
    
    def solve(self, weight_attr_name=None):
        """
        Solves the problem - returns a cheapest tour through all 
        the graph's vertices.
        """
        # which edge attribute will we use as the edge weight?
        if weight_attr_name is None:
            weight = 'cost'
        else:
            weight = weight_attr_name
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
            self.cache[query] = Tour(cost_su, (s, u))
        # make the initial query and insert it in the query queue
        initial_query = Query(rest, s, self.graph.number_of_nodes())
        tour = self._solve_subproblem(initial_query, weight)
        return tour


Solver = TspSolverDynamicProgrammingWithMemoization
