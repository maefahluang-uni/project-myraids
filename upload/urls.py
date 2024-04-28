from django.urls import path
from . import views


urlpatterns = [
    # path('', views.dashboard, name='dashboard'),
     path('upload/', views.upload_file, name='upload_file'),
     path('history/', views.history_view, name='history_view'),
     path('match/', views.match_view, name='match_view'),
     path('dashboard/', views.dashboard_view, name='dashboard_view'),
<<<<<<< HEAD
     path('login/', views.login_view,name='login'),
=======
     path('result/', views.result_view, name='result_view'),
>>>>>>> origin/matchcolumns
    # Add other URLs as needed
   
] 