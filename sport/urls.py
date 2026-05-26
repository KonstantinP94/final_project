from django.urls import path
from . import views


app_name = 'sport' 

urlpatterns = [
    path('home/', views.home, name='home'),
    
]
