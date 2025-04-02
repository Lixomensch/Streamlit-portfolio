import streamlit as st
import pandas as pd
import os

def load_data():
    """Loads geographic data from a CSV file located in the 'data' directory.

    Returns:
        pd.DataFrame: The DataFrame containing the geographical data with required
        columns 'latitude', 'longitude', and 'category'. If the file or required
        columns are missing, an error message is displayed and an empty DataFrame
        is returned.
    """
    file_path = os.path.join('data', 'geographic_data.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if {'latitude', 'longitude', 'category'}.issubset(df.columns):
            return df
        else:
            st.error("O arquivo CSV deve conter as colunas: latitude, longitude e category.")
            return pd.DataFrame()
    else:
        st.error("Arquivo CSV não encontrado na pasta 'data'.")
        return pd.DataFrame()

def show():
    """
    Displays an interactive map with geographic data filtered by category.

    The function loads geographic data from a CSV file, and if the data is available, it displays a sidebar 
    with a category filter. The user can select a category to filter the data points shown on the map. 
    The filtered data is then displayed as points on an interactive map, along with a subheader showing 
    the number of points for the selected category.

    If the data file is not found or if the DataFrame is empty, the function exits early.
    """
    st.title("🌍 Interactive Map with Geographic Data")
    
    df = load_data()
    if df.empty:
        return
    
    st.sidebar.header("Filters")
    categories = df['category'].unique()
    selected_category = st.sidebar.selectbox("Select Category:", options=categories)
    
    filtered_df = df[df['category'] == selected_category]
    
    st.subheader(f"Displaying {len(filtered_df)} points for category: {selected_category}")
    st.map(filtered_df[['latitude', 'longitude']])
