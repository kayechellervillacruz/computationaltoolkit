import streamlit as st
import numpy as np
import pandas as pd
from utils import format_matrix

def create_interactive_matrix(name, rows, cols):
    st.markdown(f"<span style='color:#8E8E8E'>Matrix {name}</span>", unsafe_allow_html=True)
    df = pd.DataFrame(np.zeros((rows, cols)))
    return st.data_editor(df, key=f"matrix_{name}_{rows}x{cols}", num_rows="fixed")

def matrix_ui(operation):
    col_in, col_out = st.columns([1, 1], gap="large")

    with col_in:
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                r_a = st.number_input("Matrix A Rows", min_value=1, value=2, key="ra")
                c_a = st.number_input("Matrix A Cols", min_value=1, value=2, key="ca")
                df_A = create_interactive_matrix("A", r_a, c_a)
            
            with c2:
                if operation in ["addition", "subtraction"]:
                    r_b, c_b = r_a, c_a
                    st.text_input("Matrix B Rows", value=r_b, disabled=True)
                    st.text_input("Matrix B Cols", value=c_b, disabled=True)
                elif operation == "multiplication":
                    r_b = c_a
                    st.text_input("Matrix B Rows", value=r_b, disabled=True)
                    c_b = st.number_input("Matrix B Cols", min_value=1, value=2, key="cb")
                df_B = create_interactive_matrix("B", r_b, c_b)

            calc_btn = st.button(f"Calculate {operation.capitalize()}", type="primary", use_container_width=True)

    if calc_btn:
        with col_out:
            with st.container(border=True):
                st.markdown("<span style='color:#8E8E8E'>Resulting Matrix:</span>", unsafe_allow_html=True)
                A = df_A.to_numpy()
                B = df_B.to_numpy()
                try:
                    if operation == "addition": C = A + B
                    elif operation == "subtraction": C = A - B
                    elif operation == "multiplication": C = np.dot(A, B)
                    st.dataframe(pd.DataFrame(format_matrix(C)), use_container_width=True)
                    st.success("Matrix calculated successfully.")
                except Exception as e:
                    st.error(f"Error computing matrix: {e}")
