import streamlit as st
import sympy as sp

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Program Calculator", layout="centered")
st.title("🧮 Numerical Methods Calculator")

# --- SIDEBAR MENU ---
st.sidebar.header("Main Menu")
category = st.sidebar.selectbox("Select Category", ["Single Variable Equation", "Matrix", "Approximation"])

if category == "Single Variable Equation":
    method = st.sidebar.radio("Select Method", ["Bisection", "Linear Interpolation", "Method of Secants", "Newton's Method"])
    
    if method == "Bisection":
        st.header("Bisection Method")
        st.write("Find the root of a continuous function within a specified interval.")
        
        # UI Inputs replacing the old input() functions
        eq_str = st.text_input("Enter equation in terms of 'x'", value="x**2 - 4")
        
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("Lower bound (a)", value=0.0)
            tol = st.number_input("Tolerance", value=0.0001, format="%.5f")
        with col2:
            b = st.number_input("Upper bound (b)", value=5.0)
            max_iter = st.number_input("Max iterations", value=50, step=1)
            
        # Calculate Button
        if st.button("Calculate Root"):
            try:
                x = sp.Symbol('x')
                f_expr = sp.sympify(eq_str)
                f = sp.lambdify(x, f_expr, 'math')
                
                if f(a) * f(b) > 0:
                    st.error("The function must have opposite signs at the bounds 'a' and 'b'.")
                else:
                    # Bisection Logic
                    k = 1
                    x_hat = a
                    success = False
                    
                    with st.spinner('Calculating...'):
                        while k <= max_iter:
                            x_hat = (a + b) / 2.0
                            if abs(b - a) / 2.0 < tol:
                                st.success(f"Root estimated at **x = {x_hat:.6f}** after {k} iterations (tolerance met).")
                                success = True
                                break
                            
                            f_x_hat = f(x_hat)
                            if f_x_hat == 0:
                                st.success(f"Exact root found at **x = {x_hat}** after {k} iterations.")
                                success = True
                                break
                            elif (f_x_hat > 0 and f(a) > 0) or (f_x_hat < 0 and f(a) < 0):
                                a = x_hat
                            else:
                                b = x_hat
                            k += 1
                            
                        if not success:
                            st.warning(f"Maximum iterations reached. Best estimate: **{x_hat:.6f}**")
            except Exception as e:
                st.error(f"Invalid input or mathematical error: {e}")

elif category == "Matrix":
    st.header("Matrix Operations")
    st.info("Matrix interface coming soon...")
    # You can use st.data_editor() later to let users input matrix grids!

elif category == "Approximation":
    st.header("Data Approximation")
    st.info("Approximation interface coming soon...")
