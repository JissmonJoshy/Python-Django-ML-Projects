"""
URL configuration for VideoSummary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from summary import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('userregistration',views.userregistration),
    path('login',views.login),
    path('userhome',views.userhome),
    path('adminhome',views.adminhome),
    path('videosummary',views.videosummary),
    path('textsummary',views.textsummary),
    path('user_video_history',views.user_video_history),
    path('user_profile',views.user_profile),
    path('deleteuserprofile',views.deleteuserprofile),
    path('admin_user',views.admin_user),
    path('admin_user_details',views.admin_user_details),
    path('admin_user_active',views.admin_user_active),
    path('admin_user_inactive',views.admin_user_inactive),
    path('user_feedback',views.user_feedback),
    path('admin_feedbacks',views.admin_feedbacks),
    path('user_premium',views.user_premium),
    path('admin_premium',views.admin_premium),
    path('admin_premium_delete',views.admin_premium_delete),
    path('user_payment',views.user_payment),
]
