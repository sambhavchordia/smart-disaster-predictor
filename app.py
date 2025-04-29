import mysql.connector
import streamlit as st
import numpy as np
import joblib
import boto3
from dotenv import load_dotenv
import os

# Load environment variables (optional, if you store AWS keys in .env)
load_dotenv()

# Load trained models
flood_rf = joblib.load("models/flood_rf_model.pkl")
flood_lr = joblib.load("models/flood_lr_model.pkl")
earthquake_rf = joblib.load("models/earthquake_rf_model.pkl")
earthquake_lr = joblib.load("models/earthquake_lr_model.pkl")

# AWS SNS client setup
sns = boto3.client(
    'sns',
    region_name='ap-south-1',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),         # or hardcode for testing
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

# Function to send alert
def send_sns_alert(message, phone_number):
    response = sns.publish(
        PhoneNumber=phone_number,
        Message=message
    )
    return response['MessageId']

# Function to connect to MySQL RDS database
def connect_to_db():
    db_connection = mysql.connector.connect(
        host="<rds-endpoint>",  # e.g., "smart-disaster-db.cjpd123xyz.us-west-2.rds.amazonaws.com"
        user="<db-username>",  # e.g., "admin"
        password="<db-password>",  # Use the password from RDS setup
        database="disaster_db"
    )
    return db_connection

# Function to save input data into MySQL database
def save_data_to_db(data):
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
    
    # SQL Insert query
    query = "INSERT INTO disaster_data (Rainfall_mm, River_Level_m, Soil_Moisture, Temperature_C, Earthquake_Magnitude, Earthquake_Depth, Phone_Number, Disaster_Type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    
    cursor.execute(query, (
        data['Rainfall_mm'],
        data['River_Level_m'],
        data['Soil_Moisture'],
        data['Temperature_C'],
        data['Earthquake_Magnitude'],
        data['Earthquake_Depth'],
        data['Phone_Number'],
        data['Disaster_Type']
    ))
    
    db_connection.commit()  # Save changes to the database
    cursor.close()
    db_connection.close()

# Streamlit UI Setup
st.set_page_config(page_title="Smart Disaster Predictor", layout="centered")
st.title("🌪️ Smart Disaster Risk Prediction System")

phone_number = st.text_input("Enter phone number for alerts (+91...):")

tab1, tab2 = st.tabs(["🌊 Flood Risk", "🌍 Earthquake Risk"])

# ------------------------
# 🌊 Flood Risk Tab
# ------------------------
with tab1:
    st.header("Flood Input")
    model_choice_flood = st.selectbox("Select Flood Model", ["Random Forest", "Logistic Regression"])

    rainfall = st.slider("Rainfall (mm)", 50, 300, 120)
    river_level = st.slider("River Level (m)", 1.0, 10.0, 5.0)
    soil_moisture = st.slider("Soil Moisture (%)", 30, 100, 60)
    temperature = st.slider("Temperature (°C)", 10, 45, 28)

    if st.button("Predict Flood Risk"):
        input_data = np.array([[rainfall, river_level, soil_moisture, temperature]])
        model = flood_rf if model_choice_flood == "Random Forest" else flood_lr
        result = model.predict(input_data)

        if result[0] == 1:
            st.error("🚨 High Risk of Flood Detected!")
            if phone_number:
                send_sns_alert("🚨 Flood Alert! Take precautions immediately.", phone_number)
                st.info("SMS Alert sent!")
            else:
                st.warning("Please enter a phone number to receive alerts.")
        else:
            st.success("✅ Low Flood Risk")

        # Save the input data to MySQL database
        input_data_dict = {
            'Rainfall_mm': rainfall,
            'River_Level_m': river_level,
            'Soil_Moisture': soil_moisture,
            'Temperature_C': temperature,
            'Earthquake_Magnitude': None,  # Not used for flood
            'Earthquake_Depth': None,  # Not used for flood
            'Phone_Number': phone_number,
            'Disaster_Type': 'Flood'
        }
        save_data_to_db(input_data_dict)

# ------------------------
# 🌍 Earthquake Risk Tab
# ------------------------
with tab2:
    st.header("Earthquake Input")
    model_choice_eq = st.selectbox("Select Earthquake Model", ["Random Forest", "Logistic Regression"])

    magnitude = st.slider("Magnitude", 3.0, 9.0, 5.5)
    depth = st.slider("Depth (km)", 1.0, 50.0, 10.0)
    distance = st.slider("Distance to City (km)", 1, 200, 50)
    population = st.slider("Population Density", 100, 15000, 3000)

    if st.button("Predict Earthquake Risk"):
        input_data = np.array([[magnitude, depth, distance, population]])
        model = earthquake_rf if model_choice_eq == "Random Forest" else earthquake_lr
        result = model.predict(input_data)

        if result[0] == 1:
            st.error("🚨 High Risk of Earthquake Detected!")
            if phone_number:
                send_sns_alert("🚨 Earthquake Alert! Stay safe and follow safety protocols.", phone_number)
                st.info("SMS Alert sent!")
            else:
                st.warning("Please enter a phone number to receive alerts.")
        else:
            st.success("✅ Low Earthquake Risk")

        # Save the input data to MySQL database
        input_data_dict = {
            'Rainfall_mm': None,  # Not used for earthquake
            'River_Level_m': None,  # Not used for earthquake
            'Soil_Moisture': None,  # Not used for earthquake
            'Temperature_C': None,  # Not used for earthquake
            'Earthquake_Magnitude': magnitude,
            'Earthquake_Depth': depth,
            'Phone_Number': phone_number,
            'Disaster_Type': 'Earthquake'
        }
        save_data_to_db(input_data_dict)
