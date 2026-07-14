import streamlit as st
import os
from utils import render_custom_tabs, load_css # Ensure load_css is in your utils or kept here

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
# Ensure style.css is in the same directory as app.py
try:
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass 

# --- STATE INITIALIZATION ---
if "main_category" not in st.session_state:
    st.session_state.main_category = "Single Variable Equation"
if "active_method" not in st.session_state:
    st.session_state.active_method = "Bisection"

# Helper to switch categories and reset sub-tabs
def switch_category(cat, default_method):
    st.session_state.main_category = cat
    st.session_state.active_method = default_method
    st.rerun()

# --- MAIN LAYOUT ---
nav_col, main_col = st.columns([1, 4], gap="large")

# --- LEFT NAVIGATION PANEL ---
with nav_col:
    # Logo Area
    logo_path = os.path.join("assets", "ComputationalLOGO.png")
    
    if os.path.exists(logo_path):
        # Shows the image if you created the folder and added the file
        st.image(logo_path, use_container_width=True)
    else:
        # Fallback text if the image is missing
        st.markdown(
            "<h3 style='color: white; margin-top:0;'>Computational<br><span style='color: #d4ff00;'>Toolkit</span></h3>", 
            unsafe_allow_html=True
        )
    st.write("") # Spacer
    
# Navigation Categories
    categories = ["Single Variable Equation", "System of Linear Equations", "Approximation"]
    
    for cat in categories:
        is_active = st.session_state.main_category == cat
        btn_type = "primary" if is_active else "secondary"
        
        if st.button(cat, use_container_width=True, type=btn_type):
            st.session_state.main_category = cat
            # Reset active tab when switching category
            if cat == "Single Variable Equation": st.session_state.active_method = "Bisection"
            elif cat == "System of Linear Equations": st.session_state.active_method = "Addition"
            elif cat == "Approximation": st.session_state.active_method = "Least Squares"
            st.rerun()

# --- RIGHT CONTENT PANEL ---
with main_col:
    # Routing Logic using Custom Tabs
    if st.session_state.main_category == "Single Variable Equation":
        methods = ["Bisection", "Linear Interpolation", "Method of Secants", "Newton's Method"]
        render_custom_tabs(methods, "active_method")
        
        if st.session_state.active_method == "Bisection": bisection_ui()
        elif st.session_state.active_method == "Linear Interpolation": linear_interpolation_ui()
        elif st.session_state.active_method == "Method of Secants": secants_ui()
        elif st.session_state.active_method == "Newton's Method": newtons_ui()

    elif st.session_state.main_category == "System of Linear Equations":
        methods = ["Addition", "Subtraction", "Multiplication", "Gaussian Elimination"]
        render_custom_tabs(methods, "active_method")
        
        if st.session_state.active_method == "Addition": matrix_ui("addition")
        elif st.session_state.active_method == "Subtraction": matrix_ui("subtraction")
        elif st.session_state.active_method == "Multiplication": matrix_ui("multiplication")
        elif st.session_state.active_method == "Gaussian Elimination": gaussian_elimination_ui()

    elif st.session_state.main_category == "Approximation":
        methods = ["Least Squares", "Cubic Splines", "Principal Component Analysis"]
        render_custom_tabs(methods, "active_method")
        
        if st.session_state.active_method == "Least Squares": least_squares_ui()
        elif st.session_state.active_method == "Cubic Splines": cubic_splines_ui()
        elif st.session_state.active_method == "Principal Component Analysis": pca_ui()
