import streamlit as st
import sympy as sp
from utils import render_root_results

def newtons_ui():
    st.header("Newton's Method")
    st.markdown("Utilize the derivative of a function to rapidly converge on a root.")
    st.divider()

    col_in, col_out = st.columns([1, 1], gap="large")

    with col_in:
        with st.container(border=True):
            with st.form("newtons_form"):
                eq_str = st.text_input("Enter equation in terms of 'x'", value="x**3 - 4*x + 1")
                c1, c2 = st.columns(2)
                with c1:
                    a = st.number_input("Initial guess (a)", value=1.0)
                    tol = st.number_input("Tolerance", value=0.0001, format="%.5f")
                with c2:
                    max_iter = st.number_input("Max iterations", value=50, step=1)
                submitted = st.form_submit_button("Calculate Root", type="primary")
            
    if submitted:
        try:
            x = sp.Symbol('x')
            f_expr = sp.sympify(eq_str)
            f = sp.lambdify(x, f_expr, 'math')
            f_prime_expr = sp.diff(f_expr, x)
            f_prime = sp.lambdify(x, f_prime_expr, 'math')
            
            k = 1
            while k <= max_iter:
                if abs(f(a)) < tol:
                    render_root_results(col_out, f_expr, a, f(a), k-1, f"Tolerance met after {k-1} iterations.", "success")
                    # Add derivative info specifically for Newton
                    with col_out: st.info(f"Calculated Derivative: `{f_prime_expr}`")
                    break
                
                f_prime_a = f_prime(a)
                if f_prime_a != 0:
                    a = a - f(a) / f_prime_a
                else:
                    render_root_results(col_out, f_expr, None, None, None, "Derivative is zero. Terminating.", "error")
                    return
                k += 1
            else:
                render_root_results(col_out, f_expr, a, f(a), max_iter, "Maximum iterations reached.", "warning")
        except Exception as e:
            render_root_results(col_out, None, None, None, None, f"Mathematical error: {e}", "error")
