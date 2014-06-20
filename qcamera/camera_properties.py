"""Camera properties"""

import json
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
            'pixels': [0, 0],

            # Bits per pixel. This could conceivably be a tuple if a
            # color camera. The pixel_mode attribute specifies if it
            # is mono or some form of color.
            'depth': 8,
            'pixel_mode': 'mono',

            # Available trigger modes
            'trigger_modes': ['software'],

            # Functionality flags
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            # Can hardware cropping be set?
            'crop': False,

            # Can the gain be adjusted?
            'gain_adjust': False,

            # Is there a built-in tempurature controller for the
            # sensor?
            'temp_control': False,

            # Does the camera have a builtin shutter?
            'shutter': False,
        }

    def __getitem__(self, key):
        return self.props[key]

    def __setitem__(self, key, value):
        self.props[key] = value

    def __delitem__(self, key):
        self.props.popitem(key)

    def __iter__(self):
        pass # TODO

    # Loading and saving properties
    # -------------------------------------------------------------------------

    def save(self, filename):
        """Save the properties to a JSON file."""
        with open(filename, 'w') as outfile:
            json.dump(self.props, outfile, indent=2, sort_keys=True)

    def load(self, filename):
        """Load the properties from a JSON file."""
        with open(filename, 'r') as infile:
            props = json.load(infile)
            # TODO: this should check that keys are valid!
            self.props = props

if __name__ == "__main__":
    props = CameraProperties()
    props.save('test.json')

            