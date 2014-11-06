"""
Select ith smallest element of a list using the quickselect algorithm.

The input should be a list (or some other list-like container). Its elements
must admit a total order denoted by a less-than operator.
"""


import random
import copy


__all__ = ['select', 'quickselect', 'partition']


def quickselect(list_, k):
    """
    The quickselect algorithm. Uses the partition algorithm.
    list_ is a list (unsorted)
    we are searching for the k'th smallest element in the list
    """
    assert(k >= 0)
    assert(k < len(list_))
    return _quickselect(copy.copy(list_), 0, len(list_), k)


select = quickselect


def _quickselect(list_, begin, end, k):
    """
    This function is called recursively to do the actual work.
    list_ is a list
    begin is an index
    end is an index
    k is a natural number
    we search for the k-th smallest element in the sublist, searching
    only between begin and end (i.e. list_[begin:end] - similar
    to slice notation)
    """
    assert(begin < end)
    assert(0 <= k < (end-begin))
    if end == begin + 1:
        # i.e. only one element
        return list_[begin]
    #pivotIndex = random.randrange(begin, end)
    pivotIndex = begin
    pivotIndex = partition(list_, begin, end, pivotIndex)
    # Partition the sublist (list_[begin:end]) into three parts,
    # a left sublist with elements less than list_[pivotIndex], the
    # element list_[pivotIndex], and a right sublist with elements
    # greater than or equal to list_[pivotIndex].
    # The pivot should now be in its final sorted position in the sublist.
    if k == pivotIndex-begin:
        return list_[pivotIndex]
    elif k < pivotIndex-begin:
        # the k'th smallest element is in the left sublist
        return _quickselect(list_, begin, pivotIndex, k)
    else:
        # k > pivotIndex-begin
        return _quickselect(list_, pivotIndex+1, end, k - (pivotIndex-begin+1))


def partition(list_, begin, end, pivotIndex):
    """
    Partition the sublist list_[begin:end] into three parts:
    lseq - which contains all elements less than list_[pivot],
    pivot - the element list_[pivotIndex], and
    rseq - which contains all elements greater than or equal to pivot
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
