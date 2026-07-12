import streamlit as st
import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Computational Science Toolkit", page_icon="🧮", layout="wide")

# --- HELPER FUNCTIONS ---
def sign(val):
    if val > 0: return 1
    elif val < 0: return -1
    else: return 0

def format_res(val):
    """Formats values: integers drop decimal places, floats are rounded to 4 decimals."""
    if float(val).is_integer():
        return f"{int(val)}"
    return f"{float(val):.4f}"

# --- 1. SINGLE VARIABLE EQUATIONS ---

def bisection_ui():
    st.header("Bisection Method")
    st.markdown("Find the root of a function by repeatedly bisecting an interval.")
    st.divider()
    
    with st.form("bisection_form"):
        eq_str = st.text_input("Enter equation in terms of 'x'", value="x**2 - 4")
        
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("Lower bound (a)", value=0.0)
            tol = st.number_input("Tolerance", value=0.0001, format="%.5f")
        with col2:
            b = st.number_input("Upper bound (b)", value=5.0)
            max_iter = st.number_input("Max iterations", value=50, step=1)
            
        submitted = st.form_submit_button("Calculate Root", type="primary")
        
    if submitted:
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
                    x_hat = (a + b) / 2.0
                    if abs(b - a) / 2.0 < tol:
                        st.success(f"Tolerance met after {k} iterations.")
                        st.metric(label="Estimated Root (x)", value=format_res(x_hat))
                        return
                    if sign(f(x_hat)) == sign(f(a)):
                        a = x_hat
                    elif sign(f(x_hat)) == sign(f(b)):
                        b = x_hat
                    elif sign(f(x_hat)) == 0:
                        st.success(f"Exact root found after {k} iterations.")
                        st.metric(label="Exact Root (x)", value=format_res(x_hat))
                        return
                    else:
                        st.error("Unexpected error during sign evaluation.")
                        return
                    k += 1
                st.warning("Maximum iterations reached.")
                st.metric(label="Best Estimate (x)", value=format_res(x_hat))
        except Exception as e:
            st.error(f"Invalid input or mathematical error: {e}")

def linear_interpolation_ui():
    st.header("Linear Interpolation")
    st.markdown("Estimate the root of a function using linear segments.")
    st.divider()

    with st.form("linear_interp_form"):
        eq_str = st.text_input("Enter equation in terms of 'x'", value="x**2 - 4")
        
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("Lower bound (a)", value=0.0)
            tol = st.number_input("Tolerance", value=0.0001, format="%.5f")
        with col2:
            b = st.number_input("Upper bound (b)", value=5.0)
            max_iter = st.number_input("Max iterations", value=50, step=1)
            
        submitted = st.form_submit_button("Calculate Root", type="primary")
        
    if submitted:
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
                        st.error("Division by zero detected. Terminating.")
                        return
                        
                    x_hat = a - f_a * (a - b) / (f_a - f_b)
                    
                    if abs(f(x_hat)) < tol:
                        st.success(f"Tolerance met after {k} iterations.")
                        st.metric(label="Estimated Root (x)", value=format_res(x_hat))
                        return
                    if sign(f(x_hat)) == 0:
                        st.success(f"Exact root found after {k} iterations.")
                        st.metric(label="Exact Root (x)", value=format_res(x_hat))
                        return
                    elif sign(f(x_hat)) == sign(f(a)):
                        a = x_hat
                    elif sign(f(x_hat)) == sign(f(b)):
                        b = x_hat
                    else:
                        st.error("Unexpected error during sign evaluation.")
                        return
                    k += 1
                st.warning("Maximum iterations reached.")
                st.metric(label="Best Estimate (x)", value=format_res(x_hat))
        except Exception as e:
            st.error(f"Invalid input or mathematical error: {e}")

def secants_ui():
    st.header("Method of Secants")
    st.markdown("Find the root utilizing secant lines through sequential estimates.")
    st.divider()

    with st.form("secants_form"):
        eq_str = st.text_input("Enter equation in terms of 'x'", value="x**2 - 4")
        
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("First initial guess (a)", value=0.0)
            b = st.number_input("Second initial guess (b)", value=5.0)
        with col2:
            tol = st.number_input("Tolerance", value=0.0001, format="%.5f")
            max_iter = st.number_input("Max iterations", value=50, step=1)
            
        submitted = st.form_submit_button("Calculate Root", type="primary")
        
    if submitted:
        try:
            x = sp.Symbol('x')
            f_expr = sp.sympify(eq_str)
            f = sp.lambdify(x, f_expr, 'math')
            
            k = 1
            x_hat = b
            with st.spinner("Calculating..."):
                while k <= max_iter:
                    f_a = f(a)
                    f_b = f(b)
                    if f_b == f_a:
                        st.error("f(b) == f(a). Division by zero detected.")
                        return
                        
                    x_hat = a - f_a * (a - b) / (f_a - f_b)
                    
                    if abs(f(x_hat)) < tol:
                        st.success(f"Tolerance met after {k} iterations.")
                        st.metric(label="Estimated Root (x)", value=format_res(x_hat))
                        return
                    
                    a = b
                    b = x_hat
                    k += 1
                st.warning("Maximum iterations reached.")
                st.metric(label="Best Estimate (x)", value=format_res(x_hat))
        except Exception as e:
            st.error(f"Invalid input or mathematical error: {e}")

def newtons_ui():
    st.header("Newton's Method")
    st.markdown("Utilize the derivative of a function to rapidly converge on a root.")
    st.divider()

    with st.form("newtons_form"):
        eq_str = st.text_input("Enter equation in terms of 'x'", value="x**2 - 4")
        
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("Initial guess (a)", value=5.0)
            tol = st.number_input("Tolerance", value=0.0001, format="%.5f")
        with col2:
            max_iter = st.number_input("Max iterations", value=50, step=1)
            
        submitted = st.form_submit_button("Calculate Root", type="primary")
        
    if submitted:
        try:
            x = sp.Symbol('x')
            f_expr = sp.sympify(eq_str)
            f = sp.lambdify(x, f_expr, 'math')
            
            f_prime_expr = sp.diff(f_expr, x)
            f_prime = sp.lambdify(x, f_prime_expr, 'math')
            
            st.info(f"Automatically calculated derivative: `{f_prime_expr}`")
            
            k = 1
            with st.spinner("Calculating..."):
                while k <= max_iter:
                    if abs(f(a)) < tol:
                        st.success(f"Tolerance met after {k-1} iterations.")
                        st.metric(label="Estimated Root (x)", value=format_res(a))
                        return
                    
                    f_prime_a = f_prime(a)
                    if f_prime_a != 0:
                        a = a - f(a) / f_prime_a
                    else:
                        st.error("Derivative is zero. Terminating to avoid division by zero.")
                        return
                    k += 1
                st.warning("Maximum iterations reached.")
                st.metric(label="Best Estimate (x)", value=format_res(a))
        except Exception as e:
            st.error(f"Invalid input or mathematical error: {e}")

# --- 2. MATRICES ---

def create_interactive_matrix(name, rows, cols):
    st.write(f"**Matrix {name}**")
    df = pd.DataFrame(np.zeros((rows, cols)))
    return st.data_editor(df, key=f"matrix_{name}_{rows}x{cols}", num_rows="fixed")

def matrix_ui(operation):
    st.header(f"Matrix {operation.capitalize()}")
    st.markdown("Perform linear algebra operations on dynamically scaled matrices.")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        r_a = st.number_input("Matrix A Rows", min_value=1, value=2, key="ra")
        c_a = st.number_input("Matrix A Cols", min_value=1, value=2, key="ca")
        df_A = create_interactive_matrix("A", r_a, c_a)
    
    with col2:
        if operation in ["addition", "subtraction"]:
            r_b, c_b = r_a, c_a
            st.write(f"Matrix B Rows: {r_b} *(Forced to match A)*")
            st.write(f"Matrix B Cols: {c_b} *(Forced to match A)*")
        elif operation == "multiplication":
            r_b = c_a
            st.write(f"Matrix B Rows: {r_b} *(Forced to match A cols)*")
            c_b = st.number_input("Matrix B Cols", min_value=1, value=2, key="cb")
            
        df_B = create_interactive_matrix("B", r_b, c_b)

    st.divider()
    if st.button(f"Calculate {operation.capitalize()}", type="primary"):
        A = df_A.to_numpy()
        B = df_B.to_numpy()
        
        try:
            if operation == "addition":
                C = A + B
            elif operation == "subtraction":
                C = A - B
            elif operation == "multiplication":
                C = np.dot(A, B)
                
            st.success("Success! Here is the resulting matrix:")
            
            # Formatting to 4 decimal places or integer
            C_formatted = [[int(val) if float(val).is_integer() else round(float(val), 4) for val in row] for row in C]
            st.dataframe(pd.DataFrame(C_formatted), use_container_width=True)
            
        except Exception as e:
            st.error(f"Error computing matrix: {e}")

# --- 3. APPROXIMATIONS ---

def least_squares_ui():
    st.header("Least Squares Approximation")
    st.markdown("Fit a polynomial curve to a set of coordinate data.")
    st.divider()

    with st.form("least_squares_form"):
        col1, col2 = st.columns(2)
        with col1:
            x_input = st.text_input("Enter X values (comma-separated)", value="1, 2, 3, 4, 5")
        with col2:
            y_input = st.text_input("Enter Y values (comma-separated)", value="2, 4, 5, 4, 5")
            
        degree = st.number_input("Polynomial Degree", min_value=1, value=1)
        submitted = st.form_submit_button("Calculate Least Squares", type="primary")
        
    if submitted:
        try:
            x_vals = np.array([float(i.strip()) for i in x_input.split(',')])
            y_vals = np.array([float(i.strip()) for i in y_input.split(',')])
            
            if len(x_vals) != len(y_vals):
                st.error("X and Y must have the same number of data points.")
                return
            if degree >= len(x_vals):
                st.warning("Warning: Fitting a polynomial of this degree may lead to overfitting.")
                
            coeffs = np.polyfit(x_vals, y_vals, degree)
            x_sym = sp.Symbol('x')
            poly_expr = sum(c * x_sym**(degree - i) for i, c in enumerate(coeffs))
            
            st.success("Calculation Complete")
            st.info(f"Function: `{poly_expr}`")
            
            predictions = np.polyval(coeffs, x_vals)
            df = pd.DataFrame({'X': x_vals, 'Actual Y': y_vals, 'Predicted Y': predictions})
            st.dataframe(df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

def cubic_splines_ui():
    st.header("Cubic Splines")
    st.markdown("Evaluate piece-wise polynomial interpolations across data points.")
    st.divider()

    with st.form("cubic_splines_form"):
        col1, col2 = st.columns(2)
        with col1:
            x_input = st.text_input("Enter X values (comma-separated)", value="1, 2, 3, 4, 5")
        with col2:
            y_input = st.text_input("Enter Y values (comma-separated)", value="2, 4, 5, 4, 5")
            
        eval_x = st.number_input("Enter an 'x' value to estimate 'y'", value=2.5)
        submitted = st.form_submit_button("Calculate Spline", type="primary")
        
    if submitted:
        try:
            x_vals = [float(i.strip()) for i in x_input.split(',')]
            y_vals = [float(i.strip()) for i in y_input.split(',')]
            
            if len(x_vals) < 3:
                st.error("At least 3 points are required.")
                return
                
            sorted_pairs = sorted(zip(x_vals, y_vals))
            x_sorted = np.array([p[0] for p in sorted_pairs])
            y_sorted = np.array([p[1] for p in sorted_pairs])
            
            cs = CubicSpline(x_sorted, y_sorted, bc_type='not-a-knot')
            result = cs(eval_x)
            
            st.success("Spline generated successfully.")
            st.metric(label=f"Interpolated value for f({eval_x})", value=f"{result:.4f}")
        except Exception as e:
            st.error(f"Error: {e}")

def pca_ui():
    st.header("Principal Component Analysis")
    st.markdown("Analyze patterns in data dimensionality by extracting principal components.")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        r = st.number_input("Number of samples (rows)", min_value=2, value=4)
    with col2:
        c = st.number_input("Number of features (columns)", min_value=1, value=3)
    
    df_data = create_interactive_matrix("Data", r, c)
    st.divider()

    if st.button("Calculate PCA", type="primary"):
        try:
            X = df_data.to_numpy()
            
            mu = np.mean(X, axis=0)
            Xc = X - mu
            C = np.cov(Xc, rowvar=False)
            eigenvalues, V = np.linalg.eigh(C)
            D = np.diag(eigenvalues)
            Y = np.dot(Xc, V)
            
            st.subheader("Results")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**Centered Data:**")
                st.dataframe(pd.DataFrame(Xc), use_container_width=True)
                st.write("**Covariance Matrix:**")
                st.dataframe(pd.DataFrame(C), use_container_width=True)
                st.write("**Eigenvalues:**")
                st.dataframe(pd.DataFrame(D), use_container_width=True)
            with col_b:
                st.write("**Eigenvectors:**")
                st.dataframe(pd.DataFrame(V), use_container_width=True)
                st.write("**Principal Components:**")
                st.dataframe(pd.DataFrame(Y), use_container_width=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

# --- MAIN SIDEBAR ROUTING ---

st.sidebar.title("Computational Science")
st.sidebar.markdown("Select a mathematical method from the dropdown below to begin.")
category = st.sidebar.selectbox(
    "Category", 
    ["Single Variable Equation", "System of Linear Equations", "Approximation"]
)

st.sidebar.divider()

if category == "Single Variable Equation":
    method = st.sidebar.radio("Subfunction", ["Bisection", "Linear Interpolation", "Method of Secants", "Newton's Method"])
    if method == "Bisection": bisection_ui()
    elif method == "Linear Interpolation": linear_interpolation_ui()
    elif method == "Method of Secants": secants_ui()
    elif method == "Newton's Method": newtons_ui()

elif category == "System of Linear Equations":
    method = st.sidebar.radio("Subfunction", ["Addition", "Subtraction", "Multiplication"])
    matrix_ui(method.lower())

elif category == "Approximation":
    method = st.sidebar.radio("Subfunction", ["Least Squares", "Cubic Splines", "Principal Component Analysis"])
    if method == "Least Squares": least_squares_ui()
    elif method == "Cubic Splines": cubic_splines_ui()
    elif method == "Principal Component Analysis": pca_ui()
