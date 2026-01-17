# app/main.py
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import io
import os
import sys
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Add src to path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import PIPELINE_PATH

app = FastAPI(
    title="Expert House Price Prediction API",
    description="A production-ready API for predicting house prices using an XGBoost model.",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Load model pipeline
if os.path.exists(PIPELINE_PATH):
    pipeline = joblib.load(PIPELINE_PATH)
else:
    pipeline = None

class HouseFeatures(BaseModel):
    Area_sqft: float = Field(..., example=2500.0)
    Bedrooms: int = Field(..., example=3)
    Bathrooms: int = Field(..., example=2)
    Age_years: int = Field(..., example=10)
    Garage_size: int = Field(..., example=1)
    Has_Garden: int = Field(..., example=1)
    Neighborhood: str = Field(..., example="Downtown")
    Distance_to_Center: float = Field(..., example=5.5)
    Condition: str = Field(..., example="Good")

@app.get("/")
def read_root():
    return FileResponse("app/static/index.html")

@app.post("/predict")
def predict_price(house: HouseFeatures):
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not found. Please train the model first.")
    
    # Convert input to DataFrame
    input_df = pd.DataFrame([house.dict()])
    
    # Predict
    try:
        prediction = pipeline.predict(input_df)[0]
        return {
            "prediction_usd": round(float(prediction), 2),
            "currency": "USD"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict-bulk")
async def predict_bulk(file: UploadFile = File(...)):
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not found. Please train the model first.")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    try:
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Check required columns
        required = ['Area_sqft', 'Bedrooms', 'Bathrooms', 'Age_years', 'Garage_size', 
                    'Has_Garden', 'Neighborhood', 'Distance_to_Center', 'Condition']
        
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing columns: {', '.join(missing)}")
            
        # Predict
        predictions = pipeline.predict(df)
        df['Predicted_Price_USD'] = predictions.astype(float).round(2)
        
        # Convert to list of dicts for JSON response
        results = df.to_dict(orient='records')
        return {"results": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk processing error: {str(e)}")

@app.get("/health")
def health_check():
    status = "ready" if pipeline else "model_missing"
    return {"status": status}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
