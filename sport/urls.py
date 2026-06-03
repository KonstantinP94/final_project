from django.urls import path
from . import views


app_name = 'sport' 

urlpatterns = [
    path('home/', views.home, name='home'),
    path('trainer/<int:trainer_id>/', views.trainer_detail, name='trainer_detail'),
    path('book_slot/<int:slot_id>/', views.book_slot, name='book_slot'),
    
]
