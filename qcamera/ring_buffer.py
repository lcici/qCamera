"""Ring buffer for automatic storage of images"""

import os.path
import logging
from datetime import datetime
import numpy as np
from scipy.misc import imsave
import tables

class RingBuffer(object):
    """Ring buffer class.

    Attributes
    ----------
    directory : str
        Location to store the ring buffer file.
    recording : bool
        True when data is being saved to the ring buffer.
    N : int
        Number of images to store in the ring buffer.
    
    """
    
    def __init__(self, **kwargs):
        """Initialize the ring buffer.

        Keyword arguments
        -----------------
        N : int
            Number of images to store in the ring buffer.
        directory : str
            The directory to buffer images to.
        filename : str
            Filename to use for the HDF5 file.
        recording : bool
            Activate recording when True, disable when False.
        logger : str
            The name of the logger to use. Defaults to 'RingBuffer'.

        """
        directory = kwargs.get('directory', '.')
        filename = kwargs.get('filename', 'rbuffer.h5')
        recording = kwargs.get('recording', True)
        N = int(kwargs.get('N', 100))
        logger = kwargs.get('logger', 'RingBuffer')
        assert isinstance(directory, (str, unicode))
        assert isinstance(filename, (str, unicode))
        assert isinstance(recording, (int, bool))
        assert isinstance(logger, (str, unicode))
        
        self.recording = recording
        self.N = N
        self.logger = logging.getLogger(logger)
        self._index = 0

        # Initialize HDF5 database.
        path = os.path.join(directory, filename)
        self._db = tables.open_file(path, 'w', title="Ring Buffer")
        self._db.create_group('/', 'images', 'Buffered Images')

    def __enter__(self):
        return self

    def __exit__(self, type_, value, tb):
        self.close()

    def close(self):
        self._db.close()

    def get_current_index(self):
        """Return the current index. This is in a function to
        hopefully prevent the user from accessing _index directly
        which could lead to bad things if it is modified!

        """
        return self._index

    def write(self, data):
        """Write data to the ring buffer file."""
        if not self.recording:
            return
        name = 'img{:04d}'.format(self._index)
        try:
            self._db.get_node('/images/' + name).remove()
        except tables.NoSuchNodeError:
            pass
        finally:
            # TODO: Adapt to CArray for compression
            #filters = tables.Filters(complevel=5, complib='zlib')
            arr = self._db.create_array('/images', name, data)
            arr.attrs.timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')
            arr.flush()
        self._db.flush()
        self._index = self._index + 1 if self._index < self.N - 1 else 0

    def read(self, index):
        """Return data from the ring buffer file."""
        return np.array(self.hdf_file[str(index)])

    def save_as(self, filename):
        """Save the ring buffer to file filename. The output format
        will depend on the extension of filename.

        """
        self.logger.warning("Saving ring buffers to non-HDF5 formats is not yet properly implemented!")

        # Save as PNG files in a zip archive.
        if filename[-3:] == 'zip':
            for node in self._db.list_nodes('/images'):
                data = node.read()
                imsave('./img.png', data)

if __name__ == "__main__":
    from numpy import random

    size = 512
    img_size = (size, size)
    with RingBuffer(N=100) as rb:
        for i in range(200):
            img = random.random(img_size)
            rb.write(img)
        rb.save_as('test.zip')