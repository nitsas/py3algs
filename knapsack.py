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


__all__ = ['Item', 'KnapsackSolverWithCachingAndStack', 'Solver']


Item = collections.namedtuple('Item', ('value', 'size'))


class KnapsackSolverWithCachingAndStack:
    """
    Solve the Knapsack problem, using memoization and a stack.
    
    Uses dynamic programming, memoization (aka caching) and a stack (instead 
    of recursion).
    """
    
    def __init__(self, knapsack_size, items):
        """
        Initialize the problem and the cache.
        
        knapsack_size -- an integer; the size of the knapsack
        items -- a list of Item namedtuples
        items[i].size -- an integer; the i'th item's size
        items[i].value -- a number; the i'th item's value
        """
        self.knapsack_size = knapsack_size
        self.items = items
        self._cache = dict()
        # fill-in the cache with base cases' (subproblems') solutions
        for size in range(knapsack_size + 1):
            # if there are no items, the max value is 0
            self._cache[(0, size)] = 0
        for end in range(len(items) + 1):
            # if the knapsack's size is 0 no items fit, the max value is 0
            self._cache[(end, 0)] = 0
    
    def solve(self):
        """
        Solve the problem.
        
        Uses a cache (i.e. memoization) to remember subproblem solutions. 
        Also uses a stack (of subproblems to be solved) instead of recursing 
        on the subproblems, so that we avoid running into the recursion depth 
        limit.
        """
        # a stack of queries (aka subproblems to be solved)
        stack = []
        initial_query = (len(self.items), self.knapsack_size)
        stack.append(initial_query)
        # Run as long as there are subproblems that need to be solved.
        # - this might not pass through all possible subproblems; in fact, 
        #   we're counting on it
        # - it will only pass through the subproblems that the initial 
        #   problem needs solved
        while len(stack) > 0:
            (end, ksize) = stack[-1]
            # this is the subproblem where we have only items self.items[:end]
            # and the knapsack size is ksize
            if self.items[end - 1].size > ksize:
                # item end-1 does not fit
                try:
                    # retrieve subproblem result from the cache
                    self._cache[(end, ksize)] = self._cache[(end - 1, ksize)]
                except KeyError:
                    # subproblem hasn't been solved yet, put it on the stack
                    stack.append((end - 1, ksize))
                    continue
            else:
                # item end-1 fits; we get two subproblems:
                # - one if we don't include item end-1 in the knapsack
                # - one if we do include it
                sub1 = (end - 1, ksize)
                sub2 = (end - 1, ksize - self.items[end - 1].size)
                try:
                    # retrieve 1st subproblem's result from the cache and 
                    # compute max value if we don't include item end-1
                    val1 = self._cache[sub1]
                except KeyError:
                    # subproblem hasn't been solved yet, put it on the stack
                    stack.append(sub1)
                    continue
                try:
                    # retrieve 2nd subproblem's result from the cache and
                    # compute max value if we do include item end-1
                    val2 = self.items[end - 1].value + self._cache[sub2]
                except KeyError:
                    # subproblem hasn't been solved yet, put it on the stack
                    stack.append(sub2)
                    continue
                # is it better to include item end-1 or not?
                self._cache[(end, ksize)] = max(val1, val2)
            # done with this subproblem
            stack.pop()
        return self._cache[(initial_query)]


Solver = KnapsackSolverWithCachingAndStack
