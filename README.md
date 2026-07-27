# 💧 Smart Hydro Forecast

## 🌊 AI Powered Hydroelectric Power Generation Prediction System

Smart Hydro Forecast is a Machine Learning-based web application that predicts hydroelectric power generation using live weather data and reservoir parameters. The system integrates the OpenWeather API with a trained ML model to provide real-time predictions through an interactive Streamlit dashboard.

---

## 🚀 Features

- 🌦 Live Weather Data using OpenWeather API
- 🤖 Machine Learning Power Prediction
- 📍 Interactive City Map
- ⚡ Power Generation Gauge Meter
- 🌊 Reservoir Status (Safe / Moderate / Critical)
- 🤖 AI Recommendation System
- 📊 Interactive Bar Chart
- 🥧 Pie Chart Visualization
- 📈 Prediction Trend Graph
- 📜 Prediction History
- 📥 Export Prediction History (CSV)

---

## 🛠 Technologies Used

- Python
- Streamlit
- Scikit-learn
- Pandas
- Plotly
- Joblib
- Requests
- OpenWeather API

---

## 📂 Project Structure

```
Smart-Hydro-Forecast
│── app.py
│── weather.py
│── hydro_power_model.pkl
│── train_model.py
│── requirements.txt
│── README.md
│── data/
│   └── hydro_power.csv
```

---

## ⚙ Installation

```bash
git clone https://github.com/Naveenguru07/smart-hydro-forecast-v2.git
cd smart-hydro-forecast-v2
pip install -r requirements.txt
streamlit run app.py
```

---

## 📊 Input Parameters

- Rainfall (mm)
- Temperature (°C)
- Humidity (%)
- Evaporation Loss (mm)
- Water Level (m)
- Inflow (cumecs)
- Outflow (cumecs)
- Reservoir Storage (%)
- Year
- Month
- Day

---

## 🎯 Output

- Predicted Hydroelectric Power Generation (MW)
- Reservoir Status
- AI Recommendations
- Interactive Visualizations
- Prediction History
- CSV Export

---

## 🌐 Live Demo

**Streamlit App:**  
https://smart-hydro-forecast-ai.streamlit.app

---

## 👨‍💻 Developer

**TEAM PROJECT**

B.Tech Information Technology

Nehru Institute of Engineering and Technology

---

## 📜 License

This project is developed for educational and academic purposes.
