Adding additional camera interfaces
===================================

In order to limit how much one has to remember to call the parent
constructors to do common tasks like setting internal class
attributes, several functions in the generic :class:`Camera` class are
not intended to be overwritten by child classes. Instead, secondary
functions are used which will be called following the execution of the
common tasks, and these secondary functions are those which should be
implemented by new interfaces. In order to make this process easier, a
template file is included as the module :py:mod:`qcamera.template`.

Following `PEP 8`_, functions that have a prepended underscore, such
as :py:meth:`Template._acquire_image_data` should not be called
externally. In this case, one should instead use the
:py:meth:`Camera.get_image` function.

.. _PEP 8: http://legacy.python.org/dev/peps/pep-0008/

template.py
-----------

This file can be found in ``/path/to/qcamera/template.py``.

.. literalinclude:: ../qcamera/template.py
   :linenos:
