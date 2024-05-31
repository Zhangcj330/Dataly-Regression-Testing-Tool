import streamlit as st
from core import DatalyCompare
import pandas as pd

st.set_page_config(
    page_title="Dataly Regression Test",
    page_icon="👋",
)

@st.cache_data
def read_data(file):
    """Reads data from an uploaded file based on its extension."""
    if file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    elif file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return None

col1, col2 = st.columns([5, 2])
with col1:
    st.title("Dataly Regression Test")
with col2:
    st.write("")
    st.image("Dataly Full Colour Logo.png", width=180)

st.divider()

st.write("Upload your original and new files for comparison.")
col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Upload your original file", key=1, type=['csv', 'xlsx'])
with col2:
    file2 = st.file_uploader("Upload your new file", key=2, type=['csv', 'xlsx'])

if file1 and file2:
    df1 = read_data(file1)
    df2 = read_data(file2)
    column_names = df1.columns.tolist()
    join_columns = st.multiselect("Choose your unique identifiers", column_names)

    if not join_columns:
        st.warning("Please select at least one unique identifier.")
        st.divider()

    col1, col2, col3, col4= st.columns([2, 1, 1, 1])
    with col2:
        compare_button = st.button("Compare")

    if compare_button:
        compare = DatalyCompare(
            df1,
            df2,
            join_columns=join_columns, 
            abs_tol=0.0001,
            rel_tol=0,
            df1_name="Original",
            df2_name="New"
        )
        # Store the regression report in the session state
        st.session_state['regression_report'] = compare.Regression_report()

        # Generate mismatch DataFrame
        st.session_state['mismatch_df'] = compare.all_mismatch(ignore_matching_cols=True)
        

    if 'mismatch_df' in st.session_state:
        csv_data = st.session_state['mismatch_df'].to_csv().encode("utf-8")
        with col4:
            st.download_button(
                label="Download",
                data=csv_data,
                file_name='sample_data.csv',
                mime='text/csv',
            )
        # Display the regression report from the session state if it exists
    if 'regression_report' in st.session_state:
        st.code(st.session_state['regression_report'], language='text')

else:
    join_columns = st.multiselect("Choose your unique identifiers", [])
    st.divider()
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        compare_button = st.button("Compare")
    if compare_button:
        st.warning("Please upload both files to enable comparison.")
    

# css = '''
# <style>
#     [data-testid='stFileUploader'] {
#         width: 325px;
#         height: 250px; 
#         display: grid;
#         flex-direction: column; 
#         justify-content: flex-end; 
#     }
#     [data-testid='stFileUploader'] section {
#         padding: 30px;
#         height: 100%; 
#         display: grid;
#     }
#     button {
#     height: auto;
#     width: auto ;
#     padding-top: 10px !important;
#     padding-bottom: 10px !important;
#     }   
# </style>
# '''

# st.markdown(css, unsafe_allow_html=True)