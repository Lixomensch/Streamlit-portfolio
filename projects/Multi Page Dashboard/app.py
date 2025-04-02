import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data(uploaded_file):
    """
    Loads data from an uploaded CSV file and stores it in the session state.

    Args:
        uploaded_file: A file-like object representing the uploaded CSV file.

    Returns:
        pd.DataFrame: The DataFrame containing the data from the uploaded CSV file.
    """
    df = pd.read_csv(uploaded_file)
    st.session_state["data"] = df
    return df

@st.cache_data
def compute_statistics(df):
    """
    Computes summary statistics of a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.

    Returns:
        pd.DataFrame: The DataFrame containing the summary statistics.
    """
    return df.describe()

def page1():
        """
        Displays the first page of the app with a file uploader, data preview, and information messages.

        The user can upload a CSV file, and if the file is valid, the data is stored in session_state and
        the app displays a success message. If the user has previously uploaded a file, the app displays
        an information message and uses the previously uploaded data. If no file is uploaded, the app
        displays a warning message and does not display the data preview.

        The page also displays the first few rows of the uploaded data as a data preview.
        """
        st.title("📂 Upload and View Data")
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
        
        if uploaded_file is not None:
            df = load_data(uploaded_file)
            st.success("✅ Data successfully uploaded!")
        elif "data" in st.session_state:
            df = st.session_state["data"]
            st.info("ℹ️ Using previously uploaded data.")
        else:
            st.warning("⚠️ No file uploaded yet.")
            df = None

        if df is not None:
            st.write("### Data Preview")
            st.dataframe(df.head())
        
def page2():
    """
    Displays a statistical analysis page with a data summary and a distribution plot for a selected numeric column.

    If the dataset is available, the user can select a numeric column to visualize in a histogram.
    If the dataset contains less than one numeric column, a warning message is displayed. If no dataset is available, a separate warning message is displayed.
    """
    st.title("📊 Statistical Analysis")
    if "data" in st.session_state:
        df = st.session_state["data"]
        stats = compute_statistics(df)
        st.write("### Data Summary")
        st.dataframe(stats)

        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        if numeric_cols:
            column = st.selectbox("Select a column for distribution plot:", numeric_cols)
            fig = px.histogram(df, x=column, nbins=30, title=f"Distribution of {column}")
            st.plotly_chart(fig)
    else:
        st.warning("⚠️ No data available. Please upload a CSV on the first page.")
        
def page3():
    """
    Displays an interactive chart page with a scatter plot of two numeric columns.

    If the dataset is available, the user can select two numeric columns to visualize
    in a scatter plot. If the dataset contains less than two numeric columns, a warning
    message is displayed. If no dataset is available, a separate warning message is
    displayed.
    """
    st.title("📈 Interactive Charts")
    if "data" in st.session_state:
        df = st.session_state["data"]
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        
        if len(numeric_cols) >= 2:
            x_axis = st.selectbox("Select X-axis:", numeric_cols, index=0)
            y_axis = st.selectbox("Select Y-axis:", numeric_cols, index=1)
            
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
            st.plotly_chart(fig)
        else:
            st.warning("⚠️ The dataset must contain at least two numeric columns for visualization.")
    else:
        st.warning("⚠️ No data available. Please upload a CSV on the first page.")
    

def show():
    """
    Displays a multi-page dashboard with a sidebar for navigation.

    The dashboard has three pages: a data upload and preview page, a statistical analysis page,
    and an interactive charts page. The user can navigate between these pages using the sidebar
    radio buttons.

    Each page is defined by a separate function, and they are called based on the user's selection
    in the sidebar.
    """
    st.sidebar.title("📌 Navigation")
    page = st.sidebar.radio("Select a Page:", ["Upload & View Data", "Statistical Analysis", "Interactive Charts"])

    if page == "Upload & View Data":
        page1()
    elif page == "Statistical Analysis":
        page2()
    elif page == "Interactive Charts":
        page3()
