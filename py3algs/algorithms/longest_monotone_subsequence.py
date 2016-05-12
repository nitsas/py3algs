"""
Implementations of longest increasing/decreasing subsequence algorithms.

Author:
  Christos Nitsas
  (nitsas)
  (nitsas.chris)

Language:
  Python 3(.4)

Date:
  May, 2016
"""


__all__ = []


def longest_monotone_subsequence(sequence, increasing=True, strictly_monotone=True):
    """
    Return the longest increasing/decreasing subsequence of the given sequence.
    
    sequence -- the sequence whose subsequences we examine
    increasing -- if truthy, look for the longest increasing subsequence;
                  otherwise look for the longest decreasing one
    strictly_monotone -- if truthy, look for strictly increasing/decreasing
                         subsequences; otherwise, allow non-decreasing/
                         non-increasing subsequences respectively
    
    Result will be a sequence.
    """
    
    raise NotImplementedError()


def longest_increasing_subsequence(sequence, strictly_monotone=True):
    """
    Return the longest increasing subsequence of the given sequence.
    
    sequence -- the sequence whose subsequences we examine
    strictly_monotone -- if truthy, look for strictly increasing/decreasing
                         subsequences; otherwise, allow non-decreasing/
                         non-increasing subsequences respectively
    
    Result will be a sequence.
    """
    
    return longest_monotone_subsequence(sequence, increasing=True)


def longest_decreasing_subsequence(sequence, strictly_monotone=True):
    """
    Return the longest decreasing subsequence of the given sequence.
    
    sequence -- the sequence whose subsequences we examine
    strictly_monotone -- if truthy, look for strictly increasing/decreasing
                         subsequences; otherwise, allow non-decreasing/
                         non-increasing subsequences respectively
    
    Result will be a sequence.
    """
    
    return longest_monotone_subsequence(sequence, increasing=False)
