import os
import json
import pickle

import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'predictor', 'ml_models')
MODEL_PATH = os.path.join(MODEL_DIR, 'banglore_home_prices_model.pickle')
COLUMNS_PATH = os.path.join(MODEL_DIR, 'columns.json')


def load_model():
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(COLUMNS_PATH) as f:
        columns_data = json.load(f)
    data_columns = columns_data['data_columns']
    return model, data_columns


def get_locations():
    _, data_columns = load_model()
    return sorted(data_columns[3:])


def predict_price(location: str, sqft: float, bath: int, bhk: int) -> dict:
    model, data_columns = load_model()

    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if location in data_columns:
        loc_index = data_columns.index(location)
        x[loc_index] = 1

    predicted_price = model.predict([x])[0]
    base_price = round(float(predicted_price), 2)
    low_price = round(base_price * 0.95, 2)
    high_price = round(base_price * 1.05, 2)

    return {
        'estimated_price': base_price,
        'estimated_price_low': low_price,
        'estimated_price_high': high_price,
    }
