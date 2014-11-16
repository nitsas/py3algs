"""
Solve the Knapsack problem using dynamic programming.

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


__all__ = ['Item', 'KnapsackSolverWithCachingAndQueue', 'Solver']


Item = collections.namedtuple('Item', ('value', 'weight'))


class KnapsackSolverWithCachingAndQueue:
    """
    Solve the Knapsack problem, using memoization and a queue.
    
    Uses dynamic programming, memoization (aka caching) and a queue (instead 
    of recursion).
    """
    
    def __init__(self, knapsack_size, items):
        """
        Initialize the problem and the cache.
        
        knapsack_size -- an integer; the size of the knapsack
        items -- a list of Item namedtuples
        items[i].weight -- an integer; the i'th item's weight
        items[i].value -- a number; the i'th item's value
        """
        self.knapsack_size = knapsack_size
        self.items = items
        self.cache = dict()
        # fill-in the cache with base cases' (subproblems') solutions
        for size in range(knapsack_size + 1):
            # if there are no items, the max value is 0
            self.cache[(0, size)] = 0
        for num in range(len(items) + 1):
            # if the knapsack's size is 0 no items fit, the max value is 0
            self.cache[(num, 0)] = 0
    
    def solve(self):
        """
        Solve the problem.
        
        Uses a cache (i.e. memoization) to remember subproblem solutions. 
        Also uses a queue (of subproblems to be solved) instead of recursing 
        on the subproblems, so that we avoid running into the recursion depth 
        limit.
        """
        # a queue of queries (aka subproblems to be solved)
        queue = []
        initial_query = (len(self.items), self.knapsack_size)
        queue.append(initial_query)
        # Run as long as there are subproblems that need to be solved.
        # - this might not pass through all possible subproblems; in fact, 
        #   we're counting on it
        # - it will only pass through the subproblems that the initial 
        #   problem needs solved
        while len(queue) > 0:
            (num, ksize) = queue[-1]
            if self.items[num - 1].weight > ksize:
                # item num-1 does not fit
                try:
                    # retrieve subproblem result from the cache
                    self.cache[(num, ksize)] = self.cache[(num - 1, ksize)]
                except KeyError:
                    # subproblem hasn't been solved yet, queue it
                    queue.append((num - 1, ksize))
                    continue
            else:
                # item num-1 fits; we get two subproblems:
                # - one if we don't include item num-1 in the knapsack
                # - one if we do include it
                sub1 = (num - 1, ksize)
                sub2 = (num - 1, ksize - self.items[num - 1].weight)
                try:
                    # retrieve 1st subproblem's result from the cache and 
                    # compute max value if we don't include item num-1
                    val1 = self.cache[sub1]
                except KeyError:
                    # subproblem hasn't been solved yet, queue it
                    queue.append(sub1)
                    continue
                try:
                    # retrieve 2nd subproblem's result from the cache and
                    # compute max value if we do include item num-1
                    val2 = self.items[num - 1].value + self.cache[sub2]
                except KeyError:
                    # subproblem hasn't been solved yet, queue it
                    queue.append(sub2)
                    continue
                # is it better to include item num-1 or not?
                self.cache[(num, ksize)] = max(val1, val2)
            # done with this subproblem
            queue.pop()
        return self.cache[(initial_query)]


Solver = KnapsackSolverRecursiveWithCaching
