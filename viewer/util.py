"""Utility functions for use throughout the viewer application."""

import numpy as np
from guiqwt.image import ImageItem
from guiqwt.shapes import RectangleShape as Rectangle
from guiqwt.annotations import AnnotatedRectangle
from config import CAM_TYPES

def get_rect(rect_tool):
    """Convert the guiqwt RectangleTool shape format to what qCamera
    wants.

    For some ridiculous reason, the rect shape the get_rect
    function returns depends on which corner you drag from. In
    other words, it always returns [x1, y1, x2, y2] where [x1, y1]
    is the first corner you started from and [x2, y2] is the last
    corner.

    """
    rect = rect_tool.get_last_final_shape().get_rect()
    rect = [int(x) for x in rect]
    if rect[0] > rect[2]:
        rect[0], rect[2] = rect[2], rect[0]
    if rect[1] > rect[3]:
        rect[1], rect[3] = rect[3], rect[1]
    return rect

def get_image_item(imageWidget):
    """Return the guiqwt ImageItem of an ImageWidget."""
    items = imageWidget.get_plot().get_items()
    image = None
    for item in items:
        if isinstance(item, ImageItem):
            image = item
            break
    return image

def get_annotated_rect_item(imageWidget):
    """Return a guiqwt AnnotatedRectangle from an ImageWidget."""
    items = imageWidget.get_plot().get_items()
    rect = None
    for item in items:
        if isinstance(item, AnnotatedRectangle):
            rect = item
            break
    return rect

def get_rect_item(imageWidget):
    """Return a guiqwt Rectangle from an ImageWidget."""
    items = imageWidget.get_plot().get_items()
    rect = None
    for item in items:
        if isinstance(item, Rectangle):
            rect = item
            break
    return rect

def rotate_rect_cw(rect, center, rotations):
    """Rotate a rectangle 90 degrees clockwise rotations times about a
    central point.

    Parameters
    ----------
    rect : tuple
        Coordinates in the form [x1, y1, x2, y2]. The input is
        independent of which corners are being specified.
    center : tuple
        The pivot point in the form [x0, y0].
    rotations : int
        Number of clockwise 90 degree rotations to perform.

    Returns
    -------
    new_rect : tuple
        Coordinates in the form [x1p, y1p, x2p, y2p]. The output does
        not keep track of which corners should be specified, so it is
        up to the user to reorder if necessary.

    """
    new_rect = rect
    if rotations != 0:
        x0, y0 = center
        x = np.array([rect[0], rect[2]])
        y = np.array([rect[1], rect[3]])
        for i in range(rotations):
            xp = -(y - y0) + x0
            yp = (x - x0) + y0
            x = xp
            y = yp
        new_rect = [xp[0], yp[0], xp[1], yp[1]]
    return new_rect

def cam_options_string():
    """Returns a string to print the valid camera types."""
    out = ''
    for cam in CAM_TYPES:
        out = out + cam + ' '
    return out
    