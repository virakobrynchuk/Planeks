from django.urls import path

from weather.views import index_html
from . import views

urlpatterns = [
    path('weather/', index_html, name='weather_index'),
]
