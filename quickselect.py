"""
Select ith smallest element of a list using the quickselect algorithm.

The input should be a list (or some other list-like container). Its elements
must admit a total order denoted by a less-than-or-equal operator.
"""


import random
import copy


__all__ = ['select', 'quickselect', 'partition']


def quickselect(sequence, k):
    """
    The quickselect algorithm. Uses the partition algorithm.
    sequence is a sequence (unsorted)
    we are searching for the k'th smallest element in the sequence
    """
    assert(k >= 0)
    assert(k < len(sequence))
    return _quickselect(copy.copy(sequence), 0, len(sequence), k)


select = quickselect


def _quickselect(sequence, left, right, k):
    """
    This function is called recursively to do the actual work.
    sequence is a sequence
    left is an index
    right is an index
    k is a natural number
    we search for the k-th smallest element in the subsequence, searching
    only between left and right (i.e. sequence[left:right] - similar
    to slice notation)
    """
    assert(left < right)
    assert(0 <= k < (right-left))
    if right == left + 1:
        # i.e. only one element
        return sequence[left]
    #pivotIndex = random.randrange(left, right)
    pivotIndex = left
    pivotIndex = partition(sequence, left, right, pivotIndex)
    # Partition the subsequence (sequence[left:right]) into three parts,
    # a left subsequence with elements less than sequence[pivotIndex], the
    # element sequence[pivotIndex], and a right subsequence with elements
    # greater than or equal to sequence[pivotIndex].
    # The pivot should now be in its final sorted position in the subsequence.
    if k == pivotIndex-left:
        return sequence[pivotIndex]
    elif k < pivotIndex-left:
        # the k'th smallest element is in the left subsequence
        return _quickselect(sequence, left, pivotIndex, k)
    else:
        # k > pivotIndex-left
        return _quickselect(sequence, pivotIndex+1, right, k - (pivotIndex-left+1))


def partition(sequence, left, right, pivotIndex):
    """
    Partition the subsequence sequence[left:right] into three parts:
    lseq - which contains all elements less than sequence[pivot],
    pivot - the element sequence[pivotIndex], and
    rseq - which contains all elements greater than or equal to pivot
    """
    pivot = sequence[pivotIndex]
    # move pivot to the end
    sequence[pivotIndex], sequence[right-1] = sequence[right-1], sequence[pivotIndex]
    # storeIndex will point to the first element that is greater than or
    # equal to the pivot (initially points to the leftmost element)
    storeIndex = left
    for i in range(left, right-1):
        if sequence[i] < pivot:
            sequence[i], sequence[storeIndex] = sequence[storeIndex], sequence[i]
            storeIndex += 1
    # now everything before storeIndex is less than the pivot, and storeIndex
    # points to the first item that is greater than or equal to the pivot;
    # move pivot back to where storeIndex points
    sequence[storeIndex], sequence[right-1] = sequence[right-1], sequence[storeIndex]
    return storeIndex
