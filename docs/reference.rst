qCamera Reference
=================

Camera base class
-----------------

The :py:class:`qcamera.Camera` class is the base class of all derived
cameras. As such, it includes more possible functionality than a
specific camera may actually have, such as TEC cooling. Methods that
must be defined by the writer of an extension class are marked as
abstract methods to enforce that they are overwritten.

.. autoclass:: qcamera.Camera
   :members:
   :private-members:

Andor cameras
-------------

The :py:class:`qcamera.AndorCamera` class uses the unified Andor_
SDK. It was designed and tested with the iXon line of EMCCD cameras,
but should work with all other Andor cameras, possibly after some
tweaking.

.. _Andor: http://www.andor.com/

.. autoclass:: qcamera.AndorCamera
   :members:

PCO Sensicam
------------

A class for using PCO_ Sensicam CCD cameras.

.. _PCO: http://www.pco.de/

.. autoclass:: qcamera.Sensicam
   :members:

Thorlabs DCx-series cameras
---------------------------

Thorlabs_ sells a number of CCD and CMOS cameras under the DCx_ line
which can be used with this class.

.. _Thorlabs: http://www.thorlabs.com
.. _DCx: http://www.thorlabs.de/software_pages/ViewSoftwarePage.cfm?Code=DCx

.. autoclass:: qcamera.ThorlabsDCx
   :members:

OpenCV
------

This class utilizes the OpenCV_ library for interfacing with a wide
variety of cameras.

.. _OpenCV: http://opencv.org/

.. note:: The OpenCV interface only has rudimentary support so far.

.. autoclass:: OpenCVCamera
   :members:

