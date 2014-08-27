"""
Error and warning types for qCamera exceptions.

TODO: Incorporate logging module with the error/warning types.

"""

from __future__ import print_function
import traceback

# Errors
# ======

class CameraError(Exception):
    """Generic camera errors."""
    pass

class AndorError(CameraError):
    """Andor-specific errors."""
    pass

class SensicamError(CameraError):
    """Sensicam errors."""
    pass

class ThorlabsDCxError(CameraError):
    """Thorlabs DCx series errors."""
    pass

class OpenCVError(CameraError):
    """Errors for OpenCV cameras."""
    pass

class CameraPropertiesError(Exception):
    """Error type for exceptions raised by CameraProperties
    objects.

    """
    pass

# Warnings
# ========

class CameraWarning(Warning):
    """Generic camera warnings."""
    def __str__(self):
        return repr(traceback.print_stack())

class AndorWarning(CameraWarning):
    """Andor-specific warnings."""
    pass

class SensicamWarning(CameraWarning):
    """Sensicam warnings."""

class ThorlabsDCxWarning(CameraWarning):
    """Thorlabs DCx series warnings."""
    pass

class OpenCVWarning(CameraWarning):
    """Warnings for OpenCV cameras."""
    pass
