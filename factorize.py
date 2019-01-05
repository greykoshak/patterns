import unittest

def factorize(x):
    """ Factorize positive integer and return its factors.
        :type x: int,>=0
        :rtype: tuple[N],N>0
    """
    pass

class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        self.cases = [1.5, "string"]
        for val in self.cases:
            with self.subTest(x=val):
                self.assertRaises(TypeError, factorize, val)

    def test_negative(self):
        self.cases = [-1, -10, -100]
        for val in self.cases:
            with self.subTest(x=val):
                self.assertRaises(ValueError, factorize, val)

    def test_zero_and_one_cases(self):
        self.cases = [0, 1]
        self.wait_results = [(0,), (1,)]
        for val, tuple_x in zip(self.cases, self.wait_results):
            with self.subTest(x=val):
                self.assertTupleEqual(factorize(val), tuple_x)

    def test_simple_numbers(self):
        self.cases = [3, 13, 29]
        self.wait_results = [(3,), (13,), (29,)]
        for val, tuple_x in zip(self.cases, self.wait_results):
            with self.subTest(x=val):
                self.assertTupleEqual(factorize(val), tuple_x)


    def test_two_simple_multipliers(self):
        self.cases = [6, 26, 121]
        self.wait_results = [(2, 3), (2, 13), (11, 11)]
        for val, tuple_x in zip(self.cases, self.wait_results):
            with self.subTest(x=val):
                self.assertTupleEqual(factorize(val), tuple_x)

    def test_many_multipliers(self):
        self.cases = [1001, 9699690]
        self.wait_results = [(7, 11, 13), (2, 3, 5, 7, 11, 13, 17, 19)]
        for val, tuple_x in zip(self.cases, self.wait_results):
            with self.subTest(x=val):
                self.assertTupleEqual(factorize(val), tuple_x)


if __name__ == "__main__":
    unittest.main()
