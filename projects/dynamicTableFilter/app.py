import streamlit as st
import pandas as pd
import os

def load_data():
    """Carrega o arquivo CSV diretamente da pasta 'data'."""
    file_path = os.path.join('data', 'example_data.csv')  # Substitua 'example_data.csv' pelo nome do seu arquivo
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        st.error("Arquivo CSV não encontrado na pasta 'data'.")
        return pd.DataFrame()  # Retorna um DataFrame vazio se o arquivo não for encontrado

def show():
    st.title("📊 Dynamic Table Filter")
    
    # Carregar os dados do CSV diretamente da pasta 'data'
    df = load_data()
    
    # Se o CSV foi carregado corretamente
    if df.empty:
        return
    
    # Sidebar Filters
    st.sidebar.header("Filters")
    
    # Filter by City
    selected_cities = st.sidebar.multiselect("Select City:", options=df['City'].unique(), default=df['City'].unique())
    
    # Filter by Category
    selected_categories = st.sidebar.multiselect("Select Category:", options=df['Category'].unique(), default=df['Category'].unique())
    
    # Filter by Price Range
    price_range = st.sidebar.slider("Select Price Range:", int(df['Price'].min()), int(df['Price'].max()), (int(df['Price'].min()), int(df['Price'].max())))
    
    # Filter by Quantity Range
    quantity_range = st.sidebar.slider("Select Quantity Range:", int(df['Quantity'].min()), int(df['Quantity'].max()), (int(df['Quantity'].min()), int(df['Quantity'].max())))
    
    # Apply Filters
    filtered_df = df[(df['City'].isin(selected_cities)) &
                     (df['Category'].isin(selected_categories)) &
                     (df['Price'].between(price_range[0], price_range[1])) &
                     (df['Quantity'].between(quantity_range[0], quantity_range[1]))]
    
    # Display Filtered Data
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    # Summary
    st.subheader("Summary Statistics")
    st.write(filtered_df.describe())
