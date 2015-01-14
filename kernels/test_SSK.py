import re
from unittest import TestCase

from kernels.SSK import *


__author__ = 'Daniel Schlaug'


class TestSSK(TestCase):
    def test_SSK(self):
        self.failUnlessAlmostEqual(SSK(2, 0.5, "car", "cat"), 0.444444444, places=6)
