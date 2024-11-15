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

    # Home view to display matching sessions
    path('home/', views.home, name='home'),

    # Step 1: File selection for new comparison
    path('create/', views.create_comparison, name='create_comparison'),

    # AJAX: Load columns after file selection
    path('load-columns/', views.load_columns, name='load_columns'),

    # Step 2: Column selection
    path('select-columns/', views.select_columns, name='column_selection'),

    # Step 3 (Optional): Column pairing for mismatched names
    path('pair-columns/', views.pair_columns, name='pair_columns'),

    # Step 4: View match results for comparison
    path('results/<int:comparison_id>/', views.compare_results, name='compare_results'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
