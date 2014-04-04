"""
Error types for qCamera exceptions.

"""

from __future__ import print_function

class UnitsError(Exception):
    """Errors caused by using inappropriate units."""

    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)
    
