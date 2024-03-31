from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [
    path('', views.display_data, name='display_data'),
    path('get_preset_names/', views.get_preset_names, name='get_preset_names'),
    path('select/<str:directory>/', views.select_directory, name='select_directory'),
    path('save/<str:filename>/', views.save_selected_data, name='save_selected_data'),
]

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
