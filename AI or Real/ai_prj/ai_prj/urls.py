"""
URL configuration for ai_prj project.

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
from ai_app import views
from ai_prj import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path("user_register/", views.user_register, name="user_register"),
    path("view_users/", views.view_users, name="view_users"),
    path("toggle_user_status/<int:id>/", views.toggle_user_status, name="toggle_user_status"),
    path("delete_user/<int:id>/", views.delete_user, name="delete_user"),
    path("user_profile/", views.user_profile, name="user_profile"),

    path(
    'predict_image/',
    views.predict_image_view,
    name='predict_image'
    ),

    path(
    'prediction_history/',
    views.prediction_history,
    name='prediction_history'
    ),
    

    path(
    "admin_view_history/",
    views.admin_view_history,
    name="admin_view_history"
    ),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)