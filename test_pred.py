import os
import django
from django.conf import settings
from django.http import HttpRequest, QueryDict

# Configure minimal Django settings
settings.configure(
    DEBUG=True,
    ROOT_URLCONF='predictor.urls',
    INSTALLED_APPS=[
        'predictor',
    ]
)
django.setup()

from predictor.views import predict_home_price

request = HttpRequest()
request.method = 'POST'
request.POST = QueryDict('sqft=1000&bath=2&bhk=2&location=Indira Nagar&city=bangalore')
response = predict_home_price(request)
print("Bangalore:", response.content)

request.POST = QueryDict('sqft=1000&bath=2&bhk=2&location=Gomti Nagar&city=lucknow')
response = predict_home_price(request)
print("Lucknow:", response.content)
