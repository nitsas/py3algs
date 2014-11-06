"""
Select kth smallest element of a list using the quickselect algorithm.

Author:
  Christos Nitsas
  (nitsas)
  (chrisnitsas)

Language:
  Python 3(.4)

Date:
  March, 2014
"""


import random


__all__ = ['select', 'quickselect', 'partition']


def quickselect(list_, k, begin=None, end=None):
    """
    Select and return the kth smallest item of a sublist. (k >= 0)
    
    list_ -- A list of items that can be compared using the less than or 
             equal (<=) operator.
    k -- An integer; 0 <= k < len(list_) must hold.
    begin -- The index of the first of the items we care about.
    end -- The index just past the last of the items we care about.
    
    This doesn't mutate the original list.
    """
    # default range indices
    if begin is None:
        begin = 0
    if end is None:
        end = len(list_)
    # check for invalid range indices
    if not 0 <= begin <= end <= len(list_):
        raise ValueError("0 <= begin <= end <= len(list_) must hold")
    # check for invalid k
    if not 0 <= k < (end - begin):
        raise ValueError("0 <= k < (end - begin) must hold")
    # make a copy of the (sub)list, so that we don't mutate the original
    list_copy = list_[begin:end]
    # let the recursive helper do the actual work
    return _quickselect(list_copy, k, 0, len(list_copy))


select = quickselect


def _quickselect(list_, k, begin, end):
    """
    Select and return the kth smallest item of a sublist. (k >= 0) (helper)

    list_ -- A list of items that can be compared using the less than or 
             equal (<=) operator.
    k -- An integer; 0 <= k < (end - begin) must hold.
    begin -- The index of the first of the items we care about.
    end -- The index just past the last of the items we care about.

    This helper function is called recursively to do the actual work.
    
    Search for and return the k-th smallest element in the sublist 
    list_[begin:end], k=0 being the min element.
    """
    assert(begin < end)
    assert(0 <= k < (end-begin))
    if end == begin + 1:
        # i.e. only one element
        return list_[begin]
    #pivotIndex = random.randrange(begin, end)
    pivotIndex = begin
    # Partition the sublist (list_[begin:end]) into three parts, a left 
    # sublist with elements less than or equal to the pivot, the pivot itself, 
    # and a right sublist with elements greater than the pivot.
    pivotIndex = partition(list_, begin, end, pivotIndex)
    # The pivot should now be in its final sorted position in the sublist.
    if k == pivotIndex-begin:
        return list_[pivotIndex]
    elif k < pivotIndex-begin:
        # the k'th smallest element is in the left sublist
        return _quickselect(list_, begin, pivotIndex, k)
    else:
        # k > pivotIndex-begin
        # The k'th smallest item of the original (sub)list, is the 
        # (pivotIndex - begin + 1)'th smallest item of the right (sub)sublist.
        return _quickselect(list_, pivotIndex+1, end, k - (pivotIndex-begin+1))


def partition(list_, begin, end, pivotIndex):
    """
    Partition a sublist around a pivot and return the final pivot index.
    
    list_ -- A list of items that can be compared using the less than or 
             equal (<=) operator.
    begin -- The index of the first of the items we care about.
    end -- The index just past the last of the items we care about.
    pivotIndex -- the (initial) index of the pivot
    
    Partition the sublist list_[begin:end] into three parts:
    - left,  which contains all items less or equal to the pivot,
    - pivot, the pivot item itself, and
    - right, which contains all items greater than or equal to the pivot
    """
    pivot = list_[pivotIndex]
    # move pivot to the end
    list_[pivotIndex], list_[end-1] = list_[end-1], list_[pivotIndex]
    # storeIndex will point to the first element that is greater than or
    # equal to the pivot (initially points to the leftmost element)
    storeIndex = begin
    for i in range(begin, end-1):
        if list_[i] < pivot:
            list_[i], list_[storeIndex] = list_[storeIndex], list_[i]
            storeIndex += 1
    # now everything before storeIndex is less than the pivot, and storeIndex
    # points to the first item that is greater than or equal to the pivot;
    # move pivot back to where storeIndex points
    list_[storeIndex], list_[end-1] = list_[end-1], list_[storeIndex]
    return storeIndex
