from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import RegisterView, VerifyEmailView, message_view, invalid_token_view, ProfileView
from clients.apps import ClientsConfig

app_name = ClientsConfig.name

urlpatterns = [
    path('login', LoginView.as_view(template_name='clients/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(template_name='clients/register.html'), name='register'),
    path('verify_email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('email_check_message/', message_view, name='email_check_message'),
    path('invalid_token/', invalid_token_view, name='invalid_token'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
