"""
Sort a list of items using the quicksort algorithm.

The default is to choose pivots uniformly at random. This can be overriden
though, by setting the choose_pivot module attribute to some other preferred
function with signature choose(list_, index_l, index_r), which chooses one
of the items list_[index_l:index_r] as the pivot and returns its index,
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
           'choose_pivot_index_random', 'choose_pivot_index_median_of_three']


def quicksort(list_, begin=None, end=None):
    """
    Sort the items in the given (part of the) list in place.

    list_ -- A list of items that can be compared using the less than
             or equal (<=) operator.
    begin -- The index of the first of the items that we want to sort.
             Default 0. (0 <= begin <= end must hold)
    end -- The index just past the last of the items that we want to sort.
           Default len(list_). (begin <= end <= len(list_) must hold)

    This does NOT produce a stable sort. A stable sort is one where, if two
    items compare equal their relative order is preserved, so that if one came
    before the other in the input, it will also come before the other in the
    output.
    """
    # default sort range indices
    if begin is None:
        begin = 0
    if end is None:
        end = len(list_)
    # check for invalid indices:
    if not 0 <= begin <= end <= len(list_):
        raise ValueError("0 <= begin <= end <= len(list_) must hold")
    _quicksort_recurse(list_, begin, end)
    return


sort = quicksort


def _quicksort_recurse(list_, begin, end):
    """
    Sort the items in the given (part of the) list in place. (helper)

    list_ -- a list of items that can be compared using the less than
             or equal (<=) operators
    begin -- the index of the leftmost item we care about
    end -- one past the index of the rightmost item we care about
    """
    # check if at most one element
    if end - begin <= 1:
        return
    # choose pivot index
    index_p = choose_pivot_index(list_, begin, end)
    # partition around the pivot and get the new index of the pivot
    index_p = partition(list_, begin, end, index_p)
    # recurse on the left and right *halves*
    _quicksort_recurse(list_, begin, index_p)
    _quicksort_recurse(list_, index_p + 1, end)
    return


def partition(list_, begin, end, index_p):
    """
    Partition around the pivot and return the final index of the pivot.

    list_ -- a list of items that can be compared using the less than or
             equal (<=) operator
    begin -- the index of the leftmost item we care about
    end -- one past the index of the rightmost item we care about
    index_p -- the (starting) index of the pivot

    When this function returns with result index_p, the original sublist will
    be partitioned so that the items list_[index_l:index_p] will be less than
    the pivot, and the items list_[index_p+1:index_r] will be greater than the
    pivot.

    TODO:
    Won't this lead to quadratic behavior in lists which contain only a
    single value multiple times? Everything will always compare less than or
    equal to any pivot. I can solve this by implementing a three-way "fat"
    partition, i.e. partition the elements into three groups, the elements
    less than the pivot, the items equal to the pivot, and the items greater
    than the pivot.
    """
    # the pivot (for readability)
    pivot = list_[index_p]
    # temporarily move the pivot to the end
    list_[end - 1], list_[index_p] = list_[index_p], list_[end - 1]
    # keep a separator pointing to the first item that might be
    # greater than the pivot
    separator = begin
    # compare each item to the pivot and move either the item
    # or the separator accordingly
    for i in range(begin, end - 1):
        if list_[i] <= pivot:
            # move it to where the separator is and advance the separator
            list_[separator], list_[i] = list_[i], list_[separator]
            separator += 1
        # else just advance i
    # this is the current state:
    # - everything to the left of separator is less than or equal to the pivot
    # - the separator points to the first item that is greater than the pivot
    # - everything to the right of the separator (except the last position) is
    # greater than the pivot
    # - the pivot is at the last position (end of the sublist)
    # swap pivot and separator
    list_[separator], list_[end - 1] = list_[end - 1], list_[separator]
    # the separator now points to (i.e. is the index of) the pivot
    return separator


def choose_pivot_index_random(list_, begin, end):
    """
    Choose a pivot uniformly at random and return its index.

    list_ -- a list of items that can be compared using the less than
             or equal operator (<=)
    begin -- the index of the leftmost item we care about
    end -- one past the index of the rightmost item we care about
    """
    return random.randrange(begin, end)


def choose_pivot_index_median_of_three(sequence, index_l, index_r):
    """
    Choose the pivot using the median-of-three rule and return its index. 
    
    sequence -- the sequence of items to sort
    index_l -- the index of the first of the items that we want to sort 
    index_r -- the index just past the end of the items that we want to sort
    """
    # the first element:
    item_l = sequence[index_l]
    # the last element:
    item_r = sequence[index_r - 1]
    # the middle element:
    if (index_r - index_l) % 2 == 0:
        index_m = index_l + (index_r - index_l) // 2 - 1
        item_m = sequence[index_m]
    else:
        index_m = index_l + (index_r - index_l) // 2 
        item_m = sequence[index_m]
    assert(index_l <= index_m <= index_r)
    # find which of the three is the median element (i.e. the middle of the
    # three when sorted):
    min_ = min(item_l, item_m, item_r)
    if min_ == item_l:
        if max(item_m, item_r) == item_r:
            return index_m
        else:
            return index_r - 1
    elif min_ == item_m:
        if max(item_l, item_r) == item_r:
            return index_l
        else:
            return index_r - 1
    else:
        if max(item_l, item_m) == item_m:
            return index_l
        else:
            return index_m


choose_pivot_index = choose_pivot_index_random
