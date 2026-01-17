import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os

# Step 1: Loading the Data
# ------------------------
# We use pandas to read our CSV file. 
# Think of a DataFrame as a table similar to an Excel sheet.
print("--- Step 1: Loading the Data ---")
data_path = os.path.join('data', 'house_prices.csv')
df = pd.read_csv(data_path)

# Display the first few rows to see what it looks like
print("First 5 rows of our dataset:")
print(df.head())

# Step 2: Data Cleaning & Preprocessing
# -------------------------------------
# In real projects, data is often "dirty" (missing values, wrong types).
# For this beginner project, our data is clean, but we always check.
print("\n--- Step 2: Data Cleaning & Preprocessing ---")
print(f"Missing values in each column:\n{df.isnull().sum()}")

# We split our data into:
# X (Features/Inputs): Area, Bedrooms, Bathrooms, Age
# y (Target/Output): Price
X = df[['Area_sqft', 'Bedrooms', 'Bathrooms', 'Age_years']]
y = df['Price_USD']

# Step 3: Splitting the Data
# --------------------------
# We split the data into a "Training Set" (to teach the AI) 
# and a "Testing Set" (to check if it actually learned).
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# Step 4: Model Training
# ----------------------
# We use "Linear Regression", which tries to find a straight-line relationship 
# between our features and the price.
print("\n--- Step 4: Training the Model ---")
model = LinearRegression()
model.fit(X_train, y_train)
print("Model training complete!")

# Step 5: Making Predictions
# --------------------------
# Now we ask our trained AI to predict the prices for the test data.
print("\n--- Step 5: Making Predictions ---")
y_pred = model.predict(X_test)

# Let's predict a single house price just for fun:
# A house with 2000 sqft, 3 bedrooms, 2 bathrooms, 5 years old
sample_house = np.array([[2000, 3, 2, 5]])
prediction = model.predict(sample_house)
print(f"Predicted price for a 2000 sqft, 3BR, 5yr old house: ${prediction[0]:,.2f}")

# Step 6: Evaluation
# -------------------
# How good is our model? We use R-squared (max 1.0) and MSE.
print("\n--- Step 6: Evaluation ---")
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared (Accuracy Score): {r2:.2f}")

# Step 7: Visualization
# ----------------------
# It's hard to visualize 4 features at once, so let's plot Area vs Price
plt.figure(figsize=(10, 6))
plt.scatter(df['Area_sqft'], df['Price_USD'], color='blue', label='Actual Data')

# To show the "line of best fit", we'll plot prediction for range of areas
# We'll fix other features to their averages for simplicity
area_range = np.linspace(df['Area_sqft'].min(), df['Area_sqft'].max(), 100).reshape(-1, 1)
avg_beds = np.full((100, 1), df['Bedrooms'].mean())
avg_baths = np.full((100, 1), df['Bathrooms'].mean())
avg_age = np.full((100, 1), df['Age_years'].mean())

X_dummy = np.hstack([area_range, avg_beds, avg_baths, avg_age])
y_line = model.predict(X_dummy)

plt.plot(area_range, y_line, color='red', linewidth=2, label='Regression Line')
plt.title('House Price Prediction: Area vs Price')
plt.xlabel('Area (sq ft)')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# Save the plot
output_dir = 'docs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
plt.savefig(os.path.join(output_dir, 'prediction_plot.png'))
print(f"\nGraph saved to: {os.path.join(output_dir, 'prediction_plot.png')}")
print("Close the graph window to finish the script.")
plt.show()
