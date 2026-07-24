import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
from weather import get_weather
from datetime import datetime

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(90deg,#00b4db,#0083b0);
    color: white;
    border-radius: 12px;
    height: 55px;
    font-size:18px;
    font-weight:bold;
    border:none;
}

.stButton>button:hover{
    background: linear-gradient(90deg,#0083b0,#00b4db);
}

div[data-testid="metric-container"]{
    background:#1b263b;
    border-radius:15px;
    padding:20px;
    border:1px solid #3d5a80;
    box-shadow:0 0 10px rgba(0,180,219,.3);
}

h1{
    text-align:center;
    color:#4fc3f7;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.title("💧 Smart Hydro")

st.sidebar.info("""
AI Powered Hydroelectric
Power Prediction System

Version 2.0
""")

st.sidebar.success("✔ Live Weather API")
st.sidebar.success("✔ AI Prediction")
st.sidebar.success("✔ Interactive Map")
st.sidebar.success("✔ Prediction History")

# Load trained model
model = joblib.load("hydro_power_model.pkl")

st.set_page_config(
    page_title="Smart Hydro Forecast",
    page_icon="💧",
    layout="wide"
)

st.markdown("""
<div style="
background: linear-gradient(90deg,#0f2027,#203a43,#2c5364);
padding:30px;
border-radius:20px;
text-align:center;
box-shadow:0px 0px 20px rgba(0,180,255,.3);
">

<h1 style="color:white;font-size:48px;">
💧 Smart Hydro Forecast
</h1>

<h4 style="color:#B0E0E6;">
AI Powered Hydroelectric Power Generation Prediction System
</h4>

</div>
""", unsafe_allow_html=True)
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.info("🌦 Live Weather")

with col2:
    st.success("⚡ AI Prediction")

with col3:
    st.warning("🗺 Interactive Map")

with col4:
    st.error("📊 Analytics")

st.write("")
if "history" not in st.session_state:
    st.session_state.history = []
city = st.text_input("Enter City", "Coimbatore")
if "weather" not in st.session_state:
    st.session_state.weather = None

if st.button("Get Live Weather"):

    weather = get_weather(city)

    if weather:
        st.session_state.weather = weather
        st.success("✅ Live Weather Data Loaded Successfully!")

    else:
        st.session_state.weather = None
        st.error("❌ City not found!")
st.subheader("Hydroelectric Power Generation Prediction")

st.write("Enter the following values:")

# Auto-filled from Live Weather API
if st.session_state.weather:
    rainfall = st.session_state.weather["rainfall"]
    temperature = st.session_state.weather["temperature"]
    humidity = st.session_state.weather["humidity"]
else:
    rainfall = 0.0
    temperature = 0.0
    humidity = 0.0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🌧 Rainfall",
        value=f"{rainfall} mm"
    )

with col2:
    st.metric(
        label="🌡 Temperature",
        value=f"{temperature} °C"
    )

with col3:
    st.metric(
        label="💧 Humidity",
        value=f"{humidity} %"
    )
# Show city on map
if st.session_state.weather:

    st.subheader("📍 Selected City Location")

    map_data = pd.DataFrame({
        "lat": [st.session_state.weather["lat"]],
        "lon": [st.session_state.weather["lon"]]
    })

    st.write(map_data)   # Debug (optional)

    st.map(map_data)

    st.write(f"Latitude : {st.session_state.weather['lat']}")
    st.write(f"Longitude : {st.session_state.weather['lon']}")
evaporation = st.number_input("Evaporation Loss (mm)", min_value=0.0)
water_level = st.number_input("Water Level (m)", min_value=0.0)
inflow = st.number_input("Inflow (cumecs)", min_value=0.0)
outflow = st.number_input("Outflow (cumecs)", min_value=0.0)
storage = st.number_input("Reservoir Storage (%)", min_value=0.0)

year = st.number_input("Year", value=2024)
month = st.number_input("Month", min_value=1, max_value=12, value=1)
day = st.number_input("Day", min_value=1, max_value=31, value=1)

left, center, right = st.columns([1,2,1])

with center:
    predict = st.button(
        "⚡ Predict Power Generation",
        use_container_width=True
    )

if predict:

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
    st.session_state.prediction = prediction[0]
    st.session_state.history.append({
    "Date & Time": datetime.now().strftime("%d-%m-%Y %H:%M"),
    "City": city,
    "Prediction (MW)": round(prediction[0], 2)
})

    st.markdown("## ⚡ Prediction Result")

if "prediction" in st.session_state:

    st.markdown(f"""
    <div style="
    background: linear-gradient(90deg,#11998e,#38ef7d);
    padding:30px;
    border-radius:20px;
    text-align:center;
    box-shadow:0px 0px 20px rgba(0,255,150,.4);
    margin-top:20px;
    margin-bottom:20px;
    ">

    <h2 style="color:white;">⚡ Predicted Power Generation</h2>

    <h1 style="
    color:white;
    font-size:60px;
    margin-top:15px;
    ">
    {st.session_state.prediction:.2f} MW
    </h1>

    <h4 style="color:white;">
    ✅ AI Prediction Completed Successfully
    </h4>

    </div>
    """, unsafe_allow_html=True)

    # Gauge Meter
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=st.session_state.prediction,

        title={"text": "⚡ Power Generation (MW)"},

        gauge={
            "axis": {"range": [0, 300]},

            "bar": {"color": "#00E676"},

            "steps": [
                {"range": [0, 100], "color": "#4CAF50"},
                {"range": [100, 200], "color": "#FFC107"},
                {"range": [200, 300], "color": "#F44336"}
            ]
        }
    ))

    fig.update_layout(
        height=400,
        paper_bgcolor="#0E1117",
        font={"color": "white", "size": 20}
    )

    st.plotly_chart(fig, use_container_width=True)
st.subheader("📊 Prediction History")

if st.session_state.history:
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)
else:
    st.info("No predictions yet.")

    # -----------------------------
# Prediction History Line Chart
# -----------------------------
if len(st.session_state.history) > 0:

    st.subheader("📈 Prediction Trend")

    history_df = pd.DataFrame(st.session_state.history)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=history_df["Date & Time"],
        y=history_df["Prediction (MW)"],
        mode="lines+markers",
        line=dict(color="#00E5FF", width=4),
        marker=dict(size=10),
        name="Prediction"
    ))

    fig.update_layout(
        title="Hydroelectric Power Prediction Trend",
        xaxis_title="Prediction Time",
        yaxis_title="Power Generation (MW)",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="white"),
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)


# Show chart only after prediction
# Interactive Bar Chart
if "prediction" in st.session_state:

    chart_data = {
        "Rainfall": rainfall,
        "Temperature": temperature,
        "Humidity": humidity,
        "Evaporation": evaporation,
        "Water Level": water_level,
        "Inflow": inflow,
        "Outflow": outflow,
        "Storage": storage,
        "Prediction": st.session_state.prediction
    }

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=list(chart_data.keys()),
            y=list(chart_data.values()),
            marker_color=[
                "#4FC3F7",
                "#FF9800",
                "#00E676",
                "#9C27B0",
                "#F44336",
                "#03A9F4",
                "#FFC107",
                "#8BC34A",
                "#00BCD4"
            ]
        )
    )

    fig.update_layout(
        title="📊 Input Parameters vs Predicted Power",
        xaxis_title="Parameters",
        yaxis_title="Values",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="white"),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
    st.subheader("🥧 Input Parameter Distribution")

pie_labels = [
    "Rainfall",
    "Temperature",
    "Humidity",
    "Evaporation",
    "Water Level",
    "Inflow",
    "Outflow",
    "Storage"
]

pie_values = [
    rainfall,
    temperature,
    humidity,
    evaporation,
    water_level,
    inflow,
    outflow,
    storage
]

pie_fig = go.Figure(
    data=[
        go.Pie(
            labels=pie_labels,
            values=pie_values,
            hole=0.45,
            textinfo="label+percent"
        )
    ]
)

pie_fig.update_layout(
    title="🥧 Input Parameter Distribution",
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="white"),
    height=500
)

st.plotly_chart(pie_fig, use_container_width=True)

# -----------------------------
# Dam Water Status
# -----------------------------
st.subheader("🌊 Reservoir Status")

if storage >= 70:
    status = "🟢 SAFE"
    color = "#2ecc71"
    message = "Reservoir water level is sufficient for power generation."

elif storage >= 40:
    status = "🟡 MODERATE"
    color = "#f1c40f"
    message = "Reservoir level is moderate. Monitor water usage."

else:
    status = "🔴 CRITICAL"
    color = "#e74c3c"
    message = "Reservoir water level is low. Immediate attention required."

st.markdown(f"""
<div style="
background:{color};
padding:20px;
border-radius:15px;
text-align:center;
box-shadow:0px 0px 15px rgba(255,255,255,0.2);
margin-bottom:20px;
">

<h2 style="color:white;">{status}</h2>

<p style="color:white;font-size:18px;">
{message}
</p>

</div>
""", unsafe_allow_html=True)

# -----------------------------
# AI Recommendation
# -----------------------------
st.subheader("🤖 AI Recommendation")

recommendations = []

if storage >= 70:
    recommendations.append("✅ Reservoir storage is sufficient for continuous power generation.")
elif storage >= 40:
    recommendations.append("⚠ Reservoir level is moderate. Monitor water usage regularly.")
else:
    recommendations.append("🚨 Increase water conservation and reduce power generation.")

if inflow < outflow:
    recommendations.append("💧 Outflow is higher than inflow. Monitor reservoir balance.")
else:
    recommendations.append("🌊 Inflow is adequate for stable reservoir operation.")

if rainfall > 50:
    recommendations.append("🌧 Heavy rainfall detected. Water availability is expected to improve.")
elif rainfall > 10:
    recommendations.append("🌦 Moderate rainfall supports reservoir recharge.")
else:
    recommendations.append("☀ Low rainfall detected. Monitor future weather conditions.")

for rec in recommendations:
    st.success(rec)