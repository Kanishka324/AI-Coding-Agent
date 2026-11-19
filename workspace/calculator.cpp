#include <iostream>
#include <stdexcept>

// Function prototypes
double add(double a, double b) { return a + b; }
double subtract(double a, double b) { return a - b; }
double multiply(double a, double b) { return a * b; }

double divide(double a, double b) {
    if (b == 0) {
        throw std::runtime_error("Division by zero error");
    }
    return a / b;
}

int main() {
    // Sample calculations
    double a = 10.0, b = 5.0;
    std::cout << "Addition: " << a << " + " << b << " = " << add(a,b) << std::endl;
    std::cout << "Subtraction: " << a << " - " << b << " = " << subtract(a,b) << std::endl;
    std::cout << "Multiplication: " << a << " * " << b << " = " << multiply(a,b) << std::endl;
    try {
        std::cout << "Division: " << a << " / " << b << " = " << divide(a,b) << std::endl;
        std::cout << "Division by zero test: " << divide(a, 0) << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Caught exception: " << e.what() << std::endl;
    }
    return 0;
}
