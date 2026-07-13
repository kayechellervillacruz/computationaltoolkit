import streamlit as st
import numpy as np
import sympy as sp
import pandas as pd
import re
from utils import format_matrix, format_res

def gaussian_elimination_ui():
    col_in, col_out = st.columns([1, 1], gap="large")

    with col_in:
        with st.container(border=True):
            with st.form("gaussian_form"):
                st.markdown("<span style='color:#8E8E8E'>Enter equations (e.g., 2x + y = 5)</span>", unsafe_allow_html=True)
                eq_input = st.text_area("", value="2x + y = 5\nx - y = 1", height=150, label_visibility="collapsed")
                submitted = st.form_submit_button("Solve System", type="primary")

    if submitted:
        with col_out:
            with st.container(border=True):
                try:
                    raw_lines = [line.strip() for line in eq_input.split('\n') if line.strip()]
                    num_eq = len(raw_lines)
                    if num_eq <= 0: return st.error("Enter at least one equation.")
                    
                    equations = []
                    for eq_str in raw_lines:
                        eq_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq_str)
                        if '=' in eq_str:
                            lhs, rhs = eq_str.split('=', 1)
                            expr_str = f"({lhs}) - ({rhs})"
                        else:
                            expr_str = eq_str
                        equations.append(sp.sympify(expr_str))
                        
                    symbols = set()
                    for eq in equations: symbols.update(eq.free_symbols)
                    symbols = sorted(list(symbols), key=lambda s: s.name)
                    
                    if len(symbols) != num_eq:
                        return st.error(f"Requires square system. Found {len(symbols)} variables and {num_eq} equations.")
                        
                    A_sp, b_sp = sp.linear_eq_to_matrix(equations, *symbols)
                    A = np.array(A_sp).astype(float)
                    b = np.array(b_sp).astype(float).flatten()
                    n = len(b)
                    
                    augmented_matrix = np.column_stack((A, b))
                    
                    for i in range(n):
                        max_row = i + np.argmax(np.abs(augmented_matrix[i:n, i]))
                        if augmented_matrix[max_row, i] == 0: return st.error("System is singular.")
                        augmented_matrix[[i, max_row]] = augmented_matrix[[max_row, i]]
                        for j in range(i + 1, n):
                            factor = augmented_matrix[j, i] / augmented_matrix[i, i]
                            augmented_matrix[j, i:] = augmented_matrix[j, i:] - factor * augmented_matrix[i, i:]
                            
                    x = np.zeros(n)
                    for i in range(n - 1, -1, -1):
                        x[i] = (augmented_matrix[i, -1] - np.dot(augmented_matrix[i, i+1:n], x[i+1:n])) / augmented_matrix[i, i]
                        
                    st.markdown("<span style='color:#8E8E8E'>Solutions:</span>", unsafe_allow_html=True)
                    res_cols = st.columns(len(symbols))
                    for idx, (var, sol) in enumerate(zip(symbols, x)):
                        with res_cols[idx % len(res_cols)]:
                            st.text_input(f"Variable {var}", value=format_res(sol), disabled=True)
                    st.success("System solved via Gaussian Elimination.")
                        
                except Exception as e:
                    st.error(f"Mathematical error: {e}")
