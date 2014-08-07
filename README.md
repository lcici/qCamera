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
  * Development is focused on the iXon line, so there could be some
    issues with other Andor cameras.
* [PCO](http://www.pco.de/) Sensicam
* [Thorlabs](http://www.thorlabs.de)
  [DCx-series](http://www.thorlabs.de/software_pages/ViewSoftwarePage.cfm?Code=DCx)
  CCD/CMOS cameras
* [OpenCV](http://opencv.org/) generic camera interface (partial support)

Requirements
------------

qCamera is mostly tested to work on Windows, but this depends on the
implementation of specific cameras. In the case of cameras with a
Linux SDK which shares function calls with its Windows counterpart,
this should be easy to implement if not already done so in the
existing code. Apart from having the shared libraries for the cameras
being used installed in the proper location for ctypes to find it, the
following Python packages are required:

* [Numpy](http://www.numpy.org/)
* [PyTables](http://www.pytables.org)

Optional requirements which if not met will result in limited
functionality:

* [Matplotlib](http://matplotlib.org/) for running tests
* [PyQt4](http://pyqt.sourceforge.net/Docs/PyQt4/) for using the
  viewer application.
* [GUIQwt](https://pythonhosted.org/guiqwt/) for image widgets in
  tests and the viewer application.

All of these are contained in the default installation of
[Python(x,y)](https://code.google.com/p/pythonxy/) for Windows.

Installation
------------

`python setup.py install`

Don't forget to rerun this whenever you want to import new changes!

Credits
-------

The camera that appears in the qCamera viewer icon is the
[Gnome-dev-camera][camicon] by David Vignoni and licensed under the
GNU Lesser General Public License via Wikimedia Commons. The original
can also be found [here][camicon_original].

[camicon]: https://commons.wikimedia.org/wiki/File:Gnome-dev-camera.svg#mediaviewer/File:Gnome-dev-camera.svg
[camicon_original]: http://ftp.gnome.org/pub/GNOME/sources/gnome-themes-extras/0.9/gnome-themes-extras-0.9.0.tar.gz

