from django.urls import path
from .views import upload_file

app_name = 'upload'

urlpatterns = [
     path('upload/', upload_file, name='upload_file'),
    # Add other URLs as needed
]


