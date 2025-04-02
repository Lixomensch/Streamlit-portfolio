import os
import pickle
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

DATA_DIR = "data"
MODEL_PATH = os.path.join(DATA_DIR, "salary_model.pkl")
CSV_PATH = os.path.join(DATA_DIR, "salary_data.csv")

def load_data():
    """
    Loads the dataset from the CSV file in the 'data' folder.

    If the file does not exist, an error message is displayed and None is returned.

    Returns:
        pd.DataFrame: The dataset if the file exists, otherwise None
    """
    if not os.path.exists(CSV_PATH):
        st.error("⚠️ Dataset not found! Please add the 'salary_data.csv' file to the 'data' folder.")
        return None
    return pd.read_csv(CSV_PATH)

def train_model(df):
    """
    Trains a linear regression model to predict future salaries based on experience and current salary.

    If a pre-trained model exists at the specified path, it is loaded and returned.
    Otherwise, a new model is trained with the provided data and saved to the file system.

    Args:
        df (pd.DataFrame): DataFrame containing the dataset with 'Experience_Years', 'Current_Salary', and 'Future_Salary' columns.

    Returns:
        LinearRegression: The trained linear regression model.
    """
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)

    os.makedirs(DATA_DIR, exist_ok=True)

    X = df[["Experience_Years", "Current_Salary"]]
    y = df["Future_Salary"]

    model = LinearRegression()
    model.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    return model

def show():
    """
    Displays a Streamlit app with a title, a sidebar for user input, and a prediction of a future salary based on the input data.

    The app first loads the dataset from a CSV file and trains a linear regression model to predict future salaries based on experience and current salary.

    The user can input their years of experience and current salary in the sidebar, and the app will display the predicted future salary and a comparison with the actual data from the dataset.

    If the dataset file is not found, an error message is displayed and the app exits early.

    """
    st.title("💼 Future Salary Prediction with Machine Learning")

    df = load_data()
    if df is None:
        return

    model = train_model(df)

    st.sidebar.header("🔢 Enter Your Data")
    experience_years = st.sidebar.number_input("Years of Experience", min_value=0, max_value=50, value=5, step=1)
    current_salary = st.sidebar.number_input("Current Salary ($)", min_value=1000, max_value=50000, value=5000, step=500)

    input_data = np.array([[experience_years, current_salary]])
    prediction = model.predict(input_data)[0]

    st.subheader("📈 Estimated Future Salary")
    st.write(f"💰 $ {prediction:,.2f}")

    st.subheader("📊 Comparison with Dataset")
    fig, ax = plt.subplots()
    ax.scatter(df["Experience_Years"], df["Future_Salary"], color="blue", label="Actual Data")
    ax.scatter(experience_years, prediction, color="red", label="Prediction", marker="x", s=100)
    ax.set_xlabel("Years of Experience")
    ax.set_ylabel("Future Salary ($)")
    ax.legend()
    st.pyplot(fig)
