from django.urls import path
from . import views


urlpatterns = [
    # path('', views.dashboard, name='dashboard'),
     path('upload/', views.upload_file, name='upload_file'),
     path('history/', views.history_view, name='history_view'),
     path('matchcolumns/', views.matchcolumns_view, name='matchcolumns_view'),
     path('dashboard/', views.dashboard_view, name='dashboard_view'),
    # Add other URLs as needed
   
]