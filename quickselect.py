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


def _quickselect(list_, left, right, k):
    """
    This function is called recursively to do the actual work.
    list_ is a list
    left is an index
    right is an index
    k is a natural number
    we search for the k-th smallest element in the sublist, searching
    only between left and right (i.e. list_[left:right] - similar
    to slice notation)
    """
    assert(left < right)
    assert(0 <= k < (right-left))
    if right == left + 1:
        # i.e. only one element
        return list_[left]
    #pivotIndex = random.randrange(left, right)
    pivotIndex = left
    pivotIndex = partition(list_, left, right, pivotIndex)
    # Partition the sublist (list_[left:right]) into three parts,
    # a left sublist with elements less than list_[pivotIndex], the
    # element list_[pivotIndex], and a right sublist with elements
    # greater than or equal to list_[pivotIndex].
    # The pivot should now be in its final sorted position in the sublist.
    if k == pivotIndex-left:
        return list_[pivotIndex]
    elif k < pivotIndex-left:
        # the k'th smallest element is in the left sublist
        return _quickselect(list_, left, pivotIndex, k)
    else:
        # k > pivotIndex-left
        return _quickselect(list_, pivotIndex+1, right, k - (pivotIndex-left+1))


def partition(list_, left, right, pivotIndex):
    """
    Partition the sublist list_[left:right] into three parts:
    lseq - which contains all elements less than list_[pivot],
    pivot - the element list_[pivotIndex], and
    rseq - which contains all elements greater than or equal to pivot
    """
    pivot = list_[pivotIndex]
    # move pivot to the end
    list_[pivotIndex], list_[right-1] = list_[right-1], list_[pivotIndex]
    # storeIndex will point to the first element that is greater than or
    # equal to the pivot (initially points to the leftmost element)
    storeIndex = left
    for i in range(left, right-1):
        if list_[i] < pivot:
            list_[i], list_[storeIndex] = list_[storeIndex], list_[i]
            storeIndex += 1
    # now everything before storeIndex is less than the pivot, and storeIndex
    # points to the first item that is greater than or equal to the pivot;
    # move pivot back to where storeIndex points
    list_[storeIndex], list_[right-1] = list_[right-1], list_[storeIndex]
    return storeIndex
