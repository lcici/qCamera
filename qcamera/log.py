"""Logging setup for qCamera."""

import logging

logger = logging.getLogger('qCamera')

default_formatter = logging.Formatter()
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(default_formatter)
