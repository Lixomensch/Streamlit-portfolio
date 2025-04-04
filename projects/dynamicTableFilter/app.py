import streamlit as st
import pandas as pd
import os

def load_data():
    """Loads data from a CSV file located in the 'data' directory.

    Returns:
        pd.DataFrame: The DataFrame containing the data from the CSV file.
        If the file is not found, an error message is displayed and an
        empty DataFrame is returned.
    """
    file_path = os.path.join('data', 'example_data.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        st.error("Arquivo CSV não encontrado na pasta 'data'.")
        return pd.DataFrame()

def show():
    """
    Displays an interactive table with filters by city, category, price range, and quantity range.

    The user can select one or more cities, categories, and a price and quantity range to filter the data.
    The filtered data is then displayed in a table, along with summary statistics.

    If the data file is not found, an error message is displayed and an empty DataFrame is returned.
    """
    st.title("📊 Dynamic Table Filter")
    
    df = load_data()
    
    if df.empty:
        return
    
    st.sidebar.header("Filters")
    
    selected_cities = st.sidebar.multiselect("Select City:", options=df['City'].unique(), default=df['City'].unique())
    
    selected_categories = st.sidebar.multiselect("Select Category:", options=df['Category'].unique(), default=df['Category'].unique())
    
    price_range = st.sidebar.slider("Select Price Range:", int(df['Price'].min()), int(df['Price'].max()), (int(df['Price'].min()), int(df['Price'].max())))
    
    quantity_range = st.sidebar.slider("Select Quantity Range:", int(df['Quantity'].min()), int(df['Quantity'].max()), (int(df['Quantity'].min()), int(df['Quantity'].max())))
    
    filtered_df = df[(df['City'].isin(selected_cities)) &
                     (df['Category'].isin(selected_categories)) &
                     (df['Price'].between(price_range[0], price_range[1])) &
                     (df['Quantity'].between(quantity_range[0], quantity_range[1]))]
    
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    st.subheader("Summary Statistics")
    st.write(filtered_df.describe())
