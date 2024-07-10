import math
import os

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x / y

def exponentiate(x, y):
    return x ** y

def modulus(x, y):
    return x % y

def sqrt(x):
    if x < 0:
        return "Error! Cannot take the square root of a negative number."
    return math.sqrt(x)

def log(x):
    if x <= 0:
        return "Error! Logarithm undefined for non-positive values."
    return math.log(x)

def exp(x):
    return math.exp(x)

def factorial(x):
    if x < 0:
        return "Error! Factorial undefined for negative values."
    return math.factorial(int(x))

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

def sinh(x):
    return math.sinh(x)

def cosh(x):
    return math.cosh(x)

def tanh(x):
    return math.tanh(x)

def asin(x):
    if x < -1 or x > 1:
        return "Error! asin undefined for values outside the range [-1, 1]."
    return math.degrees(math.asin(x))

def acos(x):
    if x < -1 or x > 1:
        return "Error! acos undefined for values outside the range [-1, 1]."
    return math.degrees(math.acos(x))

def atan(x):
    return math.degrees(math.atan(x))

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def load_history(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.readlines()
    return []

def save_history(filename, history):
    with open(filename, 'w') as file:
        file.writelines(history)

def main():
    operations = {
        "1": ("Add", add),
        "2": ("Subtract", subtract),
        "3": ("Multiply", multiply),
        "4": ("Divide", divide),
        "5": ("Exponentiate", exponentiate),
        "6": ("Modulus", modulus),
        "7": ("Square Root", sqrt),
        "8": ("Logarithm", log),
        "9": ("Sine", sin),
        "10": ("Cosine", cos),
        "11": ("Tangent", tan),
        "12": ("Hyperbolic Sine", sinh),
        "13": ("Hyperbolic Cosine", cosh),
        "14": ("Hyperbolic Tangent", tanh),
        "15": ("Arc Sine", asin),
        "16": ("Arc Cosine", acos),
        "17": ("Arc Tangent", atan),
        "18": ("Exponential", exp),
        "19": ("Factorial", factorial)
    }
    
    history_file = "history.txt"
    history = load_history(history_file)
    memory = 0

    while True:
        print("\nSelect operation:")
        for key, (name, _) in operations.items():
            print(f"{key}. {name}")
        print("20. Recall Memory")
        print("21. Store Result in Memory")
        print("22. View History")
        print("23. Clear History")
        
        choice = input("Select an option (1-23): ")

        if choice in operations:
            if choice in ('7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'):  # Operations that require only one number
                num1 = get_number("Enter number: ")
                operation_name, operation_func = operations[choice]
                result = operation_func(num1)
            else:
                num1 = get_number("Enter first number: ")
                num2 = get_number("Enter second number: ")
                operation_name, operation_func = operations[choice]
                result = operation_func(num1, num2)
            
            print(f"Result: {result}")
            entry = f"{operation_name}({num1}, {num2}) = {result}\n" if choice not in ('7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19') else f"{operation_name}({num1}) = {result}\n"
            history.append(entry)
            save_history(history_file, history)

        elif choice == "20":
            print(f"Memory: {memory}")

        elif choice == "21":
            memory = result
            print(f"Stored {result} in memory.")

        elif choice == "22":
            print("\nCalculation History:")
            for record in history:
                print(record.strip())

        elif choice == "23":
            history.clear()
            save_history(history_file, history)
            print("History cleared.")

        else:
            print("Invalid choice. Please select a valid operation.")

        next_calculation = input("Let's do another calculation? (yes/no): ").strip().lower()
        if next_calculation == "no":
            print("Thank you for using the calculator!")
            break

if __name__ == "__main__":
    main()
