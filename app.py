import streamlit as st
import os

# Set page config at the very top
st.set_page_config(page_title="Computational Science Toolkit", page_icon="🧮", layout="wide", initial_sidebar_state="collapsed")

# Import modular components
from modules.bisection import bisection_ui
from modules.interpolation import linear_interpolation_ui
from modules.secant import secants_ui
from modules.newton import newtons_ui
from modules.matrix import matrix_ui
from modules.gaussian import gaussian_elimination_ui
from modules.least_squares import least_squares_ui
from modules.spline import cubic_splines_ui
from modules.pca import pca_ui

# --- LOAD CSS ---
def load_css():
    try:
        with open("style.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        pass # Silently pass if style.css isn't found during init

load_css()

# --- STATE INITIALIZATION ---
if "main_category" not in st.session_state:
    st.session_state.main_category = "Single Variable Equation"

# --- MAIN LAYOUT ---
nav_col, main_col = st.columns([1, 4], gap="large")

# --- LEFT NAVIGATION PANEL ---
with nav_col:
    # Logo Area
    logo_path = os.path.join("assets", "ComputationalLOGO.png")
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("<h3 style='color: white; margin-top:0;'>Computational<br><span style='color: #d4ff00;'>Toolkit</span></h3>", unsafe_allow_html=True)
    
    st.write("") # Spacer
    
    # Custom Sidebar Menu
    if st.button("Single Variable Equation", use_container_width=True): 
        st.session_state.main_category = "Single Variable Equation"
    if st.button("System of Linear Equations", use_container_width=True): 
        st.session_state.main_category = "System of Linear Equations"
    if st.button("Approximation", use_container_width=True): 
        st.session_state.main_category = "Approximation"

# --- RIGHT CONTENT PANEL ---
with main_col:
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
