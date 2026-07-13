import streamlit as st
import numpy as np
import sympy as sp
from scipy.interpolate import CubicSpline
import pandas as pd
import re

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Computational Science Toolkit", page_icon="🧮", layout="wide")

# --- CUSTOM CSS THEME INJECTION ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #121212; 
        color: #FFFFFF;
    }
    
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #222222;
        border-right: 1px solid #333333;
    }
    
    /* Sidebar Text */
    [data-testid="stSidebar"] * {
        color: #FFFFFF;
    }
    
    /* === BUTTON STYLING === */
    /* Sidebar Buttons */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #d4ff00 !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 800 !important;
        border-radius: 20px !important; /* Pill shape */
        width: 100%;
        padding: 10px;
        margin-bottom: 8px;
        transition: transform 0.1s ease-in-out;
    }
    [data-testid="stSidebar"] .stButton > button:active {
        transform: scale(0.98);
    }

    /* Primary Submit Button (Calculate) */
    [data-testid="baseButton-primary"] {
        background-color: #d4ff00 !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 800 !important;
        border-radius: 6px !important;
        width: 100%;
        padding: 10px;
        transition: transform 0.1s ease-in-out;
    }
    [data-testid="baseButton-primary"]:active {
        transform: scale(0.98);
    }
    
    /* === INPUT STYLING === */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #7A7A7A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 4px !important;
    }
    
    /* Input Disabled Backgrounds */
    .stTextInput>div>div>input:disabled {
        background-color: #555555 !important;
        color: #DDDDDD !important;
    }
    
    /* Label Colors */
    label, .stTextInput label p, .stNumberInput label p {
        color: #AAAAAA !important;
        font-family: monospace;
        font-size: 0.9rem !important;
    }
    
    /* === TAB STYLING === */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        gap: 0px;
        border-bottom: 1px solid #333333;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #222222;
        border-radius: 0px;
        padding: 12px 24px;
        border: 1px solid #1E1E1E;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #8E8E8E;
        font-family: monospace;
        font-size: 1rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #d4ff00 !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #000000 !important;
        font-weight: 900;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    
    /* === FORM CONTAINER === */
    [data-testid="stForm"] {
        background-color: #262626;
        padding: 25px;
        border-radius: 0 0 8px 8px;
        border: 1px solid #333333;
        border-top: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def sign(val):
    if val > 0: return 1
    elif val < 0: return -1
    else: return 0

def format_res(val):
    if val is None: return ""
    if float(val).is_integer():
        return f"{int(val)}"
    return f"{float(val):.6f}"

def format_matrix(matrix):
    return [[int(val) if float(val).is_integer() else round(float(val), 6) for val in row] for row in matrix]

def render_results(col_out, eq_expr, root, f_val, iterations, status_msg, status_type="success"):
    with col_out:
        st.markdown("<span style='color:#AAAAAA; font-family:monospace; font-size:0.9rem;'>Interpreted Equation:</span>", unsafe_allow_html=True)
        if eq_expr:
            st.latex(f"f(x) = {sp.latex(eq_expr)}")
            
        st.write("") 
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.text_input("Estimated Root", value=format_res(root), disabled=True)
            st.text_input("Iterations Used", value=str(iterations) if iterations is not None else "", disabled=True)
        with res_col2:
            st.text_input("f(x) at Root", value=format_res(f_val), disabled=True)
            
        st.write("") 
        if status_type == "success":
            st.success(status_msg)
        elif status_type == "warning":
            st.warning(status_msg)
        elif status_type == "error":
            st.error(status_msg)

# --- 1. SINGLE VARIABLE EQUATIONS ---

def bisection_ui():
    col_in, col_spacer, col_out = st.columns([1.2, 0.1, 1.2])
    
    with col_in:
        with st.form("bisection_form"):
            eq_str = st.text_input("Enter equation in terms of 'x'", value="x**3 - 4*x + 1")
            
            c1, c2 = st.columns(2)
            with c1:
                a = st.number_input("Lower bound (a)", value=0.0)
                tol = st.number_input("Tolerance", value=0.0001, format="%.5f")
            with c2:
                b = st.number_input("Upper bound (b)", value=1.0)
                max_iter = st.number_input("Iterations", value=50, step=1, min_value=1)
                
            submitted = st.form_submit_button("Calculate Root", type="primary")
            
    if submitted:
        try:
            x = sp.Symbol('x')
            f_expr = sp.sympify(eq_str)
            f = sp.lambdify(x, f_expr, 'numpy')
            
            val_a, val_b = float(f(a)), float(f(b))
            
            if val_a * val_b > 0:
                render_results(col_out, f_expr, None, None, None, "Error: f(a) and f(b) must have opposite signs. Try different bounds.", "error")
                return

            k = 1
            x_hat = a
            while k <= max_iter:
                x_hat = (a + b) / 2.0
                val_x_hat = float(f(x_hat))
                
                if abs(b - a) / 2.0 < tol or val_x_hat == 0:
                    render_results(col_out, f_expr, x_hat, val_x_hat, k, f"Root found within tolerance after {k} iterations.", "success")
                    break
                
                if sign(val_x_hat) == sign(val_a):
                    a = x_hat
                    val_a = val_x_hat
                else:
                    b = x_hat
                k += 1
            else:
                render_results(col_out, f_expr, x_hat, float(f(x_hat)), max_iter, "Maximum iterations reached before meeting tolerance.", "warning")
                
        except Exception as e:
            render_results(col_out, None, None, None, None, f"Calculation Error: Check your equation syntax. ({e})", "error")

def linear_interpolation_ui():
    col_in, col_spacer, col_out = st.columns([1.2, 0.1, 1.2])

    with col_in:
        with st.form("linear_interp_form"):
            eq_str = st.text_input("Enter equation in terms of 'x'", value="x**3 - 4*x + 1")
            
            c1, c2 = st.columns(2)
            with c1:
                a = st.number_input("Lower bound (a)", value=0.0)
                tol = st.number_input("Tolerance", value=0.0001, format="%.5f")
            with c2:
                b = st.number_input("Upper bound (b)", value=1.0)
                max_iter = st.number_input("Iterations", value=50, step=1, min_value=1)
                
            submitted = st.form_submit_button("Calculate Root", type="primary")
            
    if submitted:
        try:
            x = sp.Symbol('x')
            f_expr = sp.sympify(eq_str)
            f = sp.lambdify(x, f_expr, 'numpy')
            
            val_a, val_b = float(f(a)), float(f(b))
            
            if val_a * val_b > 0:
                render_results(col_out, f_expr, None, None, None, "Error: f(a) and f(b) must have opposite signs.", "error")
                return

            k = 1
            x_hat = a
            while k <= max_iter:
                val_a = float(f(a))
                val_b = float(f(b))
                
                if val_a - val_b == 0:
                    render_results(col_out, f_expr, None, None, None, "Division by zero detected (f(a) == f(b)).", "error")
                    return
                    
                x_hat = a - val_a * (a - b) / (val_a - val_b)
                val_x_hat = float(f(x_hat))
                
                if abs(val_x_hat) < tol:
                    render_results(col_out, f_expr, x_hat, val_x_hat, k, f"Tolerance met after {k} iterations.", "success")
                    break
                    
                if sign(val_x_hat) == 0:
                    render_results(col_out, f_expr, x_hat, val_x_hat, k, f"Exact root found after {k} iterations.", "success")
                    break
                elif sign(val_x_hat) == sign(val_a):
                    a = x_hat
                else:
                    b = x_hat
                k += 1
            else:
                render_results(col_out, f_expr, x_hat, float(f(x_hat)), max_iter, "Maximum iterations reached.", "warning")
                
        except Exception as e:
            render_results(col_out, None, None, None, None, f"Calculation Error: {e}", "error")

def secants_ui():
    col_in, col_spacer, col_out = st.columns([1.2, 0.1, 1.2])

    with col_in:
        with st.form("secants_form"):
            eq_str = st.text_input("Enter equation in terms of 'x'", value="x**3 - 4*x + 1")
            
            c1, c2 = st.columns(2)
            with c1:
                a = st.number_input("First initial guess (a)", value=0.0)
                b = st.number_input("Second initial guess (b)", value=1.0)
            with c2:
                tol = st.number_input("Tolerance", value=0.0001, format="%.5f")
                max_iter = st.number_input("Iterations", value=50, step=1, min_value=1)
                
            submitted = st.form_submit_button("Calculate Root", type="primary")
            
    if submitted:
        try:
            x = sp.Symbol('x')
            f_expr = sp.sympify(eq_str)
            f = sp.lambdify(x, f_expr, 'numpy')
            
            k = 1
            x_hat = b
            while k <= max_iter:
                val_a = float(f(a))
                val_b = float(f(b))
                
                if val_b == val_a:
                    render_results(col_out, f_expr, None, None, None, "f(b) == f(a). Division by zero detected.", "error")
                    return
                    
                x_hat = a - val_a * (a - b) / (val_a - val_b)
                val_x_hat = float(f(x_hat))
                
                if abs(val_x_hat) < tol:
                    render_results(col_out, f_expr, x_hat, val_x_hat, k, f"Tolerance met after {k} iterations.", "success")
                    break
                
                a = b
                b = x_hat
                k += 1
            else:
                render_results(col_out, f_expr, x_hat, float(f(x_hat)), max_iter, "Maximum iterations reached.", "warning")
                
        except Exception as e:
            render_results(col_out, None, None, None, None, f"Calculation Error: {e}", "error")

def newtons_ui():
    col_in, col_spacer, col_out = st.columns([1.2, 0.1, 1.2])

    with col_in:
        with st.form("newtons_form"):
            eq_str = st.text_input("Enter equation in terms of 'x'", value="x**3 - 4*x + 1")
            
            c1, c2 = st.columns(2)
            with c1:
                a = st.number_input("Initial guess (a)", value=1.0)
                tol = st.number_input("Tolerance", value=0.0001, format="%.5f")
            with c2:
                max_iter = st.number_input("Iterations", value=50, step=1, min_value=1)
                
            submitted = st.form_submit_button("Calculate Root", type="primary")
            
    if submitted:
        try:
            x = sp.Symbol('x')
            f_expr = sp.sympify(eq_str)
            f = sp.lambdify(x, f_expr, 'numpy')
            
            f_prime_expr = sp.diff(f_expr, x)
            f_prime = sp.lambdify(x, f_prime_expr, 'numpy')
            
            k = 1
            while k <= max_iter:
                val_a = float(f(a))
                if abs(val_a) < tol:
                    render_results(col_out, f_expr, a, val_a, k-1, f"Tolerance met after {k-1} iterations.", "success")
                    break
                
                f_prime_a = float(f_prime(a))
                if f_prime_a != 0:
                    a = a - val_a / f_prime_a
                else:
                    render_results(col_out, f_expr, None, None, None, "Derivative is zero. Terminating to avoid division by zero.", "error")
                    return
                k += 1
            else:
                render_results(col_out, f_expr, a, float(f(a)), max_iter, "Maximum iterations reached.", "warning")
                
        except Exception as e:
            render_results(col_out, None, None, None, None, f"Calculation Error: Make sure syntax is valid. ({e})", "error")

# --- 2. MATRICES ---

def create_interactive_matrix(name, rows, cols):
    st.markdown(f"<span style='color:#AAAAAA; font-family:monospace; font-size:0.9rem;'>Matrix {name}</span>", unsafe_allow_html=True)
    df = pd.DataFrame(np.zeros((rows, cols)))
    return st.data_editor(df, key=f"matrix_{name}_{rows}x{cols}", num_rows="fixed")

def matrix_ui(operation):
    col_in, col_spacer, col_out = st.columns([1.2, 0.1, 1.2])

    with col_in:
        c1, c2 = st.columns(2)
        with c1:
            r_a = st.number_input("Matrix A Rows", min_value=1, value=2, key="ra")
            c_a = st.number_input("Matrix A Cols", min_value=1, value=2, key="ca")
            df_A = create_interactive_matrix("A", r_a, c_a)
        
        with c2:
            if operation in ["addition", "subtraction"]:
                r_b, c_b = r_a, c_a
                st.text_input("Matrix B Rows", value=r_b, disabled=True)
                st.text_input("Matrix B Cols", value=c_b, disabled=True)
            elif operation == "multiplication":
                r_b = c_a
                st.text_input("Matrix B Rows", value=r_b, disabled=True)
                c_b = st.number_input("Matrix B Cols", min_value=1, value=2, key="cb")
                
            df_B = create_interactive_matrix("B", r_b, c_b)

        calc_btn = st.button(f"Calculate {operation.capitalize()}", type="primary")

    with col_out:
        st.markdown("<span style='color:#AAAAAA; font-family:monospace; font-size:0.9rem;'>Resulting Matrix:</span>", unsafe_allow_html=True)
        if calc_btn:
            try:
                # Force matrices to be floats (handles accidental string inputs from the data editor)
                A = df_A.astype(float).to_numpy()
                B = df_B.astype(float).to_numpy()
                
                if operation == "addition": C = A + B
                elif operation == "subtraction": C = A - B
                elif operation == "multiplication": C = np.dot(A, B)
                
                st.dataframe(pd.DataFrame(format_matrix(C)), use_container_width=True)
                st.success("Matrix computed successfully.")
            except Exception as e:
                st.error(f"Error computing matrix. Ensure all cells contain valid numbers. ({e})")

def gaussian_elimination_ui():
    col_in, col_spacer, col_out = st.columns([1.2, 0.1, 1.2])

    with col_in:
        with st.form("gaussian_form"):
            st.markdown("<span style='color:#AAAAAA; font-family:monospace; font-size:0.9rem;'>Enter equations (e.g., 2x + y = 5)</span>", unsafe_allow_html=True)
            eq_input = st.text_area("", value="2*x + y = 5\nx - y = 1", height=150, label_visibility="collapsed")
            submitted = st.form_submit_button("Solve System", type="primary")

    with col_out:
        if submitted:
            try:
                raw_lines = [line.strip() for line in eq_input.split('\n') if line.strip()]
                num_eq = len(raw_lines)
                
                if num_eq <= 0:
                    st.error("Please enter at least one equation.")
                    return
                
                equations = []
                for eq_str in raw_lines:
                    # Robust substitution to convert implicit multiplication like '2x' to '2*x' safely
                    eq_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq_str)
                    if '=' in eq_str:
                        lhs, rhs = eq_str.split('=', 1)
                        expr_str = f"({lhs}) - ({rhs})"
                    else:
                        expr_str = eq_str
                    equations.append(sp.sympify(expr_str))
                    
                symbols = set()
                for eq in equations:
                    symbols.update(eq.free_symbols)
                symbols = sorted(list(symbols), key=lambda s: s.name)
                
                if len(symbols) != num_eq:
                    st.error(f"System must be square. Found {len(symbols)} unique variables and {num_eq} equations.")
                    return
                    
                A_sp, b_sp = sp.linear_eq_to_matrix(equations, *symbols)
                A = np.array(A_sp).astype(float)
                b = np.array(b_sp).astype(float).flatten()
                n = len(b)
                
                augmented_matrix = np.column_stack((A, b))
                
                # Gaussian Elimination logic with partial pivoting
                for i in range(n):
                    max_row = i + np.argmax(np.abs(augmented_matrix[i:n, i]))
                    if augmented_matrix[max_row, i] == 0:
                        st.error("System is singular or has infinite solutions.")
                        return
                    augmented_matrix[[i, max_row]] = augmented_matrix[[max_row, i]]
                    for j in range(i + 1, n):
                        factor = augmented_matrix[j, i] / augmented_matrix[i, i]
                        augmented_matrix[j, i:] = augmented_matrix[j, i:] - factor * augmented_matrix[i, i:]
                        
                # Back substitution
                x = np.zeros(n)
                for i in range(n - 1, -1, -1):
                    x[i] = (augmented_matrix[i, -1] - np.dot(augmented_matrix[i, i+1:n], x[i+1:n])) / augmented_matrix[i, i]
                    
                st.markdown("<span style='color:#AAAAAA; font-family:monospace; font-size:0.9rem;'>Solutions:</span>", unsafe_allow_html=True)
                res_cols = st.columns(len(symbols))
                for idx, (var, sol) in enumerate(zip(symbols, x)):
                    with res_cols[idx % len(res_cols)]:
                        st.text_input(f"Variable {var}", value=format_res(sol), disabled=True)
                st.success("System solved via Gaussian Elimination.")
                    
            except Exception as e:
                st.error(f"Parse or Math Error: {e}. Ensure variables match and equations use proper formatting (e.g., '2*x + y = 5').")

# --- 3. APPROXIMATIONS ---

def least_squares_ui():
    col_in, col_spacer, col_out = st.columns([1.2, 0.1, 1.2])

    with col_in:
        with st.form("least_squares_form"):
            c1, c2 = st.columns(2)
            with c1:
                x_input = st.text_input("X values (comma-separated)", value="-2, -1, 0, 1, 2, 3")
            with c2:
                y_input = st.text_input("Y values (comma-separated)", value="2, 2, 1, 0, 0, 3")
                
            degree = st.number_input("Polynomial Degree", min_value=1, value=2, step=1)
            submitted = st.form_submit_button("Calculate Least Squares", type="primary")
            
    with col_out:
        if submitted:
            try:
                x_vals = np.array([float(i.strip()) for i in x_input.split(',') if i.strip()])
                y_vals = np.array([float(i.strip()) for i in y_input.split(',') if i.strip()])
                
                if len(x_vals) != len(y_vals):
                    st.error("X and Y inputs must have the exact same number of data points.")
                    return
                if len(x_vals) <= degree:
                    st.warning(f"Warning: A polynomial of degree {degree} requires at least {degree + 1} points to fit perfectly without overfitting.")
                    
                coeffs = np.polyfit(x_vals, y_vals, degree)
                x_sym = sp.Symbol('x')
                
                # Construct polynomial string for SymPy cleanly
                poly_expr = sum(c * (x_sym ** (degree - i)) for i, c in enumerate(coeffs))
                
                st.markdown("<span style='color:#AAAAAA; font-family:monospace; font-size:0.9rem;'>Fitted Polynomial Equation:</span>", unsafe_allow_html=True)
                st.latex(f"f(x) = {sp.latex(poly_expr)}")
                st.write("")
                
                predictions = np.polyval(coeffs, x_vals)
                pred_formatted = [round(p, 4) if not float(p).is_integer() else int(p) for p in predictions]
                
                df = pd.DataFrame({'X': x_vals, 'Actual Y': y_vals, 'Predicted Y': pred_formatted})
                st.dataframe(df, use_container_width=True)
                st.success("Curve fitted successfully.")
                
            except Exception as e:
                st.error(f"Error computing Least Squares. Please check formatting of inputs. ({e})")

def cubic_splines_ui():
    col_in, col_spacer, col_out = st.columns([1.2, 0.1, 1.2])

    with col_in:
        with st.form("cubic_splines_form"):
            c1, c2 = st.columns(2)
            with c1:
                x_input = st.text_input("X values (comma-separated)", value="1, 2, 3, 4, 5")
            with c2:
                y_input = st.text_input("Y values (comma-separated)", value="2, 4, 5, 4, 5")
                
            eval_x = st.number_input("Enter 'x' value to estimate 'y'", value=2.5)
            submitted = st.form_submit_button("Calculate Spline", type="primary")
            
    with col_out:
        if submitted:
            try:
                x_vals = [float(i.strip()) for i in x_input.split(',') if i.strip()]
                y_vals = [float(i.strip()) for i in y_input.split(',') if i.strip()]
                
                if len(x_vals) != len(y_vals):
                    st.error("X and Y inputs must have the exact same number of data points.")
                    return
                if len(x_vals) < 4:
                    st.error("Cubic splines generally require at least 4 distinct data points.")
                    return
                    
                sorted_pairs = sorted(zip(x_vals, y_vals))
                x_sorted = np.array([p[0] for p in sorted_pairs])
                y_sorted = np.array([p[1] for p in sorted_pairs])
                
                # Check for duplicate X values
                if len(x_sorted) != len(np.unique(x_sorted)):
                    st.error("Duplicate X values found. Cubic Splines require unique X coordinates.")
                    return
                
                cs = CubicSpline(x_sorted, y_sorted, bc_type='not-a-knot')
                result = cs(eval_x)
                
                st.markdown("<span style='color:#AAAAAA; font-family:monospace; font-size:0.9rem;'>Interpolated Result:</span>", unsafe_allow_html=True)
                st.text_input(f"f({eval_x})", value=format_res(result), disabled=True)
                st.success("Spline generated successfully.")
            except Exception as e:
                st.error(f"Error generating spline: {e}")

def pca_ui():
    col_in, col_spacer, col_out = st.columns([1.2, 0.1, 1.2])

    with col_in:
        c1, c2 = st.columns(2)
        with c1:
            r = st.number_input("Number of samples (rows)", min_value=2, value=4)
        with c2:
            c = st.number_input("Number of features (cols)", min_value=1, value=3)
        
        df_data = create_interactive_matrix("Data", r, c)
        calc_btn = st.button("Calculate PCA", type="primary")

    with col_out:
        if calc_btn:
            try:
                X = df_data.astype(float).to_numpy()
                
                if X.shape[0] < 2:
                    st.error("PCA requires at least 2 samples (rows) to compute covariance.")
                    return
                    
                mu = np.mean(X, axis=0)
                Xc = X - mu
                C = np.cov(Xc, rowvar=False)
                
                # Handle edge case where there's only 1 feature
                if X.shape[1] == 1:
                    C = np.array([[C]]) if np.isscalar(C) else C

                eigenvalues, V = np.linalg.eigh(C)
                
                # Sort descending
                idx = np.argsort(eigenvalues)[::-1]
                V = V[:, idx]
                
                Y = np.dot(Xc, V)
                
                st.markdown("<span style='color:#AAAAAA; font-family:monospace; font-size:0.9rem;'>Principal Components:</span>", unsafe_allow_html=True)
                st.dataframe(pd.DataFrame(format_matrix(Y)), use_container_width=True)
                st.success("PCA Calculated successfully.")
            except Exception as e:
                st.error(f"Error computing PCA. Verify data inputs are valid. ({e})")


# --- STATE INITIALIZATION ---
if "main_category" not in st.session_state:
    st.session_state.main_category = "Single Variable Equation"

# --- SIDEBAR ---
with st.sidebar:
    col_logo, col_text = st.columns([1, 4])
    with col_logo:
        try:
            st.image("ComputationalLOGO.png", use_container_width=True)
        except:
            st.markdown("📈") 
            
    with col_text:
        st.markdown("<h3 style='color: white; margin-top: 0; padding-top: 0; font-family: monospace; font-size: 1.1rem;'>Computational<br><span style='color: #d4ff00;'>Toolkit</span></h3>", unsafe_allow_html=True)
    
    st.write("") 
    st.write("") 
    
    if st.button("Single Variable Equation"): st.session_state.main_category = "Single Variable Equation"
    if st.button("System of Linear Equations"): st.session_state.main_category = "System of Linear Equations"
    if st.button("Approximation"): st.session_state.main_category = "Approximation"

# --- MAIN AREA ---
if st.session_state.main_category == "Single Variable Equation":
    tabs = st.tabs(["Bisection", "Linear Interpolation", "Method of Secants", "Newton's Method"])
    with tabs[0]: bisection_ui()
    with tabs[1]: linear_interpolation_ui()
    with tabs[2]: secants_ui()
    with tabs[3]: newtons_ui()

elif st.session_state.main_category == "System of Linear Equations":
    tabs = st.tabs(["Addition", "Subtraction", "Multiplication", "Gaussian Elimination"])
    with tabs[0]: matrix_ui("addition")
    with tabs[1]: matrix_ui("subtraction")
    with tabs[2]: matrix_ui("multiplication")
    with tabs[3]: gaussian_elimination_ui()

elif st.session_state.main_category == "Approximation":
    tabs = st.tabs(["Least Squares", "Cubic Splines", "Principal Component Analysis"])
    with tabs[0]: least_squares_ui()
    with tabs[1]: cubic_splines_ui()
    with tabs[2]: pca_ui()
