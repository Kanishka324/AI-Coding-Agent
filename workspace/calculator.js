// Simple calculator implementation

function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  if (b === 0) {
    return "Error: Division by zero";
  }
  return a / b;
}

// Sample usage and output
console.log('Addition (5 + 3):', add(5, 3));
console.log('Subtraction (5 - 3):', subtract(5, 3));
console.log('Multiplication (5 * 3):', multiply(5, 3));
console.log('Division (5 / 2):', divide(5, 2));
console.log('Division by zero (5 / 0):', divide(5, 0));
