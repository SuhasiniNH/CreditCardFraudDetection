# Credit Card Fraud Detection

Detects fraudulent credit card transactions using historical transaction data. By analyzing transaction patterns, the model distinguishes between normal and fraudulent activity, helping financial institutions flag suspicious behavior early and reduce potential losses.

## Dataset

This project uses the [Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) from Kaggle.

The dataset (`creditcard.csv`, ~144 MB) is not included in this repo due to GitHub's file size limits. To run this project:
1. Download `creditcard.csv` from the Kaggle link above.
2. Place it in the root of this repo.

## Project Structure

```text
├── main.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js

    
- `Credit-Card-Fraud-Detection.ipynb` — data exploration, preprocessing, model training, and evaluation.
- `fraud_model.pkl` — trained Random Forest model.
- `sample.csv` — a small sample of real transactions (with true labels) for testing the demo.

## Model

A `RandomForestClassifier` (scikit-learn) trained on the dataset's 30 features (`Time`, `V1`–`V28`, `Amount`).

**Results:**
| Metric | Score |
|---|---|
| Accuracy | 99.96% |
| Precision | 97.47% |
| Recall | 78.57% |
| F1 Score | 87.01% |
| MCC | 87.49% |

## Running the demo

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Upload a CSV of transactions (same columns as the training data), or use `sample.csv` to see the model in action on real transaction examples.
