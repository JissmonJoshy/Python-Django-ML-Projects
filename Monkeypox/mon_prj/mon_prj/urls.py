"""
URL configuration for mon_prj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from mon_app import views
from mon_prj import settings
from mon_app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('view_users/', views.view_users, name='view_users'),
    path('toggle-user/<int:login_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('delete-user/<int:login_id>/', views.delete_user, name='delete_user'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path("emotion/", views.emotion_predict, name="emotion_predict"),
    path("emotion_history/", views.emotion_history, name="emotion_history"),
    path('admin-history/', views.admin_history, name='admin_history'),


     
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)