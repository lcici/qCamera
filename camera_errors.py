"""
Error types for qCamera exceptions.

"""

from __future__ import print_function

class CameraError(Exception):
    """Generic camera errors."""
    pass

class AndorError(CameraError):
    """Andor-specific errors."""
    pass

class UnitsError(Exception):
    """Errors caused by using inappropriate units."""
    pass
