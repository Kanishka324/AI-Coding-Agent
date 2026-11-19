"""Unit tests for the calculator module."""

import unittest
from calculator import add, subtract, multiply, divide, Calculator


class TestFunctionalCalculator(unittest.TestCase):
    """Tests for standalone arithmetic functions."""

    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(-5, -5), -10)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3, places=7)

    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(subtract(4, 10), -6)
        self.assertEqual(subtract(-5, -3), -2)
        self.assertAlmostEqual(subtract(5.5, 2.3), 3.2, places=7)

    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-3, 4), -12)
        self.assertEqual(multiply(-3, -4), 12)
        self.assertEqual(multiply(10, 0), 0)
        self.assertAlmostEqual(multiply(2.5, 4.0), 10.0, places=7)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5.0)
        self.assertEqual(divide(9, 2), 4.5)
        self.assertEqual(divide(-10, 2), -5.0)
        self.assertEqual(divide(-10, -2), 5.0)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError) as context:
            divide(10, 0)
        self.assertIn("Cannot divide by zero", str(context.exception))


class TestStatefulCalculator(unittest.TestCase):
    """Tests for Calculator class."""

    def setUp(self):
        self.calc = Calculator(10)

    def test_initial_value(self):
        c = Calculator()
        self.assertEqual(c.value, 0)
        self.assertEqual(self.calc.value, 10)

    def test_chained_operations(self):
        self.calc.add(5)          # 15
        self.calc.subtract(3)     # 12
        self.calc.multiply(2)     # 24
        self.calc.divide(4)       # 6.0
        self.assertEqual(self.calc.value, 6.0)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(0)

    def test_reset(self):
        self.calc.add(100)
        self.calc.reset(0)
        self.assertEqual(self.calc.value, 0)


if __name__ == "__main__":
    unittest.main()
