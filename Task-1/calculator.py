"""
Simple Interactive Calculator
-----------------------------
A beginner-friendly Python script designed for clean terminal interaction,
robust error handling, and easy explanation in an internship submission.
"""

# ==========================================
# 1. Arithmetic Functions (Core Logic)
# ==========================================

def add(a: float, b: float) -> float:
    """Returns the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Returns the difference between two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Returns the product of two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """
    Returns the quotient of two numbers.
    Raises ZeroDivisionError if the divisor is 0.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


# ==========================================
# 2. Input Handling & Validation Helpers
# ==========================================

def get_number(prompt_message: str) -> float:
    """
    Prompts the user for a numeric input.
    Repeats until a valid integer or float is provided (handles non-numeric input).
    """
    while True:
        user_input = input(prompt_message).strip()
        try:
            # Attempt to convert input to a floating-point number
            return float(user_input)
        except ValueError:
            # Handles cases where input contains letters or invalid characters
            print("  [!] Invalid input: Please enter a valid number (e.g., 10, -3, 4.5).")


def get_operation() -> str:
    """
    Prompts the user to select an arithmetic operator or quit.
    Validates choice against allowed symbols and numbers.
    """
    valid_operations = {
        "+": "+", "1": "+",
        "-": "-", "2": "-",
        "*": "*", "3": "*",
        "/": "/", "4": "/",
        "q": "q", "quit": "q", "exit": "q"
    }

    while True:
        choice = input("\nSelect operation (+, -, *, /) or 'q' to quit: ").strip().lower()
        if choice in valid_operations:
            return valid_operations[choice]
        print("  [!] Invalid operation: Please choose (+, -, *, /) or 'q' to quit.")


# ==========================================
# 3. Main Calculator Loop
# ==========================================

def run_calculator():
    """
    Main controller for the calculator:
    - Displays a clean visual menu
    - Collects user inputs
    - Executes operations and displays formatted results
    - Continues until the user decides to exit
    """
    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }

    # Welcome banner
    print("=" * 45)
    print("         INTERACTIVE PYTHON CALCULATOR       ")
    print("=" * 45)
    print(" Options:")
    print("   [+] or [1] : Addition")
    print("   [-] or [2] : Subtraction")
    print("   [*] or [3] : Multiplication")
    print("   [/] or [4] : Division")
    print("   [q]        : Quit")
    print("-" * 45)

    # Main application loop
    while True:
        # Step 1: Get chosen operation
        op = get_operation()

        # Check for quit signal
        if op == "q":
            print("\nExiting calculator. Thank you!\n")
            break

        # Step 2: Get the two numbers from the user
        num1 = get_number("Enter the first number:  ")
        num2 = get_number("Enter the second number: ")

        # Step 3: Compute and display results with error safety
        try:
            calc_function = operations[op]
            result = calc_function(num1, num2)

            # Format numbers (:g removes unnecessary trailing zeros, e.g., 5.0 -> 5)
            print("\n" + "-" * 30)
            print(f" Result: {num1:g} {op} {num2:g} = {result:g}")
            print("-" * 30)

        except ZeroDivisionError as err:
            # Handles division by zero gracefully
            print(f"\n  [Math Error] {err}")
        except Exception as err:
            # Fallback for any other unexpected runtime issues
            print(f"\n  [Error] An unexpected error occurred: {err}")

        # Step 4: Ask if user wants to continue
        next_calc = input("\nDo you want to perform another calculation? (y/n): ").strip().lower()
        if next_calc in ("n", "no", "q", "quit"):
            print("\nExiting calculator. Thank you!\n")
            break


# Standard entry point: runs when executed directly from the terminal
if __name__ == "__main__":
    run_calculator()
