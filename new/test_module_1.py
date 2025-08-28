
# my_example_module.py

# Global variable
PI = 3.14159

# Function definition with parameters and a return value
def calculate_circle_area(radius):
    """
    Calculates the area of a circle given its radius.
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    area = PI * (radius ** 2)
    return area

# Another function with a default argument
def greet_user(name="Guest"):
    """
    Prints a greeting message to the specified user.
    """
    print(f"Hello, {name}!")

# Class definition
class MyCalculator:
    """
    A simple calculator class.
    """
    def __init__(self, initial_value=0):
        self.value = initial_value

    def add(self, num):
        self.value += num
        return self.value

    def subtract(self, num):
        self.value -= num
        return self.value

# Main execution block (entry point)
if __name__ == "__main__":
    print("--- Running Example Module ---")

    # Using the global variable
    print(f"Value of PI: {PI}")

    # Calling functions
    radius_value = 5
    area_result = calculate_circle_area(radius_value)
    print(f"Area of a circle with radius {radius_value}: {area_result:.2f}")

    greet_user("Alice")
    greet_user() # Uses default argument

    # Using the class
    calculator = MyCalculator(10)
    print(f"Initial calculator value: {calculator.value}")
    calculator.add(7)
    print(f"Value after adding 7: {calculator.value}")
    calculator.subtract(3)
    print(f"Value after subtracting 3: {calculator.value}")

    print("--- Example Module Finished ---")