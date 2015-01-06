"""
The binary search algorithm - search for an item inside a sorted list.

Also includes the bisect algorithm: 
Return the insertion point for an item x in a list to maintain sorted order. 
(again in logarithmic time)

Author:
  Christos Nitsas
  (nitsas)
  (chrisnitsas)

Language:
  Python 3(.4)

Date:
  November, 2014
"""


__all__ = ['search', 'binary_search', 'bisect']


def bisect(list_, x, begin=0, end=None):
    """
    Return the insertion point for x to maintain sorted order, in logarithmic 
    time.
    
    list_ -- the sorted list of items; we assume ascending order by default
    x -- the item we search for
    begin -- the first index of the range we want to search in
    end -- the index past end of the range we want to search in
    
    Search inside list_[begin:end]. 
    
    The result is an index i such as if we insert the item there, the list
    remains sorted.
    
    Time complexity: O(log(N)), where N is the length of the search range,
                     i.e. `N = end - begin`
    """
    # check input parameters
    if end is None:
        end = len(list_)
    if not 0 <= begin <= end <= len(list_):
        raise ValueError('0 <= begin <= end <= len(list_) must hold')
    if begin == end:
        return begin
    # we don't want to implement this recursively so that we won't have to
    # worry about Python's max recursion depth 
    # loop while the search range includes two or more items
    while end - begin > 1:
        # find the midpoint 
        mid = begin + (end - begin) // 2
        # "halve" the search range and continue searching 
        # in the appropriate half
        if x <= list_[mid]:
            end = mid
        else:
            begin = mid + 1
    # we are down to a search range of zero or one items; either:
    # - begin == end, which can happen if we search for an item that's bigger
    #   than every item in the list, or
    # - begin is the index of the only left item; end is the next index
    if begin == end or x <= list_[begin]:
        return begin
    else:
        return end


def binary_search(list_, x, begin=0, end=None):
    """
    Return the first index of x in `list_` (sorted); None if x is not in it.
    
    list_ -- a sorted list of items; by default we assume ascending order
    x -- the item we search for
    begin -- the first index of the range we want to search in (default: 0)
    end -- the index past end of the range we want to search in 
           (default: end of `list_`)
    
    If x occurs in the list multiple times, return the index of the first
    occurrence.
    
    Time complexity: O(log(N)), where N is the length of the search range,
                     i.e. `N = end - begin`
    """
    # get the index where we'd have to insert x to maintain sorted order
    index = bisect(list_, x, begin, end)
    # - check if `index` is within the list,
    # - also check if `index` points to an item that's equal to x 
    #   (it could be pointing to the first item that's greater than x, if 
    #   there's no x within the search range)
    if index < end and list_[index] == x:
        return index
    else:
        # x is not in the list
        return None


search = binary_search
