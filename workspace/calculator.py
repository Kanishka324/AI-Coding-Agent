"""A simple calculator module providing basic arithmetic operations."""

from typing import Union

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """Return the sum of a and b."""
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """Return the difference of a and b (a - b)."""
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """Return the product of a and b."""
    return a * b


def divide(a: Number, b: Number) -> float:
    """Return the quotient of a divided by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


class Calculator:
    """Stateful or object-oriented interface for the calculator."""

    def __init__(self, initial_value: Number = 0):
        self.value: Number = initial_value

    def add(self, amount: Number) -> Number:
        self.value = add(self.value, amount)
        return self.value

    def subtract(self, amount: Number) -> Number:
        self.value = subtract(self.value, amount)
        return self.value

    def multiply(self, amount: Number) -> Number:
        self.value = multiply(self.value, amount)
        return self.value

    def divide(self, amount: Number) -> float:
        self.value = divide(self.value, amount)
        return self.value

    def reset(self, value: Number = 0) -> Number:
        self.value = value
        return self.value


def main():
    """Simple demonstration of calculator capabilities."""
    print("=== Calculator Demo ===")
    print(f"10 + 5 = {add(10, 5)}")
    print(f"10 - 5 = {subtract(10, 5)}")
    print(f"10 * 5 = {multiply(10, 5)}")
    print(f"10 / 5 = {divide(10, 5)}")

    calc = Calculator(100)
    print("\n=== Stateful Calculator Demo ===")
    print(f"Initial: {calc.value}")
    print(f"Add 50: {calc.add(50)}")
    print(f"Subtract 25: {calc.subtract(25)}")
    print(f"Multiply 2: {calc.multiply(2)}")
    print(f"Divide 5: {calc.divide(5)}")


if __name__ == "__main__":
    main()
