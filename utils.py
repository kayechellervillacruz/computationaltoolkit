import streamlit as st
import sympy as sp

# --- CSS LOADER ---
def load_css():
    try:
        with open("style.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception:
        pass

# --- MATHEMATICAL HELPERS ---

def sign(val):
    if val > 0: return 1
    elif val < 0: return -1
    else: return 0

def format_res(val):
    """Formats values: integers drop decimal places, floats are rounded to 4 decimals."""
    if val is None: return ""
    if float(val).is_integer():
        return f"{int(val)}"
    return f"{float(val):.4f}"

def format_matrix(matrix):
    """Formats a 2D array: integers drop decimals, floats rounded to 4 decimals."""
    return [[int(val) if float(val).is_integer() else round(float(val), 4) for val in row] for row in matrix]

# --- UI LAYOUT HELPERS ---

def render_custom_tabs(options, session_key):
    """Renders custom tab buttons using dynamic types for active state."""
    if session_key not in st.session_state:
        st.session_state[session_key] = options[0]
        
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        is_active = st.session_state[session_key] == option
        
        with cols[i]:
            # If active, use "primary" (Neon Green), else "secondary" (Dark Gray)
            btn_type = "primary" if is_active else "secondary"
            if st.button(option, key=f"tab_{option}", use_container_width=True, type=btn_type):
                st.session_state[session_key] = option
                st.rerun()

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
                st.text_input("Estimated Root", value=format_res(root), disabled=True)
                st.text_input("Iterations Used", value=str(iterations), disabled=True)
            with res_col2:
                st.text_input("f(x) at Root", value=format_res(f_val), disabled=True)
                
            st.write("")
            if status_type == "success": st.success(status_msg)
            elif status_type == "warning": st.warning(status_msg)
            elif status_type == "error": st.error(status_msg)
