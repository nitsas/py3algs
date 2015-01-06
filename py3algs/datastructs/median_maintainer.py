"""
Maintain the median of a stream of items online (i.e. in real-time).

Operations:  
- __len__
- insert 
- median

Author:  
  Christos Nitsas  
  (nitsas)  
  (chrisnitsas)

Language:
  Python 3(.4)

Date:
  November, 2014
"""


import sys
# modules I've implemented
import binary_heap


__all__ = ['MedianMaintainer', 'EvenChoice']


if sys.version_info[:2] >= (3, 4):
    # Python 3.4 and above
    import enum
    class EvenChoice(enum.Enum):
        Lower = 1
        Higher = 2
        Both = 3
        Average = 4
else:
    # below Python 3.4
    class EvenChoice:
        Lower = 1
        Higher = 2
        Both = 3
        Average = 4


class MedianMaintainer:
    """
    Maintain the median of a stream of items online (i.e. in real-time).
    
    The user can insert arbitrary items that can be compared to each other, 
    and after each insertion retrieve the median of the items inserted so far.
    
    Complexity:
    - each insertion is O(log(n)), where n is the number of items inserted 
    so far
    - retrieving the median is O(1) (constant time), at any point
    
    This works by using two binary heaps:
    - a max heap called `lower_half`, which includes the lower half of the
      items inserted so far
    - a min heap called `higher_half`, which includes the higher half of the
      items inserted so far
    
    At each point the median will be one of the two items on top of the heaps.
    If the total number N of items is even return the N/2th item.
    """
    
    def __init__(self):
        """
        Initialize an empty structure.
        """
        # a max heap for the lower half of items
        self.lower_half = binary_heap.BinaryHeap(max_=True)
        # a min heap for the higher half of items
        self.higher_half = binary_heap.BinaryHeap(max_=False)
    
    def __len__(self):
        """
        Return the number of items inserted so far.
        """
        return len(self.lower_half) + len(self.higher_half)
    
    def insert(self, item):
        """
        Insert item in the structure.
        
        item -- an item; we assume it can be compared with all other items in
                the structure
        
        Complexity is O(log(n)), where n is the number of items inserted so
        far.
        """
        try:
            median = self.median()
        except LookupError:
            # no items yet; insert this in the lower half
            self.lower_half.insert(item)
            return
        # compare to the current median, to decide where the item must go
        if item < median:
            # insert into the lower_half of items
            self.lower_half.insert(item)
            # heap sizes must differ at most by one item; else we cannot
            # compute the median using the heaps' top items
            if len(self.lower_half) > len(self.higher_half) + 1:
                # transfer top item in lower_half to higher_half
                self.higher_half.insert(self.lower_half.pop())
        elif item > median:
            # insert into the higher_half of items
            self.higher_half.insert(item)
            # heap sizes must differ at most by one item; else we cannot
            # compute the median using the heaps' top items
            if len(self.higher_half) > len(self.lower_half) + 1:
                # transfer top item in higher_half to lower_half
                self.lower_half.insert(self.higher_half.pop())
        else:
            # insert into the smaller heap (lower_half if same size)
            if len(self.higher_half) < len(self.lower_half):
                self.higher_half.insert(item)
            else:
                self.lower_half.insert(item)
    
    def median(self, if_even=EvenChoice.Lower):
        """
        Return the median of the items inserted so far.
        
        if_even -- Choose what to return if the number of items inserted so
                   far is even, i.e. there is no single median. Choices are:
                   - EvenChoice.Lower, for the lower of the two "medians",
                     i.e. the N/2th item (default)
                   - EvenChoice.Higher, for the higher of the two "medians",
                     i.e. the (N/2 + 1)th item
                   - EvenChoice.Both, for a tuple of both "medians"
                   - EvenChoice.Average, for the average of the two "medians"
        
        Raises LookupError if no items have been inserted.
        """
        if len(self) == 0:
            raise LookupError('median of no items')
        # compare number of items in each heap
        if len(self.lower_half) > len(self.higher_half):
            # single median
            return self.lower_half.peek()
        elif len(self.lower_half) < len(self.higher_half):
            # single median
            return self.higher_half.peek()
        else:
            # number of inserted items is even, so there is no single
            # median, we have two "medians"
            # the user can choose what we'll return
            if if_even == EvenChoice.Higher:
                # the (N/2 + 1)th item
                return self.higher_half.peek()
            elif if_even == EvenChoice.Both:
                # a tuple with both "medians"
                return (self.lower_half.peek(), self.higher_half.peek())
            elif if_even == EvenChoice.Average:
                # try to return the average of the two "medians"
                # (takes care of potential overflows)
                return self.lower_half.peek() + \
                       (self.higher_half.peek() - \
                        self.lower_half.peek()) / 2
            else: 
                # if_even == EvenChoice.Lower or unknown option
                # return the N/2th item (default)
                return self.lower_half.peek()
