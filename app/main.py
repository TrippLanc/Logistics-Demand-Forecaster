import streamlit as st
import pandas as pd 
import numpy as np 
import pickle
import os

st.set_page_config(page_title="DataCo Logistics Risk Forecaster", layout="centered")

st.title("Logistics Demand & Late Delivery Risk Forecaster")
st.markdown("""
            This predictive analytics engine evaluates order profiles at checkout to asses the statistical risk of fulfillment delays *before* transit begins.
            """)

@st.cache_resource
def load_artifacts():
    model_path = os.path.join("models", "late_delivery_rf_model.pkl")
    with open(model_path, "rb") as f:
        return pickle.load(f)
    
try:
    artifacts = load_artifacts()
    model = artifacts['model']
    model_features = artifacts['features']
except FileNotFoundError:
    st.error("Model artifacts file not found. Make sure 'models/late_delivery_rf_model.pkl' exists.")
    st.stop()

st.header("New Order Parameters")

col1, col2 = st.columns(2)

with col1:
    days_scheduled = st.number_input("Scheduled Shipping Days", min_value=0, max_value=10, value=3)
    shipping_mode = st.selectbox("Shipping Mode", ["First Class", "Same Day", "Second Class", "Standard Class"])
    market = st.selectbox("Market Group", ["APAC", "Africa", "Europe", "LATAM", "USCA"])
    
with col2:
    order_hour = st.slider("Order Checkout Hour", 0, 23, 12)
    order_day = st.slider("Day of Month", 1, 31, 15)
    order_day_of_week = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    order_month = st.slider("Month", 1, 12, 6)

order_item_total = st.number_input("Order Item Total ($)", min_value=0.0, value=150.0)
product_price = st.number_input("Product Price ($)", min_value=0.0, value=150.0)

day_mapping = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
numeric_day_of_week = day_mapping[order_day_of_week]

input_data = {
    'days_for_shipment_scheduled': days_scheduled,
    'order_item_quantity': 1,
    'order_item_total': order_item_total,
    'product_price': product_price,
    'category_id': 1,
    'order_year': 2026,
    'order_month': order_month,
    'order_day': order_day,
    'order_hour': order_hour,
    'order_day_of_week': numeric_day_of_week
}

input_df = pd.DataFrame(0, index=[0], columns=model_features)

for col in input_data:
    if col in input_df.columns:
        input_df.loc[0, col] = input_data[col]

ship_col = f"shipping_mode_{shipping_mode}"
market_col = f"market_{market}"

if ship_col in input_df.columns:
    input_df.loc[0, ship_col] = 1
if market_col in input_df.columns:
    input_df.loc[0, market_col] = 1


st.markdown("---")

if st.button("Evaluate Delivery Risk", type="primary"):
    probabilities = model.predict_proba(input_df)[0]
    late_probability = probabilities[1] * 100
    
    st.subheader("Forecast Results")
    
    if late_probability > 50:
        st.error(f"High Risk Detected: There is a **{late_probability:.1f}% statistical probability that this shipment will face delays.")
        st.markdown("**Recommendation:** Upgrade this order profile to an express shipping tier or flag for early warehouse dispatch.")
    else:
        st.success(f"On-time Target: There os a **{100 - late_probability:.1f}% probability this shipment will fulfill on schedule.")
        