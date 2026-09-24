"""
URL configuration for car_prj project.

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

from car_app import views
from car_prj import settings
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('mvd_dashboard/', views.mvd_dashboard, name='mvd_dashboard'),
    path('add_mvd/', views.add_mvd, name='add_mvd'),
    path('view_mvd/',views.view_mvd,name='view_mvd'),
    path('delete_mvd/<int:id>/',views.delete_mvd,name='delete_mvd'),
    path('mvd_profile/', views.mvd_profile, name='mvd_profile'),
    path('edit_mvd_profile/', views.edit_mvd_profile, name='edit_mvd_profile'),
    path('upload-image/',views.upload_image,name='upload_image'),
    path('prediction-result/<int:id>/',views.prediction_result,name='prediction_result'),
    path('prediction-history/',views.prediction_history,name='prediction_history'),
    path('admin_prediction_history', views.admin_prediction_history, name='admin_prediction_history'),
    path('admin_analytics/', views.admin_analytics, name='admin_analytics'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)