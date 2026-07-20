import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import json
import os

# Load dataset
df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'lucknow_housing_prices.csv'))

# Drop unnecessary columns
df = df.drop(['type', 'carpet_area', 'status'], axis=1)

# Rename columns to match Bangalore format
df = df.rename(columns={'area_sq_ft': 'total_sqft', 'bathrooms': 'bath', 'price_lakh': 'price'})

# Handle missing values
df = df.dropna()

# Reorder columns to match Bangalore format exactly
df = df[['total_sqft', 'bath', 'bhk', 'location', 'price']]

# Clean and filter locations
df['location'] = df['location'].apply(lambda x: x.strip())
location_stats = df['location'].value_counts(ascending=False)
location_stats_less_than_10 = location_stats[location_stats <= 10]
df['location'] = df['location'].apply(lambda x: 'other' if x in location_stats_less_than_10 else x)

# One hot encoding
dummies = pd.get_dummies(df['location'])
df_encoded = pd.concat([df, dummies], axis=1)
df_encoded = df_encoded.drop('location', axis=1)
if 'other' in df_encoded.columns:
    df_encoded = df_encoded.drop('other', axis=1)

X = df_encoded.drop('price', axis=1)
y = df_encoded['price']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
model_path = os.path.join(os.path.dirname(__file__), 'ml_models', 'lucknow_home_prices_model.pickle')
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

# Save columns
columns = {
    'data_columns': [col if col in ['total_sqft', 'bath', 'bhk'] else col.title() for col in X.columns]
}
columns_path = os.path.join(os.path.dirname(__file__), 'ml_models', 'lucknow_columns.json')
with open(columns_path, 'w') as f:
    json.dump(columns, f)

print(f"Model saved to {model_path}")
print(f"Columns saved to {columns_path}")
