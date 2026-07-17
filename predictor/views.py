import json
import numpy as np
import pickle
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml_models', 'banglore_home_prices_model.pickle')
COLUMNS_PATH = os.path.join(os.path.dirname(__file__), 'ml_models', 'columns.json')

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

with open(COLUMNS_PATH) as f:
    columns_data = json.load(f)

data_columns = columns_data['data_columns']
locations = data_columns[3:]

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')


def index(request):
    return render(request, 'index.html')


def get_location_names(request):
    return JsonResponse({'locations': locations})


@csrf_exempt
def get_location_insights(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    location = request.POST.get('location', '')
    if not location:
        return JsonResponse({'error': 'Location is required'}, status=400)

    if not GROQ_API_KEY:
        return JsonResponse({'insight': f'{location} is a prominent neighborhood in Bengaluru with growing real estate demand and excellent connectivity to major IT corridors.'})

    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        prompt = (
            f'Return a JSON object with keys: insight_text (2-sentence professional real estate '
            f'insight about {location}, Bangalore, covering connectivity, infrastructure, and '
            f'market trends), investment_score (number 0-10 for ROI potential), safety_score '
            f'(number 0-10 for neighborhood safety and infrastructure). Only valid JSON.'
        )
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.7,
        )
        result = json.loads(response.choices[0].message.content)
        return JsonResponse({
            'insight_text': result.get('insight_text', ''),
            'investment_score': result.get('investment_score', 7),
            'safety_score': result.get('safety_score', 7),
        })
    except Exception:
        return JsonResponse({
            'insight_text': (
                f'{location} is a sought-after residential area in Bengaluru with '
                f'developing infrastructure and good connectivity to major business hubs.'
            ),
            'investment_score': 7,
            'safety_score': 7,
        })


@csrf_exempt
def predict_home_price(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    sqft = float(request.POST.get('sqft', 0))
    bath = int(request.POST.get('bath', 0))
    bhk = int(request.POST.get('bhk', 0))
    location = request.POST.get('location', '')

    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if location in data_columns:
        loc_index = data_columns.index(location)
        x[loc_index] = 1

    predicted_price = model.predict([x])[0]
    base_price = round(predicted_price, 2)
    low_price = round(predicted_price * 0.95, 2)
    high_price = round(predicted_price * 1.05, 2)

    return JsonResponse({
        'estimated_price': base_price,
        'estimated_price_low': low_price,
        'estimated_price_high': high_price,
    })
