import numpy as np
from scipy import optimize
from scipy.interpolate import CubicSpline
import sys
import sympy as sp

def bisection():
    print("\n[Executing Bisection...]")
    
    # 1. Ask the user for the equation and parameters
    eq_str = input("Enter the single variable equation in terms of 'x' (e.g., x**2 - 4): ")
    
    try:
        # Parse the string into a mathematical function using sympy
        x = sp.Symbol('x')
        f_expr = sp.sympify(eq_str)
        f = sp.lambdify(x, f_expr, 'math') 
        
        # Get boundaries and termination criteria
        a = float(input("Enter the lower bound (a): "))
        b = float(input("Enter the upper bound (b): "))
        tol = float(input("Enter the tolerance (e.g., 0.0001): "))
        max_iter = int(input("Enter the maximum number of iterations: "))
        
        # Check if a root exists between 'a' and 'b'
        if f(a) * f(b) > 0:
            print("\n[Error] The function must have opposite signs at the bounds 'a' and 'b'.")
            print("Please try again with different bounds.")
            return

        # Helper function to mirror the exact 'sign()' logic from the pseudocode
        def sign(val):
            if val > 0: return 1
            elif val < 0: return -1
            else: return 0

        # 2. Pseudocode Implementation
        k = 1
        x_hat = a # Initialize variable
        
        # "while unmet termination criteria do"
        while k <= max_iter:
            # x_hat = (a + b)/2
            x_hat = (a + b) / 2.0
            
            # Additional termination criteria: checking if we are within the tolerance
            if abs(b - a) / 2.0 < tol:
                print(f"\n[Success] Root estimated at x = {x_hat:.6f} after {k} iterations (tolerance met).")
                return

            # "if sign(f(x_hat)) == sign(f(a)) then"
            if sign(f(x_hat)) == sign(f(a)):
                a = x_hat
            # "else if sign(f(x_hat)) == sign(f(b)) then"
            elif sign(f(x_hat)) == sign(f(b)):
                b = x_hat
            # "else if sign(f(x_hat)) == 0 then"
            elif sign(f(x_hat)) == 0:
                print(f"\n[Success] Exact root found at x = {x_hat} after {k} iterations.")
                return # "set termination status to true"
            # "else"
            else:
                print("\n[Failure] Unexpected error during sign evaluation. Terminating.")
                return # "set status to failure and terminate"
                
            # "k = k + 1"
            k += 1
            
        # "return best estimate of root"
        print(f"\n[Warning] Maximum iterations ({max_iter}) reached.")
        print(f"Best estimate of root: {x_hat:.6f}")
        
    except Exception as e:
        print(f"\n[Error] Invalid input or mathematical error: {e}")
        print("Ensure you format your equation properly (e.g., use '2*x' instead of '2x').")


def linear_interpolation():
    print("\n[Executing Linear Interpolation...]")
    
    eq_str = input("Enter the single variable equation in terms of 'x' (e.g., x**2 - 4): ")
    
    try:
        x = sp.Symbol('x')
        f_expr = sp.sympify(eq_str)
        f = sp.lambdify(x, f_expr, 'math') 
        
        a = float(input("Enter the lower bound (a): "))
        b = float(input("Enter the upper bound (b): "))
        tol = float(input("Enter the tolerance (e.g., 0.0001): "))
        max_iter = int(input("Enter the maximum number of iterations: "))
        
        if f(a) * f(b) > 0:
            print("\n[Error] The function must have opposite signs at the bounds 'a' and 'b'.")
            return

        def sign(val):
            if val > 0: return 1
            elif val < 0: return -1
            else: return 0

        # Based on Algorithm 2 Pseudocode
        k = 1
        x_hat = a
        
        while k <= max_iter:
            f_a = f(a)
            f_b = f(b)
            
            # Prevent division by zero
            if f_a - f_b == 0:
                print("\n[Failure] Division by zero detected (f(a) - f(b) == 0). Terminating.")
                return

            # x_hat = a - f(a)(a - b)/(f(a) - f(b)) 
            x_hat = a - f_a * (a - b) / (f_a - f_b)
            
            # Additional termination check for tolerance
            if abs(f(x_hat)) < tol:
                print(f"\n[Success] Root estimated at x = {x_hat:.6f} after {k} iterations (tolerance met).")
                return

            # if sign(f(x_hat)) == 0 then 
            if sign(f(x_hat)) == 0:
                print(f"\n[Success] Exact root found at x = {x_hat} after {k} iterations.")
                return 
            # else if sign(f(x_hat)) == sign(f(a)) then 
            elif sign(f(x_hat)) == sign(f(a)):
                a = x_hat
            # else if sign(f(x_hat)) == sign(f(b)) then 
            elif sign(f(x_hat)) == sign(f(b)):
                b = x_hat
            else:
                print("\n[Failure] Unexpected error during sign evaluation. Terminating. ")
                return 
                
            k += 1
            
        print(f"\n[Warning] Maximum iterations ({max_iter}) reached.")
        print(f"Best estimate of root: {x_hat:.6f} ")
        
    except Exception as e:
        print(f"\n[Error] Invalid input or mathematical error: {e}")
        print("Ensure you format your equation properly (e.g., use '2*x' instead of '2x').")

def method_of_secants():
    print("\n[Executing Method of Secants...]")
    # Computation code goes here

def newtons_method():
    print("\n[Executing Newton's Method...]")
    # Computation code goes here

def matrix_addition():
    print("\n[Executing Matrix Addition...]")
    # Computation code goes here

def matrix_subtraction():
    print("\n[Executing Matrix Subtraction...]")
    # Computation code goes here

def matrix_multiplication():
    print("\n[Executing Matrix Multiplication...]")
    # Computation code goes here

def matrix_division():
    print("\n[Executing Matrix Division...]")
    # Computation code goes here

def least_squares():
    print("\n[Executing Least Squares...]")
    # Computation code goes here

def cubic_splines():
    print("\n[Executing Cubic Splines...]")
    # Computation code goes here

def principal_component_analysis():
    print("\n[Executing Principal Component Analysis...]")
    # Computation code goes here

# --- SUB-MENUS ---

def single_variable_menu():
    while True:
        print("\n=== Single Variable Equation ===")
        print("1. Bisection")
        print("2. Linear Interpolation")
        print("3. The Method of Secants")
        print("4. Newton's Method")
        print("5. Back to Main Menu")

        choice = input("Select a subfunction (1-5): ")

        if choice == '1':
            bisection()
        elif choice == '2':
            linear_interpolation()
        elif choice == '3':
            method_of_secants()
        elif choice == '4':
            newtons_method()
        elif choice == '5':
            break
        else:
            print("Invalid input. Please select a valid option.")

def matrix_menu():
    while True:
        print("\n=== System of Linear Equations ===")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Back to Main Menu")

        choice = input("Select a subfunction (1-5): ")

        if choice == '1':
            matrix_addition()
        elif choice == '2':
            matrix_subtraction()
        elif choice == '3':
            matrix_multiplication()
        elif choice == '4':
            matrix_division()
        elif choice == '5':
            break
        else:
            print("Invalid input. Please select a valid option.")

def approximation_menu():
    while True:
        print("\n=== Approximation ===")
        print("1. Least Squares")
        print("2. Cubic Splines")
        print("3. Principal Component Analysis")
        print("4. Back to Main Menu")

        choice = input("Select a subfunction (1-4): ")

        if choice == '1':
            least_squares()
        elif choice == '2':
            cubic_splines()
        elif choice == '3':
            principal_component_analysis()
        elif choice == '4':
            break
        else:
            print("Invalid input. Please select a valid option.")

# --- MAIN MENU ---

def main_menu():
    while True:
        print("\n==============================")
        print("      PROGRAM CALCULATOR      ")
        print("==============================")
        print("1. Single Variable Equation")
        print("2. System of Linear Equations")
        print("3. Approximation")
        print("4. Exit")

        choice = input("Select a function (1-4): ")

        if choice == '1':
            single_variable_menu()
        elif choice == '2':
            matrix_menu()
        elif choice == '3':
            approximation_menu()
        elif choice == '4':
            print("\nExiting the calculator. Goodbye!")
            sys.exit()
        else:
            print("Invalid input. Please select a valid option.")

if __name__ == "__main__":
    main_menu()
