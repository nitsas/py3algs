"""
Compute the greatest common divisor (gcd) of a pair of integers.

Includes the extended Euclidean algorithm for finding the gcd.

Author:
  Christos Nitsas
  (nitsas)
  (chrisnitsas)

Language:
  Python 3(.3)

Date:
  March, 2014
"""


import numbers


__all__ = ['gcd', 'extended_gcd']


def gcd(a, b):
    """
    Computes the greatest common divisor of integers a, b and returns an int.
    
    input parameters:
    a -- an integer (isinstance(a, numbers.Integral) must hold)
    b -- an integer (isinstance(a, numbers.Integral) must hold)
    """
    # input must be integers
    if not isinstance(a, numbers.Integral) or \
       not isinstance(b, numbers.Integral):
        raise TypeError("Can't find gcd of non-integral objects '" + \
                        a.__class__.__name__ + "' and '" + \
                        b.__class__.__name__ + "'")
    # we only need to solve the case where: a >= b >= 0
    if not (a >= b >= 0):
        a, b = max(abs(a), abs(b)), min(abs(a), abs(b))
    # main loop
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    """
    Computes the greatest common divisor (gcd) of integers a, b plus a pair of 
    Bezout's coefficients s, t and returns the tuple (gcd, s, t).
    
    A pair s, t of Bezout's coefficients are integers that, together with the
    input parameters a, b, satisfy the equation:
    a * s + b * t = gcd
    In fact, this returns one minimum such pair.
    
    input parameters:
    a -- an integer (isinstance(a, numbers.Integral) must hold)
    b -- an integer (isinstance(a, numbers.Integral) must hold)
    """
    
    # input must be integers
    if not isinstance(a, numbers.Integral) or \
       not isinstance(b, numbers.Integral):
        raise TypeError("Can't find gcd of non-integral objects '" + \
                        a.__class__.__name__ + "' and '" + \
                        b.__class__.__name__ + "'")
    
    # make the necessary conversions so that we only need to solve 
    # the case where: a >= b >= 0
    if not (a >= b >= 0):
        aa, bb = max(abs(a), abs(b)), min(abs(a), abs(b))
        # call this recursively with aa and bb, where: aa >= bb >= 0
        # don't worry, we'll get at most 1 recursive call
        gcd, s, t = extended_gcd(aa, bb)
        # figure out the result for (a, b) from the result for (aa, bb)
        if abs(b) >= abs(a):
            s, t = t, s
        if a < 0:
            s = -s
        if b < 0:
            t = -t
        return gcd, s, t
    
    #assert(a >= b >= 0)
    
    # we'll mutate a, b, remember them if you'll use the assertion below
    #orig_a, orig_b = a, b
    
    # initialization
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    # main loop
    while b != 0:
        k = a // b
        r = a % b
        old_s, s = s, old_s - k * s
        old_t, t = t, old_t - k * t
        #assert(r == orig_a * s + orig_b * t)
        a, b = b, r
    
    # when the current a was r, the current old_s and old_t were s and t
    # and they all satisfied: r == orig_a*s + orig_b*t
    # they are the solution we were looking for
    gcd, s, t = a, old_s, old_t
    
    return gcd, s, t
