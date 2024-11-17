# matching/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'matching'

urlpatterns = [
    # Logout path
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('create/', views.create_comparison, name='create_comparison'),
    path('load-columns/', views.load_columns, name='load_columns'),
    path('select-columns/', views.select_columns, name='column_selection'),
    path('pair-columns/', views.pair_columns, name='pair_columns'),
    path('results/<int:comparison_id>/', views.compare_results, name='compare_results'),
    path('view_history/', views.view_matching_history, name='view_matching_history'),
    path('delete-result/<int:result_id>/', views.delete_result, name='delete_result'),
    
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
