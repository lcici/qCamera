"""Camera properties"""

from camera_errors import CameraPropertiesError

class CameraProperties(object):
    """Class used for storing properties of the camera in use and
    flags about what functionality is supported.

    """
    
    # Dunder functions
    # -------------------------------------------------------------------------
    
    def __init__(self, **kwargs):
        """Without kwargs passed, populate the base properties
        dict. Otherwise, populate as appropriate. See self.props for
        valid keyword arguments.

        """
        self.props = {
            # Generic properties
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
            # Number of horizontal and vertical pixels
            'width': None,
            'height': None,

            # Functionality flags
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            # Can the gain be adjusted?
            'gain_adjust': False,

            # Is there a built-in tempurature controller for the
            # sensor?
            'temp_control': False,

            # Does the camera have a builtin shutter?
            'shutter': False,

            # Color camera?
            'color': False,
        }

    def __getitem__(self, key):
        return self.props[key]

    def __setitem__(self, key, value):
        self.props[key] = value

    def __delitem__(self, key):
        self.props.popitem(key)

    def __iter__(self):
        pass # TODO

            