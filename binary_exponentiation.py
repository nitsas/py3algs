"""
Exponentiate quickly, using the binary exponentiation algorithm.

Also known as exponentiation by squaring, or square-and-multiply.

Author:
  Christos Nitsas
  (nitsas)
  (chrisnitsas)

Language:
  Python 3(.4)

Date:
  October, 2014
"""


__all__ = ['binary_exponentiation', 'power']


def binary_exponentiation(num, power):
    """
    Calculate num**power quickly (via binary exponentiation).
    
    num -- a number
    power -- an integer
    
    Also known as exponentiation by squaring, or square-and-multiply.
    """
    # check for valid input:
    if not isinstance(power, int):
        raise ValueError("power must be an integer")
    if power < 0:
        raise ValueError("power must be non-negative")
    # instantly take care of easy cases:
    if num == 0:
        return 0
    if num == -1 and power % 2 != 0:
        return -1
    if abs(num) == 1 or power == 0:
        return 1
    # calculate using the recursive helper function:
    return _recurse_binary_exponentiation(num, power)


power = binary_exponentiation


def _recurse_binary_exponentiation(num, power):
    """
    Recursively calculate num**power quickly (via binary exponentiation). 
    
    Helper function. We did parameter checks before so that we don't have to 
    do them inside every recursive call.
    """
    if power == 1:
        return num
    num_squared = num * num
    if power % 2 == 0:
        # power was even
        return _recurse_binary_exponentiation(num_squared, power // 2)
    else:
        # power was odd
        return num * _recurse_binary_exponentiation(num_squared, power // 2)
