# -*- coding: utf-8 -*-

import unittest

from gorinich.base import TemplateRenderingMixin, BaseHandler
from gorinich.core import *
from gorinich.handlers import *
from gorinich.objects import *
from gorinich.run import *
from gorinich.utils import *

class TestInit(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(TemplateRenderingMixin(), TemplateRenderingMixin)
