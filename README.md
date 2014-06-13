qCamera
=======

qCamera is a unified camera interface meant to be used in experimental
control systems such as qControl. It is designed to have commands for
cameras be as generic as possible to the user, that way swapping out
physical cameras should require little more than changing a line of
code to reflect the new hardware.

Supported cameras
-----------------

Not all SDK features of supported cameras are necessarily
implemented. Currently, cameras supported by qCamera include:

* [Andor](http://www.andor.com/) cameras
  * This includes all cameras supported by the Andor SDK
* [PCO](http://www.pco.de/) Sensicam

Coming soon:

* [Thorlabs](http://www.thorlabs.de)
  [DCx-series](http://www.thorlabs.de/software_pages/ViewSoftwarePage.cfm?Code=DCx)
  CCD/CMOS cameras

Possible for future inclusion�

* Generic web cam driver interface (avicap32.dll on Windows)

Requirements
------------

qCamera at the moment is limited to working on Windows only, though
this should not be difficult to allow functionality on Linux where
camera SDKs exist. Apart from having the shared libraries for the
cameras being used installed in the proper location, the following
Python packages are required:

* [Numpy](http://www.numpy.org/)
* [h5py](http://www.h5py.org/)

Optional requirements which if not met will result in limited
functionality:

* [Matplotlib](http://matplotlib.org/) for running tests
* [PyQt4](http://pyqt.sourceforge.net/Docs/PyQt4/) for embedding in
  GUI applications. This may be replaced with
  [PyQt5](http://pyqt.sourceforge.net/Docs/PyQt5/) in the future.
* [GUIQwt](https://pythonhosted.org/guiqwt/) for image widgets in
  tests.

All of these are contained in the default installation of
[Python(x,y)](https://code.google.com/p/pythonxy/) for Windows.

TODO
----

* Verify that all docstrings are up to date and accurately reflecting
  arguments, class attributes, etc.

Issues
------

* The ring buffer has problems if the image size changes. This needs
  to be addressed so that binning can be changed and images are still
  recorded to the buffer properly.
