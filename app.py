import streamlit as st
import joblib
import pandas as pd

# Load model
model = joblib.load("models/adaptive_crop_recommender_model.pkl")
scaler = joblib.load("models/scaler.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
st.title("🌱 Crop Recommendation System")

# Inputs
N = st.number_input("Nitrogen (N)", 0, 200)
P = st.number_input("Phosphorus (P)", 0, 100)
K = st.number_input("Potassium (K)", 0, 100)
temperature = st.number_input("Temperature", -10.0, 50.0)
humidity = st.number_input("Humidity", 0.0, 100.0)
ph = st.number_input("pH", 0.0, 14.0)
rainfall = st.number_input("Rainfall", 0.0, 500.0)

if st.button("Predict Crop"):
    input_data = pd.DataFrame([{
        'N': N, 'P': P, 'K': K,
        'temperature': temperature,
        'humidity': humidity,
        'ph': ph,
        'rainfall': rainfall
    }])

    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)
    crop = label_encoder.inverse_transform(prediction)[0]

    # === Rule-based correction ===
    if rainfall < 50 and humidity < 30:
        st.warning("⚠️ Very dry conditions detected")
        st.info("Recommended drought-resistant crops like millet or pulses")
        crop = "Millet (Best for dry conditions)"

    # ✅ THIS WAS MISSING
    st.success(f"🌾 Recommended Crop: {crop}")