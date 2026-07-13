import streamlit as st
import sympy as sp

def sign(val):
    if val > 0: return 1
    elif val < 0: return -1
    else: return 0

def format_res(val):
    """Formats values: integers drop decimal places, floats are rounded to 4 decimals."""
    if float(val).is_integer():
        return f"{int(val)}"
    return f"{float(val):.4f}"

def format_matrix(matrix):
    """Formats a 2D array: integers drop decimals, floats rounded to 4 decimals."""
    return [[int(val) if float(val).is_integer() else round(float(val), 4) for val in row] for row in matrix]

def render_root_results(col_out, eq_expr, root, f_val, iterations, status_msg, status_type="success"):
    """Renders the single-variable output in the right column container."""
    with col_out:
        with st.container(border=True):
            st.markdown("<span style='color:#8E8E8E'>Interpreted Equation:</span>", unsafe_allow_html=True)
            if eq_expr:
                st.latex(f"f(x) = {sp.latex(eq_expr)}")
            
            st.write("")
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.text_input("Estimated Root", value=format_res(root) if root is not None else "", disabled=True)
                st.text_input("Iterations Used", value=str(iterations) if iterations is not None else "", disabled=True)
            with res_col2:
                st.text_input("f(x) at Root", value=format_res(f_val) if f_val is not None else "", disabled=True)
                
            st.write("")
            if status_type == "success": st.success(status_msg)
            elif status_type == "warning": st.warning(status_msg)
            elif status_type == "error": st.error(status_msg)
