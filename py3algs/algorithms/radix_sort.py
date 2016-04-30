"""
A simple (and probably hugely inefficient) radix sort implementation

I couldn't think of a simple enough general interface that would allow to
ask to sort any kind of values, so I provide an implementation specifically
for integers up to a given max value.

Author:
  Christos Nitsas
  (nitsas)
  (nitsas.chris)

Language:
  Python 3(.4)

Date:
  May, 2016
"""


from math import log2
from collections import deque


__all__ = ['sort']


def sort_non_negative_integers(sequence, max_value):
    """
    A simple (and probably hugely inefficient) radix sort implementation
    
    sequence -- a sequence of non-negative integers to sort
    max_value -- an upper bound for the values in the sequence
    
    Returns a list with the elements of the sequence sorted in non-decreasing
    order.
    """
    
    zero_bit_queue = deque()
    one_bit_queue = deque()
    
    powers_of_two = (2 ** i for i in range(int(log2(max_value)) + 1))
    
    intermediate_list = list(sequence)
    for power_of_two in powers_of_two:
        for num in intermediate_list:
            if num & power_of_two > 0:
                one_bit_queue.append(num)
            else:
                zero_bit_queue.append(num)
        
        intermediate_list = list()
        for i in range(len(zero_bit_queue)):
            intermediate_list.append(zero_bit_queue.popleft())
        for i in range(len(one_bit_queue)):
            intermediate_list.append(one_bit_queue.popleft())
    
    return intermediate_list
