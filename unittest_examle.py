import unittest


# from fibonacci import fibo  # pip3 install fibonacci


class TestFibonacciNumbers(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(fibo(0), 0)

    def test_simple(self):
        for n, fib_n in (1, 1), (2, 1), (3, 2), (4, 3), (5, 5):
            with self.subTest(i=n):
                self.assertEqual(fibo(n), fib_n)

    def test_positive(self):
        self.assertEqual(fibo(10), 55)

    def test_negative(self):
        with self.subTest(i=1):
            self.assertRaises(ArithmeticError, fibo, -1)
        with self.subTest(i=2):
            self.assertRaises(ArithmeticError, fibo, -10)

    def test_fractional(self):
        self.assertRaises(ArithmeticError, fibo, 2.3)


def fibo(n: int) -> int:
    """
    Calculates fibonacci number by it's index
    """
    if not isinstance(n, int) or n < 0:
        raise ArithmeticError

    f = [0, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
        f[i] = f[i - 1] + f[i - 2]

    return f[n]


if __name__ == "__main__":
    unittest.main()
