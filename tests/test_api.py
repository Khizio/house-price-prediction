# tests/test_api.py
import requests
import time
import subprocess
import os
import signal

def test_api():
    print("Starting FastAPI server...")
    # Start server in background
    # We use uvicorn app.main:app to run it
    proc = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(5) # Wait for server to start
    
    try:
        # 1. Health check
        print("Checking health...")
        resp = requests.get("http://127.0.0.1:8000/health")
        print(f"Health: {resp.json()}")
        
        # 2. Prediction test
        print("Testing prediction...")
        payload = {
            "Area_sqft": 2500,
            "Bedrooms": 3,
            "Bathrooms": 2,
            "Age_years": 5,
            "Garage_size": 2,
            "Has_Garden": 1,
            "Neighborhood": "Downtown",
            "Distance_to_Center": 5.0,
            "Condition": "New"
        }
        resp = requests.post("http://127.0.0.1:8000/predict", json=payload)
        print(f"Prediction Result: {resp.json()}")
        
    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        print("Shutting down server...")
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    test_api()
