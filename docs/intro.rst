Introduction to qCamera
=======================

Motivation
----------

For the purposes of automating data processing, it is often beneficial
to use an SDK provided by a camera's manufacturer rather than their
graphical interface. This can sometimes make it challenging to write
good control software which is flexible enough to accommodate cameras
from different sources. The qCamera framework was designed with this
problem in mind, using an abstract base camera class which includes
calls to both basic and specific functionality that can be implemented
as needed for each individual camera.

Requirements
------------

In addition to having the appropriate shared libraries to interface
with a given camera, the following Python libraries are required:

 * NumPy_
 * PyTables_

.. _NumPy: http://www.numpy.org/
.. _PyTables: http://www.pytables.org/

Some tests also utilize Matplotlib_. Additionally, the following
modules are required for using the qCamera Viewer utility:

 * PyQt4_
 * GUIQwt_

.. _Matplotlib: http://matplotlib.org/
.. _PyQt4: http://pyqt.sourceforge.net/Docs/PyQt4/
.. _GUIQwt: https://pythonhosted.org/guiqwt/

Basic usage example
-------------------

TODO
