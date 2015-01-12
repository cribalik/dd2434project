__author__ = 'Daniel Schlaug'


class ConfusionMatrix:
    def __init__(self, true_positive, true_negative, false_positive, false_negative):
        self.__test_count = true_positive + true_negative + false_positive + false_negative
        self.__true_positive = float(true_positive) / self.test_count
        self.__true_negative = float(true_negative) / self.test_count
        self.__false_positive = float(false_positive) / self.test_count
        self.__false_negative = float(false_negative) / self.test_count

    @staticmethod
    def from_classifications(expected_classes, actual_classes):
        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0
        for (expected, actual) in zip(expected_classes, actual_classes):
            if expected:
                # true
                if actual:
                    true_positive += 1
                else:
                    true_negative += 1
            else:
                # false
                if actual:
                    false_positive += 1
                else:
                    false_negative += 1
        return ConfusionMatrix(true_positive, true_negative, false_positive, false_negative)

    @property
    def test_count(self):
        return self.__test_count

    @property
    def true_positive(self):
        return self.__true_positive

    @property
    def true_negative(self):
        return self.__true_negative

    @property
    def false_positive(self):
        return self.__false_positive

    @property
    def false_negative(self):
        return self.__false_negative

    @property
    def positive(self):
        return self.true_positive + self.false_positive

    @property
    def true(self):
        return self.true_positive + self.true_negative

    @property
    def precision(self):
        return self.true_positive / self.positive

    @property
    def recall(self):
        return self.true_positive / self.true

    @property
    def f1(self):
        return 2 * self.precision * self.recall / (self.precision + self.recall)