"""
A queue implemented using an array.

This should be more efficient than a queue implemented like a
linked list, because of locality of reference.

Note:
If we add pop_back and peek_back operations this could double as a
stack, but there's not much point. Python's list or collections.deque
can also function as stacks and will probably be more efficient.

Operations:
- __len__
- push
- pop
- peek

Warning:
Keep in mind that python's built-in collections.deque will probably
be more efficient than this.

Author:
  Chris Nitsas
  (nitsas)
  (nitsas.chris)

Language:
  Python 3(.4)

Date:
  May, 2016
"""


__all__ = ['CircularArrayQueue']


class CircularArrayQueue:
    """
    A queue implemented using an array.

    This should be more efficient than a queue implemented like a
    linked list, because of locality of reference.

    Warning:
    Keep in mind that python's built-in collections.deque will probably
    be more efficient than this.
    """
    
    def __init__(self, sequence=None):
        raise NotImplementedError()
    
    def __len__(self):
        raise NotImplementedError()
    
    def push(self, value):
        raise NotImplementedError()
    
    def pop(self):
        raise NotImplementedError()
    
    def peek(self):
        raise NotImplementedError()
