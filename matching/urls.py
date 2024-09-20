from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'matching'

urlpatterns = [
    path('', views.display_data, name='display_data'),
    path('get_preset_names/', views.get_preset_names, name='get_preset_names'),
    path('get_preset_data/', views.get_preset_data, name='get_preset_data'),
    path('select/<path:directory>/', views.select_directory, name='select_directory'),
    path('save/<path:filename>/', views.save_selected_data, name='save_selected_data'),
    path('home/', views.home, name='home'),
    path('logout/', LogoutView.as_view(), name ='logout'),
]

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
