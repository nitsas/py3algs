"""
Count the number of inversions in a sequence of orderable items.

Description:
  Informally, when we say inversion we mean inversion from the (ascending) 
  sorted order.
  
  For a more formal definition, let's call the list of items L. We call
  inversion a pair of indices i, j with i < j and L[i] > L[j], where L[i] is
  the ith item of the list and L[j] the jth one.
  
  In a given list of size N there could be up to O(N^2) inversions. To do the
  counting efficiently (i.e. in O(N*log(N)) time) we use a divide and conquer 
  approach. More specifically, we piggyback on the mergesort algorithm.

Author:
  Christos Nitsas
  (nitsas)
  (chrisnitsas)

Language:
  Python 3(.4)

Date:
  October, 2014
"""


__all__ = ['count_inversions', 'count']


def count_inversions(sequence):
    """
    Count the number of inversions in the sequence and return an integer.
    
    sequence -- a sequence of items that can be compared using <=
                we assume the sequence is sliceable
    
    We count inversions from the ascending order.
    This will piggyback on the mergesort divide and conquer algorithm.
    """
    sorted_sequence, num_inversions = mergesort_and_count(sequence)
    return num_inversions


count = count_inversions


def mergesort_and_count(sequence):
    """
    Sort the sequence into a list (call this "merged"), count the number "N" 
    of inversions, and return a tuple with "merged" and "N".
    """
    if len(sequence) <= 1:
        return (sequence, 0)
    left = sequence[:len(sequence)//2]
    right = sequence[len(sequence)//2:]
    return merge_and_count_inversions(mergesort_and_count(left), 
                                      mergesort_and_count(right))


def merge_and_count_inversions(left_tuple, right_tuple):
    """
    Count the number of split inversions while merging the given results of 
    the left and right subproblems and return a tuple containing the 
    resulting merged sorted list and the total number of inversions.
    
    left_tuple -- a tuple containing the sorted sublist and the count of
                  inversions from the left subproblem 
    right_tuple -- a tuple containing the sorted sublist and the count of
                  inversions from the right subproblem
    
    We call split inversions the pairs of items where the larger item is in 
    the left subsequence and the smaller item is in the right. 
    
    The total number of inversions "count_total" is:
    count_total = count_left + count_right + count_split,
    where "count_left", "count_right" are the number of inversions in the 
    left and right subsequence respectively and "count_split" is the number 
    of split inversions.
    """
    left, count_left = left_tuple
    right, count_right = right_tuple
    merged, count_split = list(), 0
    # Careful! 
    # If we use list slicing in the following loop we might end up with 
    # worse than O(L*log(L)) complexity. We will use indices instead.
    index_l, index_r = 0, 0
    while len(left) - index_l > 0 and len(right) - index_r > 0:
        if left[index_l] <= right[index_r]:
            merged.append(left[index_l])
            index_l += 1
            # no inversions discovered here
        else:
            # the item right[index_r] is smaller than every item in
            # left[index_l:]
            merged.append(right[index_r])
            index_r += 1
            # all the items of left[index_l:] formed inversions with the 
            # item we just appended to "merged"
            count_split += len(left) - index_l
    if len(left) - index_l > 0:
        merged.extend(left[index_l:])
        # no more inversions
    elif len(right) - index_r > 0:
        merged.extend(right[index_r:])
        # no more inversions
    count_total = count_left + count_right + count_split
    return (merged, count_total)
