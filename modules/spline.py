import streamlit as st
import numpy as np
from scipy.interpolate import CubicSpline
from utils import format_res

def cubic_splines_ui():
    col_in, col_out = st.columns([1, 1], gap="large")

    with col_in:
        with st.container(border=True):
            with st.form("cubic_splines_form"):
                c1, c2 = st.columns(2)
                with c1:
                    x_input = st.text_input("X values (comma-separated)", value="1, 2, 3, 4, 5")
                with c2:
                    y_input = st.text_input("Y values (comma-separated)", value="2, 4, 5, 4, 5")
                eval_x = st.number_input("Enter 'x' value to estimate 'y'", value=2.5)
                submitted = st.form_submit_button("Calculate Spline", type="primary")
            
    if submitted:
        with col_out:
            with st.container(border=True):
                try:
                    x_vals = [float(i.strip()) for i in x_input.split(',')]
                    y_vals = [float(i.strip()) for i in y_input.split(',')]
                    if len(x_vals) < 3: return st.error("At least 3 points required.")
                        
                    sorted_pairs = sorted(zip(x_vals, y_vals))
                    x_sorted = np.array([p[0] for p in sorted_pairs])
                    y_sorted = np.array([p[1] for p in sorted_pairs])
                    
                    cs = CubicSpline(x_sorted, y_sorted, bc_type='not-a-knot')
                    result = cs(eval_x)
                    
                    st.markdown("<span style='color:#8E8E8E'>Interpolated Result:</span>", unsafe_allow_html=True)
                    st.text_input(f"f({eval_x})", value=format_res(result), disabled=True)
                    st.success("Spline generated successfully.")
                except Exception as e:
                    st.error(f"Error: {e}")
