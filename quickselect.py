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
import copy


__all__ = ['select', 'quickselect', 'partition']


def quickselect(list_, k):
    """
    Select and return the kth smallest item of a list. (k >= 0)
    
    list_ -- A list of items that can be compared using the less than or 
             equal (<=) operator.
    k -- An integer; 0 <= k < len(list_) must hold.
    
    This doesn't mutate the original list.
    """
    assert(k >= 0)
    assert(k < len(list_))
    return _quickselect(copy.copy(list_), 0, len(list_), k)


select = quickselect


def _quickselect(list_, begin, end, k):
    """
    Select and return the kth smallest item of a sublist. (k >= 0) (helper)

    list_ -- A list of items that can be compared using the less than or 
             equal (<=) operator.
    begin -- The index of the first of the items we care about.
    end -- The index just past the last of the items we care about.
    k -- An integer; 0 <= k < (end - begin) must hold.

    This helper function is called recursively to do the actual work.
    
    Search for and return the k-th smallest element in the sublist 
    list_[begin:end]. 
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
