from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sport/', include('sport.urls')),
    path('users/', include('users.urls')),
    
]