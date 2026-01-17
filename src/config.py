# src/config.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'house_prices_expert.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
PIPELINE_PATH = os.path.join(MODEL_DIR, 'house_price_pipeline.joblib')

NUMERIC_FEATURES = [
    'Area_sqft', 
    'Bedrooms', 
    'Bathrooms', 
    'Age_years', 
    'Garage_size', 
    'Distance_to_Center'
]

CATEGORICAL_FEATURES = [
    'Neighborhood', 
    'Condition',
    'Has_Garden'
]

TARGET = 'Price_USD'

# Advanced XGBoost Parameters (Can be tuned)
XGB_PARAMS = {
    'n_estimators': 1000,
    'learning_rate': 0.05,
    'max_depth': 6,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'n_jobs': -1,
    'random_state': 42
}
