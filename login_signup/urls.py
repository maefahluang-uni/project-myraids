from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'authen'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),  # Signup page (custom view for signup)
]
