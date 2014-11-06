"""
Sort a sequence of items using the quicksort algorithm.

The default is to choose pivots uniformly at random. This can be overriden
though, by setting the choose_pivot module attribute to some other preferred
function with signature choose(sequence, index_l, index_r), which chooses one
of the items sequence[index_l:index_r] as the pivot and returns its index,
index_p, where index_l <= index_p < index_r.

Author:
  Christos Nitsas
  (nitsas)
  (chrisnitsas)

Language:
  Python 3(.4)

Date:
  October, 2014
"""


import random


__all__ = ['sort', 'quicksort', 'partition', 'choose_pivot_index',
           'choose_random_pivot_index']


def quicksort(sequence, begin=None, end=None):
    """
    Sort the items in the given (part of the) sequence in place.

    sequence -- A sequence of items that can be compared using the less than
                or equal (<=) operator. We assume that the sequence is
                indexable.
    begin -- The index of the first of the items that we want to sort.
             Default 0. (0 <= begin <= end must hold)
    end -- The index just past the last of the items that we want to sort.
           Default len(sequence). (begin <= end <= len(sequence) must hold)

    This does NOT produce a stable sort. A stable sort is one where, if two
    items compare equal their relative order is preserved, so that if one came
    before the other in the input, it will also come before the other in the
    output.
    """
    # default sort range indices
    if begin is None:
        begin = 0
    if end is None:
        end = len(sequence)
    # check for invalid indices:
    if not 0 <= begin <= end <= len(sequence):
        raise ValueError("0 <= begin <= end <= len(sequence) must hold")
    _quicksort_recurse(sequence, begin, end)
    return


sort = quicksort


def _quicksort_recurse(sequence, begin, end):
    """
    Sort the items in the given (part of the) sequence in place. (helper)

    sequence -- a sequence of items that can be compared using the less than
                or equal (<=) operators
    begin -- the index of the leftmost item we care about
    end -- one past the index of the rightmost item we care about
    """
    # check if at most one element
    if end - begin <= 1:
        return
    # choose pivot index
    index_p = choose_pivot_index(sequence, begin, end)
    # partition around the pivot and get the new index of the pivot
    index_p = partition(sequence, begin, end, index_p)
    # recurse on the left and right *halves*
    _quicksort_recurse(sequence, begin, index_p)
    _quicksort_recurse(sequence, index_p + 1, end)
    return


def partition(seq, begin, end, index_p):
    """
    Partition around the pivot and return the final index of the pivot.

    seq -- a sequence of items that can be compared using the less than or
           equal (<=) operator
    begin -- the index of the leftmost item we care about
    end -- one past the index of the rightmost item we care about
    index_p -- the (starting) index of the pivot

    When this function returns with result index_p, the original subsequence
    will be partitioned so that the items sequence[index_l:index_p] will be
    less than the pivot, and the items sequence[index_p+1:index_r]
    will be greater than the pivot.

    TODO:
    Won't this lead to quadratic behavior in sequences which contain only a
    single value multiple times? Everything will always compare less than or
    equal to any pivot. I can solve this by implementing a three-way "fat"
    partition, i.e. partition the elements into three groups, the elements
    less than the pivot, the items equal to the pivot, and the items greater
    than the pivot.
    """
    # the pivot (for readability)
    pivot = seq[index_p]
    # temporarily move the pivot to the end
    seq[end - 1], seq[index_p] = seq[index_p], seq[end - 1]
    # keep a separator pointing to the first item that might be
    # greater than the pivot
    separator = begin
    # compare each item to the pivot and move either the item
    # or the separator accordingly
    for i in range(begin, end - 1):
        if seq[i] <= pivot:
            # move it to where the separator is and advance the separator
            seq[separator], seq[i] = seq[i], seq[separator]
            separator += 1
        # else just advance i
    # this is the current state:
    # - everything to the left of separator is less than or equal to the pivot
    # - the separator points to the first item that is greater than the pivot
    # - everything to the right of the separator (except the last position) is
    # greater than the pivot
    # - the pivot is at the last position (end of the subsequence)
    # swap pivot and separator
    seq[separator], seq[end - 1] = seq[end - 1], seq[separator]
    # the separator now points to (i.e. is the index of) the pivot
    return separator


def choose_random_pivot_index(sequence, begin, end):
    """
    Choose a pivot uniformly at random and return its index.

    sequence -- a sequence of items that can be compared using the less than
                or equal operator (<=)
    begin -- the index of the leftmost item we care about
    end -- one past the index of the rightmost item we care about
    """
    return random.randrange(begin, end)


choose_pivot_index = choose_random_pivot_index
