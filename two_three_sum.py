"""
Simple algorithms for the 2-SUM and 3-SUM problems.

R-SUM problem:
Check if a given list of numbers contains R elements that some to a target
value.

These algorithms can actually be used with any kind of items that support
summation, subtraction and equality tests.

Author:
  Christos Nitsas
  (nitsas)
  (chrisnitsas)

Language:
  Python 3(.4)

Date:
  November, 2014
"""


import itertools


__all__ = ['two_sum', 'three_sum']


def two_sum(nums, target=0, distinct=True):
    """
    Return the indices of two numbers in `nums` that sum to `target` if such
    numbers exist; None otherwise.
    
    nums -- a list of numbers
    target -- a number (default 0)
    distinct -- if True only return distinct indices, i.e. there must be two
                entries (not necessarily with distinct values) that sum to 
                target - we don't accept a single entry being repeated; 
                allow repeats otherwise
    
    Time complexity: O(n)
    Space complexity: O(n)
    """
    # insert all nj's in a dict, which will remember their index in `nums`
    num_to_index = dict()
    for j, nj in enumerate(nums):
        num_to_index[nj] = j
    # iterate through nums
    for i, ni in enumerate(nums):
        # if ni's complement (w.r.t. target) exists
        if (target - ni) in num_to_index:
            # do we want distinct entries? or do we allow repeats?
            if distinct and i == num_to_index[target - ni]:
                continue
            # return the indices of ni and its complement
            return i, num_to_index[target - ni]
    # else
    return None


def three_sum(nums, target=0, distinct=True):
    """
    Return the indices of three numbers in `nums` that sum to `target` if such
    numbers exist; None otherwise.
    
    nums -- a list of numbers
    target -- a number (default 0)
    distinct -- if True only return distinct indices, i.e. there must be three
                entries (not necessarily with distinct values) that sum to
                target - we don't accept a single entry being repeated; 
                allow repeats otherwise
    
    Time complexity: O(n**2)
    Space complexity: O(n**2)
    """
    # insert all nk's in a dict, which will remember their index in `nums`
    num_to_index = dict()
    for k, nk in enumerate(nums):
        num_to_index[nk] = k
    # iterate through pairs in `nums`
    for i, ni in enumerate(nums):
        # j takes values from i onwards
        for j, nj in enumerate(itertools.islice(nums, start=i, stop=None), 
                               start=i):
            # if (ni + nj)'s complement (w.r.t. target) exists
            if (target - ni - nj) in num_to_index:
                k = num_to_index[target - ni - nj]
                # do we want distinct entries? or do we allow repeats?
                if distinct and (i == j or i == k or j == k):
                    continue
                return i, j, k
    # else
    return None
