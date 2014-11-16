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
        self.knapsack_size = knapsack_size
        self.items = items
        self.cache = dict()
        for size in range(knapsack_size + 1):
            self.cache[(0, size)] = 0
        for num in range(len(items) + 1):
            self.cache[(num, 0)] = 0
    
    def solve(self):
        queue = []
        initial_query = (len(self.items), self.knapsack_size)
        queue.append(initial_query)
        while len(queue) > 0:
            (num, size) = queue[-1]
            if self.items[num-1].weight > size:
                try:
                    self.cache[(num, size)] = self.cache[(num-1, size)]
                except KeyError:
                    queue.append((num-1, size))
                    continue
            else:
                sub1 = (num-1, size)
                sub2 = (num-1, size-self.items[num-1].weight)
                try:
                    val1 = self.cache[sub1]
                except KeyError:
                    queue.append(sub1)
                    continue
                try:
                    val2 = self.items[num-1].value + self.cache[sub2]
                except KeyError:
                    queue.append(sub2)
                    continue
                self.cache[(num, size)] = max(val1, val2)
            queue.pop()
        return self.cache[(initial_query)]


Solver = KnapsackSolverRecursiveWithCaching
