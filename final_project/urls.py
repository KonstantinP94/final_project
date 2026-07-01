from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sport/', include(('sport.urls', 'sport'), namespace='sport')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('', RedirectView.as_view(url='/sport/home/', permanent=False)),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)