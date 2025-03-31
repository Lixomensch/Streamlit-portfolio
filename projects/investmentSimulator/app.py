import streamlit as st
import pandas as pd
import plotly.express as px

def calculate_compound_interest_daily(principal, rate, years):
    """Calculates daily compound interest growth over time."""
    days = years * 365
    daily_rate = rate / 365  # Convert annual rate to daily rate
    amounts = [principal * (1 + daily_rate) ** day for day in range(days + 1)]
    return amounts, list(range(days + 1))

def show():
    st.title("📈 Investment Growth Simulator")
    
    # User Inputs
    initial_amount = st.number_input("Initial Investment Amount ($):", min_value=100.0, value=1000.0, step=100.0)
    annual_rate = st.slider("Annual Interest Rate (%):", min_value=1.0, max_value=20.0, value=5.0, step=0.1) / 100
    years = st.selectbox("Investment Period (Years):", options=list(range(1, 31)), index=4)
    
    # Calculate Daily Compound Interest Growth
    growth_data, days = calculate_compound_interest_daily(initial_amount, annual_rate, years)
    
    # Create DataFrame for Plotting
    df = pd.DataFrame({"Day": days, "Investment Value": growth_data})
    
    # Display Results
    st.subheader("Investment Growth Over Time (Daily)")
    fig = px.line(df, x="Day", y="Investment Value", markers=False, title="Daily Investment Growth Projection")
    st.plotly_chart(fig)
    
    # Final Amount
    st.subheader("Final Investment Value")
    st.write(f"💰 After {years} years, your investment will be worth **${growth_data[-1]:,.2f}**.")
