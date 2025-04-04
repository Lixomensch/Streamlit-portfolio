import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city, country="us"):
    """
    Fetches weather data from the OpenWeatherMap API for a specified city and country.

    Args:
        city (str): The name of the city to fetch weather data for.
        country (str, optional): The country code (default is "us" for the United States).

    Returns:
        dict: A dictionary containing weather data such as temperature, humidity,
              and weather description if the request is successful.
              If the request fails, a dictionary with an error message is returned.
    """
    params = {
        "q": f"{city},{country}",
        "appid": API_KEY,
        "units": "metric",
        "lang": "en"
    }
    
    response = requests.get(URL, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        error_msg = response.json().get("message", "Unknown error")
        return {"error": f"Error {response.status_code}: {error_msg}"}

def show():
    """
    Displays a weather forecast application using Streamlit.

    The application prompts the user to input a city name and country code. Upon confirmation, it fetches
    weather data from the OpenWeatherMap API and displays various weather metrics, such as current
    temperature, minimum and maximum temperatures, humidity, and weather condition description.

    If the API request fails, an error message is displayed. Otherwise, the application shows the weather
    metrics as text and visualizes them using a bar chart.
    """
    st.title("🌤 Weather Forecast")

    city = st.text_input("Enter the city name:", "")
    country = st.text_input("Enter the country code (e.g., 'us' for the United States):", "")

    if st.button("Search"):
        weather_data = get_weather_data(city, country)
        
        if "error" in weather_data:
            st.error(weather_data["error"])
        else:
            st.write(f"### Weather in {weather_data['name']}, {country.upper()}")
            temp = weather_data["main"]["temp"]
            temp_min = weather_data["main"]["temp_min"]
            temp_max = weather_data["main"]["temp_max"]
            humidity = weather_data["main"]["humidity"]
            description = weather_data["weather"][0]["description"].capitalize()
            
            st.metric("🌡 Current Temperature", f"{temp}°C")
            st.metric("📉 Minimum Temperature", f"{temp_min}°C")
            st.metric("📈 Maximum Temperature", f"{temp_max}°C")
            st.metric("💧 Humidity", f"{humidity}%")
            st.write(f"**Condition:** {description}")

            df = pd.DataFrame(
                {"Metric": ["Current Temperature", "Min Temp", "Max Temp", "Humidity"], 
                 "Value": [temp, temp_min, temp_max, humidity]}
            )
            fig = px.bar(df, x="Metric", y="Value", color="Metric", title="Weather Metrics")
            st.plotly_chart(fig)
