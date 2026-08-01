import streamlit as st
import pandas as pd
import joblib

st.title('Credit Card Fraud Detector')

model = joblib.load('fraud_model.pkl')

st.write("Upload a CSV with the same columns as the training data (Time, V1-V28, Amount) — no 'Class' column needed.")

upload_file = st.file_uploader("Upload transactions csv", type="csv")

if upload_file is not None:
    data = pd.read_csv(upload_file)

    # Drop the Class column if present (e.g. when uploading sample.csv, which keeps it for reference)
    features = data.drop(columns=['Class']) if 'Class' in data.columns else data

    y_predict = model.predict(features)
    y_probability = model.predict_proba(features)[:, 1]

    data['Prediction'] = ['Fraud' if p == 1 else 'Not a Fraud' for p in y_predict]
    data['Fraud Probability'] = y_probability

    st.write(data[['Prediction', 'Fraud Probability']])
    st.write(f"Flagged {sum(y_predict)} out of {len(y_predict)} transactions as fraud.")