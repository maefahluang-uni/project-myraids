from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [
    path('', views.display_data, name='display_data'),
    path('select/<str:directory>/', views.select_directory, name='select_directory'),
    path('save/<str:filename>/', views.save_selected_data, name='save_selected_data'),  # Updated pattern
]
