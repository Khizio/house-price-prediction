import pandas as pd
import numpy as np
import os

def generate_enhanced_data(n_samples=1000, output_path='data/house_prices_expert.csv'):
    np.random.seed(42)
    
    # Core features
    area = np.random.normal(2000, 500, n_samples).clip(500, 5000)
    bedrooms = np.random.randint(1, 6, n_samples)
    bathrooms = np.random.randint(1, 4, n_samples)
    age = np.random.randint(0, 50, n_samples)
    garage_size = np.random.randint(0, 3, n_samples)
    has_garden = np.random.choice([0, 1], n_samples)
    
    # More realistic features
    neighborhoods = ['Downtown', 'Suburbs', 'Rural', 'Modern_District']
    neighborhood = np.random.choice(neighborhoods, n_samples)
    
    distance_to_center = np.random.uniform(1, 30, n_samples)
    
    conditions = ['New', 'Good', 'Renovated', 'Old']
    condition = np.random.choice(conditions, n_samples)
    
    # Base price calculation with some logic
    # Base $50,000 + area*$150 + beds*$10k + baths*$8k - age*$1k
    price = 50000 + (area * 150) + (bedrooms * 10000) + (bathrooms * 8000) - (age * 1200)
    
    # Neighborhood multipliers
    n_map = {'Downtown': 1.8, 'Modern_District': 1.5, 'Suburbs': 1.2, 'Rural': 0.8}
    price *= np.array([n_map[n] for n in neighborhood])
    
    # Distance penalty
    price -= (distance_to_center * 2000)
    
    # Condition modifiers
    c_map = {'New': 1.3, 'Good': 1.0, 'Renovated': 1.15, 'Old': 0.7}
    price *= np.array([c_map[c] for n, c in zip(neighborhood, condition)])
    
    # Add noise
    price += np.random.normal(0, 5000, n_samples)
    
    df = pd.DataFrame({
        'Area_sqft': area,
        'Bedrooms': bedrooms,
        'Bathrooms': bathrooms,
        'Age_years': age,
        'Garage_size': garage_size,
        'Has_Garden': has_garden,
        'Neighborhood': neighborhood,
        'Distance_to_Center': distance_to_center,
        'Condition': condition,
        'Price_USD': price.round(2)
    })
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {n_samples} samples and saved to {output_path}")

if __name__ == "__main__":
    generate_enhanced_data()
