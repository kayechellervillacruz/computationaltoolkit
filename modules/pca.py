import streamlit as st
import numpy as np
import pandas as pd
from utils import format_matrix
from modules.matrix import create_interactive_matrix

def pca_ui():
    col_in, col_out = st.columns([1, 1], gap="large")

    with col_in:
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1: r = st.number_input("Samples (Rows)", min_value=2, value=4)
            with c2: c = st.number_input("Features (Cols)", min_value=1, value=3)
            
            df_data = create_interactive_matrix("Data", r, c)
            calc_btn = st.button("Calculate PCA", type="primary", use_container_width=True)

    if calc_btn:
        with col_out:
            with st.container(border=True):
                try:
                    X = df_data.to_numpy()
                    mu = np.mean(X, axis=0)
                    Xc = X - mu
                    C = np.cov(Xc, rowvar=False)
                    eigenvalues, V = np.linalg.eigh(C)
                    
                    st.markdown("<span style='color:#8E8E8E'>Principal Components:</span>", unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(format_matrix(np.dot(Xc, V))), use_container_width=True)
                    st.success("PCA Calculated successfully.")
                except Exception as e:
                    st.error(f"Error: {e}")
