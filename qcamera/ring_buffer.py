"""Ring buffer for automatic storage of images"""

from __future__ import print_function
import time
import numpy as np
import h5py

class RingBuffer(object):
    """Ring buffer class.

    Attributes
    ----------
    directory : str
    recording : bool
    N : int
    index : int

    """
    
    def __init__(self, N=100, directory=".", recording=True):
        """Initialize the ring buffer.

        Parameters
        ----------
        N : int, optional
            Number of images to store in the ring buffer.
        directory : str, optional
            The directory to buffer images to.
        recording : bool, optional
            Activate recording when True, disable when False.

        """
        self.hdf_file = h5py.File(directory + '/ring_buffer.h5', 'w')
        self.recording = recording
        self.N = N
        self.index = 0

    def __enter__(self):
        return self

    def __exit__(self, type_, value, tb):
        self.close()

    def close(self):
        self.hdf_file.close()

    def write(self, data):
        """Write data to the ring buffer file."""
        if not self.recording:
            return
        idx = str(self.index)
        if idx not in self.hdf_file.keys():
            self.hdf_file.create_dataset(idx, data=data, maxshape=(2048, 2048))
        else:
            self.hdf_file[idx].write_direct(np.array(data))
        self.hdf_file[idx].attrs['timestamp'] = time.ctime()
        self.index = self.index + 1 if self.index < self.N - 1 else 0
        self.hdf_file.flush()

    def read(self, index):
        """Return data from the ring buffer file."""
        return np.array(self.hdf_file[str(index)])

if __name__ == "__main__":
    from numpy import random

    size = 512
    img_size = (size, size)
    with RingBuffer(N=100) as rb:
        for i in range(100):
            img = random.random(img_size)
            rb.write(img)
            