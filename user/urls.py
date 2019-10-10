"""testproject URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from .views import signup, UserLoginView, activate, ResendEmailView, resend_email_view_ajax
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registration/', signup, name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path(
        'resend_activation_link/<int:preview>/<int:pk>/',
        ResendEmailView.as_view(),
        name="resend_activation_preview"
    ),
    path(
        'resend_activation_link/<int:pk>/',
        resend_email_view_ajax,
        name="resend_activation_link"
    ),
    path('logout/', auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path('404/', TemplateView.as_view(template_name="404.html"), name="404"),
]