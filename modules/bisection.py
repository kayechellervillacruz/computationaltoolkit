import streamlit as st
import sympy as sp
from utils import sign, render_root_results

def bisection_ui():
    st.header("Bisection Method")
    with st.container(border=True):
        st.markdown("Find the root of a function by repeatedly bisecting an interval.")
    st.write("")

    col_in, col_out = st.columns([1, 1], gap="large")
    
    with col_in:
        with st.container(border=True):
            st.markdown("##### ⚙️ Input Parameters")
            with st.form("bisection_form"):
                eq_str = st.text_input("Enter equation in terms of 'x'", value="x**3 - 4*x + 1")
                c1, c2 = st.columns(2)
                with c1:
                    a = st.number_input("Lower bound (a)", value=0.0)
                    tol = st.number_input("Tolerance", value=0.0001, format="%.5f")
                with c2:
                    b = st.number_input("Upper bound (b)", value=1.0)
                    max_iter = st.number_input("Max iterations", value=50, step=1)
                submitted = st.form_submit_button("Calculate Root", type="primary", use_container_width=True)
            
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
                x_hat = (a + b) / 2.0
                if abs(b - a) / 2.0 < tol:
                    render_root_results(col_out, f_expr, x_hat, f(x_hat), k, f"Tolerance met after {k} iterations.", "success")
                    break
                if sign(f(x_hat)) == sign(f(a)): a = x_hat
                elif sign(f(x_hat)) == sign(f(b)): b = x_hat
                elif sign(f(x_hat)) == 0:
                    render_root_results(col_out, f_expr, x_hat, f(x_hat), k, f"Exact root found.", "success")
                    break
                k += 1
            else:
                render_root_results(col_out, f_expr, x_hat, f(x_hat), max_iter, "Maximum iterations reached.", "warning")
        except Exception as e:
            render_root_results(col_out, None, None, None, None, f"Mathematical error: {e}", "error")
