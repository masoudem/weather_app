from django.urls import path
from .views import WeatherList


urlpatterns = [
    path('weather/<str:city>', WeatherList.as_view(), name='weather-list'),
]
