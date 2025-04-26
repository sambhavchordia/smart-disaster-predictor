import streamlit as st
import numpy as np
import joblib
import boto3

# ✅ Must be the first Streamlit command
st.set_page_config(page_title="🌪️ Smart Disaster Predictor", layout="centered")

# ✅ AWS Credentials (For production, use env variables instead of hardcoding)
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

# ✅ Load ML models
flood_rf = joblib.load("models/flood_rf_model.pkl")
flood_lr = joblib.load("models/flood_lr_model.pkl")
earthquake_rf = joblib.load("models/earthquake_rf_model.pkl")
earthquake_lr = joblib.load("models/earthquake_lr_model.pkl")

# ✅ Set up AWS SNS client
sns = boto3.client(
    'sns',
    region_name='',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# ✅ Function to send SMS alert
def send_sns_alert(message, phone_number):
    response = sns.publish(
        PhoneNumber=phone_number,
        Message=message
    )
    return response['MessageId']

# ------------------------
# 🎯 Streamlit UI
# ------------------------

st.title("🌪️ Smart Disaster Risk Prediction System")
st.markdown("Stay prepared, stay safe! 🚑")

phone_number = st.text_input(
    "📱 Enter phone number for alerts (e.g., +917073272899):",
    max_chars=15
)

# Tabs for disasters
tab1, tab2 = st.tabs(["🌊 Flood Risk", "🌍 Earthquake Risk"])

# ------------------------
# 🌊 Flood Risk Tab
# ------------------------
with tab1:
    st.header("🚰 Flood Risk Prediction")
    st.subheader("Enter Environmental Parameters:")

    model_choice_flood = st.selectbox(
        "🤖 Choose Model",
        ["Random Forest", "Logistic Regression"],
        key="flood_model_selectbox"
    )

    rainfall = st.slider("🌧️ Rainfall (mm)", 50, 300, 120)
    river_level = st.slider("🏞️ River Level (m)", 1.0, 10.0, 5.0)
    soil_moisture = st.slider("🌱 Soil Moisture (%)", 30, 100, 60)
    temperature = st.slider("🌡️ Temperature (°C)", 10, 45, 28)

    if st.button("🔍 Predict Flood Risk"):
        with st.spinner('⏳ Predicting flood risk...'):
            input_data = np.array([[rainfall, river_level, soil_moisture, temperature]])
            model = flood_rf if model_choice_flood == "Random Forest" else flood_lr
            result = model.predict(input_data)

            if result[0] == 1:
                st.error("🚨 High Risk of Flood Detected!")
                if phone_number:
                    send_sns_alert("🚨 Flood Alert! Take precautions immediately.", phone_number)
                    st.info("📨 SMS Alert sent successfully!")
                else:
                    st.warning("⚠️ Please enter a valid phone number to receive alerts.")
            else:
                st.success("✅ Low Risk of Flood. Stay safe!")

# ------------------------
# 🌍 Earthquake Risk Tab
# ------------------------
with tab2:
    st.header("🌎 Earthquake Risk Prediction")
    st.subheader("Enter Seismic Parameters:")

    model_choice_eq = st.selectbox(
        "🤖 Choose Model",
        ["Random Forest", "Logistic Regression"],
        key="earthquake_model_selectbox"
    )

    magnitude = st.slider("📏 Magnitude", 3.0, 9.0, 5.5)
    depth = st.slider("🧠 Depth (km)", 1.0, 50.0, 10.0)
    distance = st.slider("📍 Distance to Nearest City (km)", 1, 200, 50)
    population = st.slider("🏘️ Population Density (people/km²)", 100, 15000, 3000)

    if st.button("🔍 Predict Earthquake Risk"):
        with st.spinner('⏳ Predicting earthquake risk...'):
            input_data = np.array([[magnitude, depth, distance, population]])
            model = earthquake_rf if model_choice_eq == "Random Forest" else earthquake_lr
            result = model.predict(input_data)

            if result[0] == 1:
                st.error("🚨 High Risk of Earthquake Detected!")
                if phone_number:
                    send_sns_alert("🚨 Earthquake Alert! Follow safety protocols.", phone_number)
                    st.info("📨 SMS Alert sent successfully!")
                else:
                    st.warning("⚠️ Please enter a valid phone number to receive alerts.")
            else:
                st.success("✅ Low Risk of Earthquake. Stay safe!")

