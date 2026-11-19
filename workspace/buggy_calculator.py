# buggy_calculator.py

"""
A simple calculator module with intentional bug in multiplication.
Provides functions: add, subtract, multiply, divide.
The main block demonstrates usage with sample inputs.
"""

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
def multiply(a, b):
    # Fixed bug: use multiplication instead of addition
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    x = 6
    y = 7
    print(f"{x} + {y} = {add(x, y)}")
    print(f"{x} - {y} = {subtract(x, y)}")
    print(f"{x} * {y} = {multiply(x, y)}")
    print(f"{x} / {y} = {divide(x, y)}")
