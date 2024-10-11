# matching/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'matching'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('select_files/', views.select_files_for_matching, name='select_files'),
    path('select_columns/', views.select_columns_for_matching, name='select_columns'),
    path('view_results/', views.view_matching_results, name='view_results'),
    path('view_history/', views.view_matching_history, name='view_matching_history'),
    path('create_preset/', views.create_matching_preset, name='create_matching_preset'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
