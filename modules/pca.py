# modules/pca.py
import streamlit as st
import numpy as np
import pandas as pd
from utils import format_matrix
from modules.matrix import create_interactive_matrix

def pca_ui():
    st.header("Principal Component Analysis")
    st.markdown("Analyze patterns in data dimensionality by extracting principal components.")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        r = st.number_input("Number of samples (rows)", min_value=2, value=4)
    with col2:
        c = st.number_input("Number of features (columns)", min_value=1, value=3)
    
    # FIX: Added the 4th argument "pca" to uniquely identify these widgets
    df_data = create_interactive_matrix("Data", r, c, "pca")
    st.divider()

    if st.button("Calculate PCA", type="primary"):
        try:
            X = df_data.to_numpy()
            mu = np.mean(X, axis=0)
            Xc = X - mu
            C = np.cov(Xc, rowvar=False)
            eigenvalues, V = np.linalg.eigh(C)
            D = np.diag(eigenvalues)
            Y = np.dot(Xc, V)
            
            st.subheader("Results")
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**Centered Data:**")
                st.dataframe(pd.DataFrame(format_matrix(Xc)), use_container_width=True)
                st.write("**Covariance Matrix:**")
                st.dataframe(pd.DataFrame(format_matrix(C)), use_container_width=True)
                st.write("**Eigenvalues:**")
                st.dataframe(pd.DataFrame(format_matrix(D)), use_container_width=True)
            with col_b:
                st.write("**Eigenvectors:**")
                st.dataframe(pd.DataFrame(format_matrix(V)), use_container_width=True)
                st.write("**Principal Components:**")
                st.dataframe(pd.DataFrame(format_matrix(Y)), use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
