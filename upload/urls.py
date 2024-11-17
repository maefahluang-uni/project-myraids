#upload/urls.py
from django.urls import path
from .views import upload_file
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'upload'

urlpatterns = [
     path('upload/', views.upload_file, name='upload_file'),
    # Add other URLs as needed
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

