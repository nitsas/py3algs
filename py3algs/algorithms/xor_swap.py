"""
Swap two variables' contents without using a 3rd variable.

Not really useful in Python since you can do: `a, b = b, a`.

Author:
  Christos Nitsas
  (nitsas)
  (nitsas.chris)

Language:
  Python 3(.4)

Date:
  April, 2016
"""


__all__ = ['xor_swap']


def xor_swap(a, b):
    a ^= b        # invert those bits of a where b has 1s
    b ^= a        # reverse the above and store in b
    # current b is the original a
    # current a still has the result of the 1st operation
    #   but viewed differently:
    #   current a is original b with inverted bits where original a had 1s
    a ^= b        # use b (original a) to invert 1st operation & get original b
    return a, b
