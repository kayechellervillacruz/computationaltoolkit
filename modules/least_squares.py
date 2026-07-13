import streamlit as st
import numpy as np
import sympy as sp
import pandas as pd
from utils import format_res

def least_squares_ui():
    st.header("Least Squares Approximation")
    st.markdown("Fit a polynomial curve to a set of coordinate data.")
    st.divider()

    col_in, col_out = st.columns([1, 1], gap="large")

    with col_in:
        with st.container(border=True):
            st.markdown("##### Input Parameters")
            with st.form("least_squares_form"):
                c1, c2 = st.columns(2)
                with c1:
                    x_input = st.text_input("X values (comma-separated)", value="-2, -1, 0, 1, 2, 3")
                with c2:
                    y_input = st.text_input("Y values (comma-separated)", value="2, 2, 1, 0, 0, 3")
                    
                degree = st.number_input("Polynomial Degree", min_value=1, value=2)
                submitted = st.form_submit_button("Calculate Fit", type="primary", use_container_width=True)
            
    if submitted:
        with col_out:
            with st.container(border=True):
                st.markdown("#####  Results")
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
                    
                    # Formatting coefficients
                    rounded_coeffs = [round(c, 4) if not float(c).is_integer() else int(c) for c in coeffs]
                    poly_expr = sum(c * x_sym**(degree - i) for i, c in enumerate(rounded_coeffs))
                    
                    st.markdown("<span style='color:#8E8E8E'>Fitted Polynomial Equation:</span>", unsafe_allow_html=True)
                    st.latex(f"f(x) = {sp.latex(poly_expr)}")
                    
                    predictions = np.polyval(coeffs, x_vals)
                    pred_formatted = [float(format_res(p)) for p in predictions]
                    df = pd.DataFrame({'X': x_vals, 'Actual Y': y_vals, 'Predicted Y': pred_formatted})
                    st.dataframe(df, use_container_width=True)
                    st.success("Curve fitted successfully.")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
