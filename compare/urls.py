from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'comparefiles'

urlpatterns = [
    path('', views.select_files, name='select_files'),
    path('results/', views.results, name='results'),
    # Add URL pattern for deleting a comparison result
    path('results/delete/<int:id>/', views.delete_comparison_result, name='delete_comparison_result'),
]

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
