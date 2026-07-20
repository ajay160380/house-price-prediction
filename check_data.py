import pandas as pd
df = pd.read_csv('predictor/india_housing_prices.csv')
print("Unique States:", df['State'].nunique())
print("Unique Cities:", df['City'].nunique())
print("Unique Localities:", df['Locality'].nunique())
