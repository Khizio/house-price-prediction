# Professional House Price Prediction System 🏠🚀

An industry-standard Machine Learning pipeline and REST API for predicting house prices with high accuracy using XGBoost and FastAPI.

## 🌟 Key Features
- **Advanced Modeling**: Uses **XGBoost Regressor** with optimized hyperparameters (0.98+ Accuracy).
- **Premium Web UI**: High-end glassmorphism dashboard for real-time interaction.
- **Bulk Data Processing**: Drag & Drop CSV files to predict prices for hundreds of houses at once.
- **Robust Pipeline**: Automated feature engineering and scaling.

## 📁 Project Structure
```text
house-price-prediction/
├── app/
│   └── main.py              # FastAPI Application
├── data/
│   ├── house_prices.csv      # Legacy dataset
│   └── house_prices_expert.csv # Enhanced 1000-sample dataset
├── models/
│   ├── house_price_pipeline.joblib # Saved trained model pipeline
│   └── feature_importance.png      # AI insights graph
├── src/
│   ├── config.py            # Global configuration & Hyperparameters
│   ├── preprocessing.py     # Pipeline definitions
│   ├── train.py             # Training & Evaluation script
│   └── data_generator.py    # Synthetic data generation logic
├── tests/
│   └── test_api.py          # End-to-end API testing
├── requirements.txt         # Production dependencies
└── README.md                # System Documentation
```

## 🛠️ Installation & Setup

1. **Clone & Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Dataset (Optional)**:
   ```bash
   python src/data_generator.py
   ```

3. **Train the Model**:
   ```bash
   python src/train.py
   ```

4. **Launch the API**:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🌐 API Documentation
Once the server is running, visit:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### Sample Prediction Request
**POST** `/predict`
```json
{
  "Area_sqft": 2500,
  "Bedrooms": 4,
  "Bathrooms": 3,
  "Age_years": 2,
  "Garage_size": 2,
  "Has_Garden": 1,
  "Neighborhood": "Suburbs",
  "Distance_to_Center": 12.5,
  "Condition": "New"
}
```

## 📊 Performance Metrics
- **Mean Absolute Error (MAE)**: ~$15,000
- **R-squared Score**: **0.98+** (indicating high predictive power)

---
*Developed for Professional Grade AI Applications.*
