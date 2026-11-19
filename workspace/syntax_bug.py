def calculate(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    else:
        return None

# Simple user interaction replaced with predefined test values
if __name__ == "__main__":
    # Predefined test cases
    test_cases = [
        (5, 3, '+'),
        (10, 4, '-'),
        (6, 7, '*')
    ]
    for a, b, op in test_cases:
        result = calculate(a, b, op)
        if result is not None:
            print(f"{a} {op} {b} = {result}")
        else:
            print(f"Invalid operation: {op}")
