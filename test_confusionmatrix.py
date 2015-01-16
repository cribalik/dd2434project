from unittest import TestCase

from confusionmatrix import *


__author__ = 'Daniel Schlaug'


class TestConfusionMatrix(TestCase):
    def test_from_classifications(self):
        expected = [True, True, False, False]
        actual = [True, False, True, False]
        cm = ConfusionMatrix.from_classifications(expected, actual)
        self.failUnlessEqual(cm.true_negative, 0.25)
        self.failUnlessEqual(cm.true_positive, 0.25)
        self.failUnlessEqual(cm.false_negative, 0.25)
        self.failUnlessEqual(cm.false_positive, 0.25)

    def test_precision(self):
        expected = [True, True, False, False]
        actual = [True, False, True, False]
        cm = ConfusionMatrix.from_classifications(expected, actual)
        self.failUnlessEqual(cm.precision, 0.5)

    def test_recall(self):
        expected = [True, True, False, False]
        actual = [True, False, True, False]
        cm = ConfusionMatrix.from_classifications(expected, actual)
        self.failUnlessEqual(cm.recall, 0.5)

    def test_f1(self):
        expected = [True, True, False, False]
        actual = [True, False, True, False]
        cm = ConfusionMatrix.from_classifications(expected, actual)
        self.failUnlessEqual(cm.f1, 0.5)