"""Camera properties"""

import os.path
import json
# TODO: don't allow updating of properties that don't exist in the
# default self.props set in __init__
from camera_errors import CameraPropertiesError

PATH = os.path.split(os.path.abspath(__file__))[0]

class CameraProperties(object):
    """Class used for storing properties of the camera in use and
    flags about what functionality is supported.

    """
    
    # Basic functions
    # -------------------------------------------------------------------------
    
    def __init__(self, filename=None, **kwargs):
        """Without kwargs passed, populate the base properties
        dict. Otherwise, populate as appropriate. See self.props for
        valid keyword arguments.

        Parameters
        ----------
        filename : str or None
            If passed, the path to a JSON file that sets all the
            camera properties.

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
            'trigger_modes': ['internal'],

            # Available acquisition modes
            'acquisition_modes': ['continuous'],

            # List of valid values for binning
            'bins': [1],

            # Functionality flags
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            # Can hardware cropping be set?
            'hardware_crop': False,

            # Can the gain be adjusted?
            'gain_adjust': False,

            # Is there a built-in tempurature controller for the
            # sensor?
            'temp_control': False,

            # Does the camera have a builtin shutter?
            'shutter': False,
        }

        # Update parameters from a file if given.
        if filename is not None:
            self.load(filename)

    def __getitem__(self, key):
        return self.props[key]

    def __setitem__(self, key, value):
        self.props[key] = value

    def __delitem__(self, key):
        self.props.popitem(key)

    def __iter__(self):
        pass # TODO

    def update(self, props):
        """Update the props dict."""
        assert isinstance(props, dict)
        self.props.update(props)

    # Loading and saving properties
    # -------------------------------------------------------------------------

    # Definitions of basic camera properties can be stored in a JSON
    # file so that we only need to determine at runtime a few
    # differing parameters that change depending on the specific model
    # of camera being used. For example, the Andor SDK supports
    # several different specific cameras, but some functionality
    # depends on the physical camera being used. Most of the
    # capabilities for all models is the same, however, and so these
    # generic values are stored in a file and only the few that are
    # camera-specific are queried for.

    def save(self, filename):
        """Save the properties to a JSON file."""
        with open(os.path.join(PATH, 'props', filename), 'w') as outfile:
            json.dump(self.props, outfile, indent=4, sort_keys=True)

    def load(self, filename):
        """Load the properties from a JSON file."""
        with open(os.path.join(PATH, 'props', filename), 'r') as infile:
            props = json.load(infile)
            # TODO: this should check that keys are valid!
            self.props = props

if __name__ == "__main__":
    props = CameraProperties()
    props.save('test.json')

            