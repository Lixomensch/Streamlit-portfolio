import streamlit as st
import pandas as pd
import plotly.express as px

def calculate_compound_interest_daily(principal, rate, years):
    """
    Calculates daily compound interest growth over a specified number of years.

    Args:
        principal (float): The initial amount of money invested.
        rate (float): The annual interest rate (as a decimal).
        years (int): The investment period in years.

    Returns:
        tuple: A tuple containing a list of investment values at each day and a list of corresponding days.
    """
    days = years * 365
    daily_rate = rate / 365
    amounts = [principal * (1 + daily_rate) ** day for day in range(days + 1)]
    return amounts, list(range(days + 1))

def show():
    """
    Displays an investment growth simulator that calculates daily compound interest over time.

    The user can input an initial investment amount, an annual interest rate, and an investment period (in years).

    The output will display the daily investment growth over the specified period, and the final investment value after the specified period.
    """
    st.title("📈 Investment Growth Simulator")
    
    initial_amount = st.number_input("Initial Investment Amount ($):", min_value=100.0, value=1000.0, step=100.0)
    annual_rate = st.slider("Annual Interest Rate (%):", min_value=1.0, max_value=20.0, value=5.0, step=0.1) / 100
    years = st.selectbox("Investment Period (Years):", options=list(range(1, 31)), index=4)

    growth_data, days = calculate_compound_interest_daily(initial_amount, annual_rate, years)

    df = pd.DataFrame({"Day": days, "Investment Value": growth_data})

    st.subheader("Investment Growth Over Time (Daily)")
    fig = px.line(df, x="Day", y="Investment Value", markers=False, title="Daily Investment Growth Projection")
    st.plotly_chart(fig)

    st.subheader("Final Investment Value")
    st.write(f"💰 After {years} years, your investment will be worth **${growth_data[-1]:,.2f}**.")
