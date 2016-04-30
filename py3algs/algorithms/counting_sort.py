"""
Counting sort algorithm.

Useful for sorting sequences of integers up to a relatively small number K.
To generalize, counting sort can be useful for sorting sequences of a relatively
small number of different values, when we have a sequence of all possible values
(in sorted order).

The complexity of counting sort for a sequence of N elements with K possible
different values for each element is O(N * K).

Example:
---

Sort the list ['c', 'd', 'd', 'a', 'c', 'c', 'b', 'a', 'c', ... ] knowing that
all elements have values in: ('a', 'b', 'c', 'd').

If the length N of the list is: `N > 2^4` (i.e. `log(N) > 4`), counting sort
will be faster than comparison-sorting algorithms (which have complexity of
O(N * log(N)).

Author:
  Christos Nitsas
  (nitsas)
  (nitsas.chris)

Language:
  Python 3(.4)

Date:
  April, 2016
"""


from collections import Counter


__all__ = ['sort']


def sort(sequence, values):
    """
    Sort using the counting sort algorithm.
    
    sequence -- the sequence to sort
    values -- all the possible values of elements in the sequence
              (values must be in sorted order)
    
    Returns a list with the given sequence's elements in non-decreasing order.
    """
    count_per_value = Counter(sequence)
    result = []
    for value in values:
        result.extend([value] * count_per_value[value])
    return result
