# src/train.py
import pandas as pd
import joblib
import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

from src.config import DATA_PATH, TARGET, PIPELINE_PATH, XGB_PARAMS, MODEL_DIR
from src.preprocessing import create_preprocessing_pipeline

def train_model():
    # Load data
    print(f"Loading data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    
    X = df.drop(TARGET, axis=1)
    y = df[TARGET]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create full pipeline
    preprocessor = create_preprocessing_pipeline()
    model = XGBRegressor(**X_PARAMS) # This was a typo in my thought, fixing to XGB_PARAMS
    # Wait, XGB_PARAMS is correct in my config. Fixing here.

def train_and_evaluate():
    print(f"Loading data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    
    X = df.drop(TARGET, axis=1)
    y = df[TARGET]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize pipeline
    full_pipeline = Pipeline(steps=[
        ('preprocessor', create_preprocessing_pipeline()),
        ('model', XGBRegressor(**XGB_PARAMS))
    ])
    
    # Train
    print("Training XGBoost Regressor...")
    full_pipeline.fit(X_train, y_train)
    
    # Cross-validation
    print("Performing Cross-Validation...")
    cv_scores = cross_val_score(full_pipeline, X_train, y_train, cv=5, scoring='r2')
    print(f"CV R2 scores: {cv_scores}")
    print(f"Mean CV R2: {cv_scores.mean():.4f}")
    
    # Evaluate on test set
    y_pred = full_pipeline.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse**0.5
    r2 = r2_score(y_test, y_pred)
    
    print("\n--- Test Set Evaluation ---")
    print(f"MAE:  ${mae:,.2f}")
    print(f"RMSE: ${rmse:,.2f}")
    print(f"R2:   {r2:.4f}")
    
    # Persistence
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(full_pipeline, PIPELINE_PATH)
    print(f"\nPipeline saved to {PIPELINE_PATH}")
    
    # Plot Feature Importance
    model_step = full_pipeline.named_steps['model']
    preprocessor_step = full_pipeline.named_steps['preprocessor']
    
    # Correct way to get feature names from preprocessor in newer sklearn
    try:
        all_features = preprocessor_step.get_feature_names_out()
    except:
        # Fallback for older versions
        ohe_features = list(preprocessor_step.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out())
        all_features = list(NUMERIC_FEATURES) + ohe_features
    
    importances = model_step.feature_importances_
    feat_importances = pd.Series(importances, index=all_features)
    
    plt.figure(figsize=(10, 8))
    feat_importances.nlargest(15).plot(kind='barh')
    plt.title('Top 15 Feature Importances')
    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_DIR, 'feature_importance.png'))
    print(f"Feature importance plot saved to {os.path.join(MODEL_DIR, 'feature_importance.png')}")

if __name__ == "__main__":
    train_and_evaluate()
