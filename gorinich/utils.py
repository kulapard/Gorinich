# -*- coding: utf-8 -*-
__author__ = 'Taras Drapalyuk <taras@drapalyuk.com>'
__date__ = '26.05.2015'

import os
import time
import socket

from tornado.gen import coroutine, Task, Return
from tornado.ioloop import IOLoop

from gorinich import logger


try:
    # Trying to import fastest JSON decoder
    import ujson

    json_encode = ujson.dumps
    json_decode = ujson.loads
except ImportError:
    from tornado.escape import json_encode, json_decode


ROOT = os.path.normpath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(ROOT, 'static')
TEMPLATES_ROOT = os.path.join(ROOT, 'templates')


def path_to_static(filename):
    """
        Returns full path the static file.
    """
    return os.path.join(STATIC_ROOT, filename)


def path_to_template(filename):
    """
        Returns full path the template file.
    """
    return os.path.join(TEMPLATES_ROOT, filename)


@coroutine
def sleep(seconds):
    """
        Non-blocking sleep.
    """
    awake_at = time.time() + seconds
    yield Task(IOLoop.instance().add_timeout, awake_at)
    raise Return((True, None))


def get_server_address():
    """
        Returns servers IP address.
    """
    try:
        address = socket.gethostbyname(socket.gethostname())
    except Exception as err:
        logger.warning(err)
        address = "?"
    return address
