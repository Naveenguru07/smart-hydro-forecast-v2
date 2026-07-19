import streamlit as st
import joblib
import pandas as pd

# Load trained model
model = joblib.load("hydro_power_model.pkl")

st.title("Smart Hydro Forecast")
st.subheader("Hydroelectric Power Generation Prediction")

st.write("Enter the following values:")

rainfall = st.number_input("Rainfall (mm)", min_value=0.0)
temperature = st.number_input("Temperature (°C)", min_value=0.0)
humidity = st.number_input("Humidity (%)", min_value=0.0)
evaporation = st.number_input("Evaporation Loss (mm)", min_value=0.0)
water_level = st.number_input("Water Level (m)", min_value=0.0)
inflow = st.number_input("Inflow (cumecs)", min_value=0.0)
outflow = st.number_input("Outflow (cumecs)", min_value=0.0)
storage = st.number_input("Reservoir Storage (%)", min_value=0.0)

year = st.number_input("Year", value=2024)
month = st.number_input("Month", min_value=1, max_value=12, value=1)
day = st.number_input("Day", min_value=1, max_value=31, value=1)

if st.button("Predict Power Generation"):

    input_data = pd.DataFrame([[
        rainfall,
        temperature,
        humidity,
        evaporation,
        water_level,
        inflow,
        outflow,
        storage,
        year,
        month,
        day
    ]], columns=[
        "Rainfall (mm)",
        "Temperature (C)",
        "Humidity (%)",
        "Evaporation Loss (mm)",
        "Water Level (m)",
        "Inflow (cumecs)",
        "Outflow (cumecs)",
        "Reservoir Storage (%)",
        "Year",
        "Month",
        "Day"
    ])

    prediction = model.predict(input_data)

    st.success(f"Predicted Power Generation: {prediction[0]:.2f} MW")