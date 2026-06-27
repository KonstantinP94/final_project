from django.urls import path
from . import views


app_name = 'sport' 

urlpatterns = [
    path('home/', views.home, name='home'),
    path('trainer/<int:trainer_id>/', views.trainer_detail, name='trainer_detail'),
    path('book_slot/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('add_review/<int:trainer_id>/', views.add_review, name='add_review'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    
    
]
