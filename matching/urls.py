# urls.py

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

    # Step 1: File and patient selection
    path('select-files/', views.file_selection_view, name='file_selection'),

    # Step 2: Column selection
    path('select-columns/', views.column_selection_view, name='column_selection'),

    # Step 3: Column pairing
    path('pair-columns/', views.column_pairing_view, name='column_pairing'),

    # Step 4: View match results
    path('results/', views.match_results_view, name='match_results'),

    path('results/<int:session_id>/', views.display_results, name='display_results'),
]

# Serve static files in development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
