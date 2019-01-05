import unittest

def factorize(x):
    """ Factorize positive integer and return its factors.
        :type x: int,>=0
        :rtype: tuple[N],N>0
    """
    pass

class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        with self.subTest(x=1):
            self.assertRaises(TypeError, factorize, "string")
        with self.subTest(x=2):
            self.assertRaises(TypeError, factorize, 1.5)

    def test_negative(self):
        with self.subTest(x=1):
            self.assertRaises(ValueError, factorize, -1)
        with self.subTest(x=2):
            self.assertRaises(ValueError, factorize, -10)
        with self.subTest(x=3):
            self.assertRaises(ValueError, factorize, -100)

    def test_zero_and_one_cases(self):
        with self.subTest(x=1):
            self.assertTupleEqual(factorize(0), tuple([0]))
        with self.subTest(x=2):
            self.assertTupleEqual(factorize(1), tuple([1]))

    def test_simple_numbers(self):
        with self.subTest(x=1):
            self.assertTupleEqual(factorize(3), tuple([3]))
        with self.subTest(x=2):
            self.assertTupleEqual(factorize(13), tuple([13]))
        with self.subTest(x=3):
            self.assertTupleEqual(factorize(29), tuple([29]))

    def test_two_simple_multipliers(self):
        with self.subTest(x=1):
            self.assertTupleEqual(factorize(6), tuple([2, 3]))
        with self.subTest(x=2):
            self.assertTupleEqual(factorize(26), tuple([2, 13]))
        with self.subTest(x=3):
            self.assertTupleEqual(factorize(121), tuple([11, 11]))

    def test_many_multipliers(self):
        with self.subTest(x=1):
            self.assertTupleEqual(factorize(1001), tuple([7, 11, 13]))
        with self.subTest(x=2):
            self.assertTupleEqual(factorize(9699690), tuple([2, 3, 5, 7, 11, 13, 17, 19]))

if __name__ == "__main__":
    unittest.main()
