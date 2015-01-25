qCamera
=======

qCamera is a unified camera interface meant to be used in experimental
control systems such as qControl, a system developed at Aarhus
University for running experiments with trapped ions. It is designed
to have commands for cameras be as generic as possible to the user,
that way swapping out physical cameras should require little more than
changing a line of code or two to reflect the new hardware.

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
* [OpenCV](http://opencv.org/) generic camera interface (partial
  support)
  
qCamera Viewer
--------------

This repository includes a sample PyQt-based application for testing
new camera interfaces in the `viewer` directory. 

```
usage: viewer.py [-h] [-c <camera type> | -s]

qCamera Viewer

optional arguments:
  -h, --help            show this help message and exit
  -c <camera type>, --camera-type <camera type>
                        Specify the camera type to use. If not given, default
                        to the last camera type used. Options include: opencv
                        sensicam andor thorlabs_dcx
  -s, --camera-select   Run the camera select dialog.
```

Requirements
------------

qCamera is mostly tested to work on Windows, but this depends on the
implementation of specific cameras. In the case of cameras with a
Linux SDK which shares function calls with its Windows counterpart,
this should be easy to implement if not already done so in the
existing code. Apart from having the shared libraries for the cameras
being used installed in the proper location for ctypes to find it, the
following Python packages are required:

* [NumPy](http://www.numpy.org/)
* [SciPy](http://www.scipy.org/)
* [PyTables](http://www.pytables.org)

Optional requirements which if not met will result in some slightly
limited functionality:

* [Matplotlib](http://matplotlib.org/) for running tests
* [PyQt4](http://pyqt.sourceforge.net/Docs/PyQt4/) for using the
  viewer application.
* [GUIQwt](https://pythonhosted.org/guiqwt/) for image widgets in
  tests and the viewer application.

All of these are contained in the default installation of
[Python(x,y)](https://code.google.com/p/pythonxy/) for Windows. Please
note that all of the above are required to run the qCamera Viewer
application.

Bugs
----

There is an issue with compression introduced in commit `c1a5edf`. It
is not yet confirmed, but this may be due to using version 3.0.0 of
PyTables, which ships with Python(x,y), versus the more recent 3.1.x
branch. The change will be reverted for the time being until a
solution can be worked out.

Installation
------------

`python setup.py install`

Credits
-------

The camera that appears in the qCamera viewer icon is the
[Gnome-dev-camera][camicon] by David Vignoni and licensed under the
GNU Lesser General Public License via Wikimedia Commons. The original
can also be found [here][camicon_original].

[camicon]: https://commons.wikimedia.org/wiki/File:Gnome-dev-camera.svg#mediaviewer/File:Gnome-dev-camera.svg
[camicon_original]: http://ftp.gnome.org/pub/GNOME/sources/gnome-themes-extras/0.9/gnome-themes-extras-0.9.0.tar.gz

