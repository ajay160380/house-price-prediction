from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard', views.index, name='index'),
    path('get_location_names', views.get_location_names, name='get_location_names'),
    path('get_india_hierarchy', views.get_india_hierarchy, name='get_india_hierarchy'),
    path('get_location_insights', views.get_location_insights, name='get_location_insights'),
    path('predict_home_price', views.predict_home_price, name='predict_home_price'),
    path('get_nearby_amenities', views.get_nearby_amenities, name='get_nearby_amenities'),
    path('get_locality_scores', views.get_locality_scores, name='get_locality_scores'),
    path('get_ai_analysis', views.get_ai_analysis, name='get_ai_analysis'),
    path('chatbot', views.chatbot, name='chatbot'),
    path('calculate_commute', views.calculate_commute, name='calculate_commute'),
]
