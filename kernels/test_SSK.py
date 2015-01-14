from unittest import TestCase

from numpy import linspace

from kernels.SSK import *

__author__ = 'Daniel Schlaug'

_dir = os.path.dirname(os.path.abspath(__file__))


class TestSSK(TestCase):
    def test_SSK(self):
        os.remove(os.path.join(_dir, "SSK.out"))
        self.failUnlessAlmostEqual(SSK(2, 0.5, "car", "cat"), 0.444444444, places=6)
        expected_result_for_length = [
            # As given in the paper
            (1, 0.849),
            (2, 0.580),
            (3, 0.478),
            (4, 0.439),
            (5, 0.406),
            (6, 0.370),
        ]

        str1 = "science is organized knowledge"
        str2 = "wisdom is organized life"


        for length, expected_result in expected_result_for_length:
            actual_result = SSK(length, 0.5, str1, str2)

            self.assertAlmostEqual(expected_result, actual_result, delta=0.001,
                                   msg="Failed for length %i. %f != %f" % (length, actual_result, expected_result))