"""Utility functions for use throughout the viewer application."""

from guiqwt.image import ImageItem
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

def get_rect_item(imageWidget):
    """Return a guiqwt AnnotatedRectangle from an ImageWidget."""
    items = imageWidget.get_plot().get_items()
    rect = None
    for item in items:
        if isinstance(item, AnnotatedRectangle):
            rect = item
            break
    return rect

def cam_options_string():
    """Returns a string to print the valid camera types."""
    out = ''
    for cam in CAM_TYPES:
        out = out + cam + ' '
    return out
    