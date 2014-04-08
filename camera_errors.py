"""
Error and warning types for qCamera exceptions.

"""

from __future__ import print_function
import traceback

# Errors
# ------

class CameraError(Exception):
    """Generic camera errors."""
    pass

class AndorError(CameraError):
    """Andor-specific errors."""
    pass

class UnitsError(Exception):
    """Errors caused by using inappropriate units."""
    pass

# Warnings
# --------

class CameraWarning(Warning):
    """Generic camera warnings."""
    def __str__(self):
        return repr(traceback.print_stack())

class AndorWarning(CameraWarning):
    """Andor-specific warnings."""
    pass
