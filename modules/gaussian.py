import streamlit as st
import numpy as np
import sympy as sp
import pandas as pd
import re
from utils import format_matrix, format_res

def gaussian_elimination_ui():
    st.header("Gaussian Elimination")
    st.markdown("Solve a system of linear equations using partial pivoting and back substitution.")
    st.divider()

    with st.form("gaussian_form_unique"):
        st.info("Enter your equations below, one per line. Example: `2x + y = 5`")
        eq_input = st.text_area("Linear Equations", value="2x + y = 5\nx - y = 1", height=150, key="gaussian_input_area")
        submitted = st.form_submit_button("Solve System", type="primary")

    if submitted:
        try:
            raw_lines = [line.strip() for line in eq_input.split('\n') if line.strip()]
            num_eq = len(raw_lines)
            if num_eq <= 0: return st.error("Please enter at least one equation.")
            
            equations = []
            for eq_str in raw_lines:
                eq_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq_str)
                if '=' in eq_str:
                    lhs, rhs = eq_str.split('=', 1)
                    expr_str = f"({lhs}) - ({rhs})"
                else:
                    expr_str = eq_str
                equations.append(sp.sympify(expr_str))
                
            symbols = sorted(list(set().union(*[e.free_symbols for e in equations])), key=lambda s: s.name)
            
            if not symbols: return st.error("No variables found.")
            if len(symbols) != num_eq:
                return st.error(f"Requires square system. Found {len(symbols)} variables and {num_eq} equations.")
                
            A = np.array(sp.linear_eq_to_matrix(equations, *symbols)[0]).astype(float)
            b = np.array(sp.linear_eq_to_matrix(equations, *symbols)[1]).astype(float).flatten()
            n = len(b)
            aug = np.column_stack((A, b))
            
            st.subheader("Calculation Steps")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Initial Augmented Matrix:**")
                st.dataframe(pd.DataFrame(format_matrix(aug)), use_container_width=True)
            
            for i in range(n):
                max_row = i + np.argmax(np.abs(aug[i:n, i]))
                if aug[max_row, i] == 0: return st.error("System is singular.")
                aug[[i, max_row]] = aug[[max_row, i]]
                for j in range(i + 1, n):
                    aug[j, i:] -= (aug[j, i] / aug[i, i]) * aug[i, i:]
                    
            with col2:
                st.write("**Upper Triangular Matrix:**")
                st.dataframe(pd.DataFrame(format_matrix(aug)), use_container_width=True)
                
            x = np.zeros(n)
            for i in range(n - 1, -1, -1):
                x[i] = (aug[i, -1] - np.dot(aug[i, i+1:n], x[i+1:n])) / aug[i, i]
                
            st.divider()
            st.subheader("Final Results")
            res_cols = st.columns(len(symbols))
            for idx, (var, sol) in enumerate(zip(symbols, x)):
                res_cols[idx % len(res_cols)].metric(f"Variable: {var}", format_res(sol))
        except Exception as e:
            st.error(f"Mathematical error: {e}")
