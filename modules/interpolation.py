import streamlit as st
import sympy as sp
from utils import sign, render_root_results

def linear_interpolation_ui():
    st.header("Linear Interpolation")
    st.markdown("Estimate the root of a function using linear segments.")
    st.divider()

    col_in, col_out = st.columns([1, 1], gap="large")

    with col_in:
        with st.container(border=True):
            with st.form("linear_interp_form"):
                eq_str = st.text_input("Enter equation in terms of 'x'", value="x**3 - 4*x + 1")
                c1, c2 = st.columns(2)
                with c1:
                    a = st.number_input("Lower bound (a)", value=0.0)
                    tol = st.number_input("Tolerance", value=0.0001, format="%.5f")
                with c2:
                    b = st.number_input("Upper bound (b)", value=1.0)
                    max_iter = st.number_input("Max iterations", value=50, step=1)
                submitted = st.form_submit_button("Calculate Root", type="primary")
            
    if submitted:
        try:
            x = sp.Symbol('x')
            f_expr = sp.sympify(eq_str)
            f = sp.lambdify(x, f_expr, 'math')
            
            if f(a) * f(b) > 0:
                render_root_results(col_out, f_expr, None, None, None, "Function must have opposite signs at bounds.", "error")
                return

            k = 1
            x_hat = a
            while k <= max_iter:
                f_a, f_b = f(a), f(b)
                if f_a - f_b == 0:
                    render_root_results(col_out, f_expr, None, None, None, "Division by zero detected.", "error")
                    return
                    
                x_hat = a - f_a * (a - b) / (f_a - f_b)
                
                if abs(f(x_hat)) < tol:
                    render_root_results(col_out, f_expr, x_hat, f(x_hat), k, f"Tolerance met after {k} iterations.", "success")
                    break
                if sign(f(x_hat)) == 0:
                    render_root_results(col_out, f_expr, x_hat, f(x_hat), k, f"Exact root found after {k} iterations.", "success")
                    break
                elif sign(f(x_hat)) == sign(f(a)): a = x_hat
                elif sign(f(x_hat)) == sign(f(b)): b = x_hat
                k += 1
            else:
                render_root_results(col_out, f_expr, x_hat, f(x_hat), max_iter, "Maximum iterations reached.", "warning")
        except Exception as e:
            render_root_results(col_out, None, None, None, None, f"Mathematical error: {e}", "error")
