import streamlit as st
import numpy as np
import pandas as pd
from utils import format_matrix

def create_interactive_matrix(name, rows, cols, key_suffix):
    st.write(f"**Matrix {name}**")
    df = pd.DataFrame(np.zeros((rows, cols)))
    return st.data_editor(df, key=f"matrix_{name}_{rows}x{cols}_{key_suffix}", num_rows="fixed")

def matrix_ui(operation):
    st.header(f"Matrix {operation.capitalize()}")
    st.markdown("Perform linear algebra operations on dynamically scaled matrices.")
    st.divider()

    col1, col2 = st.columns(2)
    # Using the operation name as a unique key suffix
    with col1:
        r_a = st.number_input("Matrix A Rows", min_value=1, value=2, key=f"ra_{operation}")
        c_a = st.number_input("Matrix A Cols", min_value=1, value=2, key=f"ca_{operation}")
        df_A = create_interactive_matrix("A", r_a, c_a, operation)
    
    with col2:
        if operation in ["addition", "subtraction"]:
            r_b, c_b = r_a, c_a
            st.text_input("Matrix B Rows", value=r_b, disabled=True, key=f"rb_{operation}")
            st.text_input("Matrix B Cols", value=c_b, disabled=True, key=f"cb_{operation}")
        elif operation == "multiplication":
            r_b = c_a
            st.text_input("Matrix B Rows", value=r_b, disabled=True, key=f"rb_{operation}")
            c_b = st.number_input("Matrix B Cols", min_value=1, value=2, key=f"cb_{operation}")
            
        df_B = create_interactive_matrix("B", r_b, c_b, operation)

    st.divider()
    if st.button(f"Calculate {operation.capitalize()}", key=f"btn_{operation}", type="primary"):
        A = df_A.to_numpy()
        B = df_B.to_numpy()
        
        try:
            if operation == "addition": C = A + B
            elif operation == "subtraction": C = A - B
            elif operation == "multiplication": C = np.dot(A, B)
                
            st.success("Resulting matrix:")
            st.dataframe(pd.DataFrame(format_matrix(C)), use_container_width=True)
        except Exception as e:
            st.error(f"Error computing matrix: {e}")
