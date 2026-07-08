import streamlit as st
import numpy as np
from scipy import optimize
from scipy.interpolate import CubicSpline
import sympy as sp

# --- HELPER FUNCTIONS ---
def sign(val):
    if val > 0: return 1
    elif val < 0: return -1
    else: return 0

# --- COMPUTATION MODULES ---

def bisection_ui():
    st.header("Bisection Method")
    
    eq_str = st.text_input("Enter the single variable equation in terms of 'x'", value="x**2 - 4")
    
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Lower bound (a)", value=0.0)
        tol = st.number_input("Tolerance", value=0.0001, format="%.5f")
    with col2:
        b = st.number_input("Upper bound (b)", value=5.0)
        max_iter = st.number_input("Maximum iterations", value=50, step=1)
        
    if st.button("Calculate Bisection Root"):
        try:
            x = sp.Symbol('x')
            f_expr = sp.sympify(eq_str)
            f = sp.lambdify(x, f_expr, 'math') 
            
            if f(a) * f(b) > 0:
                st.error("The function must have opposite signs at the bounds 'a' and 'b'. Please try again with different bounds.")
                return

            k = 1
            x_hat = a 
            
            with st.spinner("Calculating..."):
                while k <= max_iter:
                    x_hat = (a + b) / 2.0
                    
                    if abs(b - a) / 2.0 < tol:
                        st.success(f"Root estimated at **x = {x_hat:.6f}** after {k} iterations (tolerance met).")
                        return

                    if sign(f(x_hat)) == sign(f(a)):
                        a = x_hat
                    elif sign(f(x_hat)) == sign(f(b)):
                        b = x_hat
                    elif sign(f(x_hat)) == 0:
                        st.success(f"Exact root found at **x = {x_hat}** after {k} iterations.")
                        return 
                    else:
                        st.error("Unexpected error during sign evaluation. Terminating.")
                        return 
                        
                    k += 1
                    
                st.warning(f"Maximum iterations ({max_iter}) reached. Best estimate of root: **{x_hat:.6f}**")
                
        except Exception as e:
            st.error(f"Invalid input or mathematical error: {e}")
            st.info("Ensure you format your equation properly (e.g., use '2*x' instead of '2x').")


def linear_interpolation_ui():
    st.header("Linear Interpolation")
    
    eq_str = st.text_input("Enter the single variable equation in terms of 'x'", value="x**2 - 4", key="lin_eq")
    
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Lower bound (a)", value=0.0, key="lin_a")
        tol = st.number_input("Tolerance", value=0.0001, format="%.5f", key="lin_tol")
    with col2:
        b = st.number_input("Upper bound (b)", value=5.0, key="lin_b")
        max_iter = st.number_input("Maximum iterations", value=50, step=1, key="lin_max")
        
    if st.button("Calculate Interpolation Root"):
        try:
            x = sp.Symbol('x')
            f_expr = sp.sympify(eq_str)
            f = sp.lambdify(x, f_expr, 'math') 
            
            if f(a) * f(b) > 0:
                st.error("The function must have opposite signs at the bounds 'a' and 'b'.")
                return

            k = 1
            x_hat = a
            
            with st.spinner("Calculating..."):
                while k <= max_iter:
                    f_a = f(a)
                    f_b = f(b)
                    
                    if f_a - f_b == 0:
                        st.error("Division by zero detected (f(a) - f(b) == 0). Terminating.")
                        return

                    x_hat = a - f_a * (a - b) / (f_a - f_b)
                    
                    if abs(f(x_hat)) < tol:
                        st.success(f"Root estimated at **x = {x_hat:.6f}** after {k} iterations (tolerance met).")
                        return

                    if sign(f(x_hat)) == 0:
                        st.success(f"Exact root found at **x = {x_hat}** after {k} iterations.")
                        return 
                    elif sign(f(x_hat)) == sign(f(a)):
                        a = x_hat
                    elif sign(f(x_hat)) == sign(f(b)):
                        b = x_hat
                    else:
                        st.error("Unexpected error during sign evaluation. Terminating.")
                        return 
                        
                    k += 1
                    
                st.warning(f"Maximum iterations ({max_iter}) reached. Best estimate of root: **{x_hat:.6f}**")
                
        except Exception as e:
            st.error(f"Invalid input or mathematical error: {e}")
            st.info("Ensure you format your equation properly (e.g., use '2*x' instead of '2x').")

# --- MAIN APP ROUTING ---

st.set_page_config(page_title="Program Calculator", layout="centered")

st.sidebar.title("🧮 Program Calculator")
category = st.sidebar.selectbox(
    "Select a Category", 
    ["Single Variable Equation", "System of Linear Equations", "Approximation"]
)

if category == "Single Variable Equation":
    method = st.sidebar.radio(
        "Select a Subfunction", 
        ["Bisection", "Linear Interpolation", "The Method of Secants", "Newton's Method"]
    )
    
    if method == "Bisection":
        bisection_ui()
    elif method == "Linear Interpolation":
        linear_interpolation_ui()
    elif method == "The Method of Secants":
        st.header("The Method of Secants")
        st.info("Computation code goes here...")
    elif method == "Newton's Method":
        st.header("Newton's Method")
        st.info("Computation code goes here...")

elif category == "System of Linear Equations":
    method = st.sidebar.radio(
        "Select a Subfunction", 
        ["Addition", "Subtraction", "Multiplication", "Division"]
    )
    
    st.header(f"Matrix {method}")
    st.info("Computation code goes here...")

elif category == "Approximation":
    method = st.sidebar.radio(
        "Select a Subfunction", 
        ["Least Squares", "Cubic Splines", "Principal Component Analysis"]
    )
    
    st.header(method)
    st.info("Computation code goes here...")
