"""
Solve the linear Diophantine equation: a * x + b * y = c

Author:
  Christos Nitsas
  (nitsas)
  (chrisnitsas)

Language:
  Python 3(.3)

Date:
  March, 2014

Given a triplet of integers (a, b, c), a solution is a pair of 
integers (x, y) that satisfies the linear Diophantine equation:
a * x + b * y = c
"""


import sys
import numbers
# modules I've written:
import euclidean_alg


__all__ = ['solve']


def solve_linear_diophantine_equation(a, b, c):
    """
    Solve the linear Diophantine equation: a*x + b*y = c, and return a tuple.
    
    Return the tuple (x, y); or None if no solution exists.
    
    a -- an integer
    b -- an integer
    c -- an integer
    """
    for x in (a, b, c):
        if not isinstance(x, numbers.Integral):
            raise TypeError("can't find solution for non-ints")
    if c == 0:
        return 0, 0
    gcd, s, t = euclidean_alg.extended_gcd(a, b)
    if c % gcd != 0:
        return None
    else:
        #assert(a * s * c // gcd + b * t * c // gcd == c)
        return s * c // gcd, t * c // gcd


solve = solve_linear_diophantine_equation
