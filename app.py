import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Credit Card Fraud Detector",
    page_icon="💳",
    layout="centered"
)

model = joblib.load('fraud_model.pkl')

st.title("💳 Credit Card Fraud Detector")
st.caption("Upload transaction data and get instant fraud predictions from a trained Random Forest model.")

st.divider()

with st.container(border=True):
    st.subheader("📁 Upload Transactions")
    st.write(
        "Upload a CSV with the same columns as the training data "
        "(`Time`, `V1`–`V28`, `Amount`) — no `Class` column needed."
    )
    upload_file = st.file_uploader("Upload transactions CSV", type="csv", label_visibility="collapsed")

st.divider()

if upload_file is not None:
    with st.spinner("Analyzing transactions..."):
        data = pd.read_csv(upload_file)
        features = data.drop(columns=['Class']) if 'Class' in data.columns else data

        y_predict = model.predict(features)
        y_probability = model.predict_proba(features)[:, 1]

        data['Prediction'] = ['Fraud' if p == 1 else 'Not Fraud' for p in y_predict]
        data['Fraud Probability'] = y_probability.round(4)

    st.success(f"Analysis complete — flagged **{sum(y_predict)}** out of **{len(y_predict)}** transactions as fraud.")

    col1, col2 = st.columns(2)
    col1.metric("Total Transactions", len(y_predict))
    col2.metric("Flagged as Fraud", int(sum(y_predict)))

    st.dataframe(data[['Prediction', 'Fraud Probability']], use_container_width=True)