"""
URL configuration for reversibleDataHiding project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from uceApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('reg/', views.reg),
    path('otp-verify/', views.otp_verify, name='otp_verify'),
    path('login/', views.login),
    path('profile/', views.profile),
    # path('dlt/', views.dlt),












    path('adminHome/', views.adminHome),
    path('adminViewUsers/', views.adminViewUsers),
    path('adminViewFeedbacks/', views.adminViewFeedbacks),












    path('userHome/', views.userHome),
    path('userEnc/', views.userEnc),
    path('userEncData/', views.userEncData),
    path('userImageEnc/', views.userImageEnc),
    path('userImageEncData/', views.userImageEncData),
    path('userTextEnc/', views.userTextEnc),
    path('userTextEncData/', views.userTextEncData),
    path('userFeedback/', views.userFeedback),
    path('generate_audio/', views.generate_audio),





















    
]
