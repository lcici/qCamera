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

Basic usage example
-------------------

