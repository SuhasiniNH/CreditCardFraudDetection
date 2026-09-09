from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import joblib
import io

app = FastAPI(title="Credit Card Fraud Detection API")

model= joblib.load("fraud_model.pkl")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be CSV format")

    contents = await file.read()

    try:
        data = pd.read_csv(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="File must be CSV format")

    features = data.drop(columns=["Class"]) if  "Class" in data.columns else data

    try:
        y_predict = model.predict(features)
        y_probability = model.predict_proba(features)[:,1]
    except Exception as e:
        raise HTTPException(status_code=22, detail=f"prediction failed {str(e)}")

    data["Prediction"] = ["Fraud" if p == 1  else "Not_Fraud" for p in y_predict ]
    data["Fraud Probability"] = y_probability.round(2)

    return{
        "total_transactions": len(y_predict),
        "flagged_fraud": int(sum(y_predict)),
        "results": data[["Prediction", "Fraud Probability"]].to_dict(orient="records")
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}






