import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    """
    Displays a data analysis dashboard with a file uploader, data preview, and
    statistics for a selected numeric column (mean, median, standard deviation).
    Also displays a histogram of the selected column.

    If the uploaded file does not contain any numeric columns, a warning message
    is displayed. If no file is uploaded, an information message is displayed.
    """
    st.title("📊 Data Analysis Dashboard")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader("Data Preview")
        st.dataframe(df.head())

        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_columns:
            column = st.selectbox("Select a numeric column", numeric_columns)
            mean_value = df[column].mean()
            median_value = df[column].median()
            std_value = df[column].std()

            st.markdown(f"**Mean:** {mean_value:.2f}")
            st.markdown(f"**Median:** {median_value:.2f}")
            st.markdown(f"**Standard Deviation:** {std_value:.2f}")

            fig = px.histogram(df, x=column, nbins=30, title=f"Distribution of {column}")
            st.plotly_chart(fig)
        else:
            st.warning("The file does not contain numeric columns.")
    else:
        st.info("Please upload a CSV file to start the analysis.")
