"""textproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from textapp import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('index/', views.index,name='index'),
    path('adminhome/', views.adminhome),
    path('driverhome/', views.driverhome),
    path('userhome/', views.userhome),
    path('', views.index),
    path('login/', views.logins),
    path('userreg/', views.userreg),
    path('driverreg/', views.driverreg),
    path('udp/', views.udp),
    path('adminviewdriver/', views.adminviewdriver),
    path('adminviewuser/', views.adminviewuser),
    path('userviewdriver/', views.userviewdriver),
    path('viewbooking/', views.userviewbooking),
    path('userviewbooking/', views.userviewbooking),
    path('driverviewbooking/', views.driverviewbooking),
    path('ddetection/', views.ddetection),
    path('driverdetection/', views.driverdetection),
    path('userpayment', views.userpayment),
    path('userfeedback', views.userfeedback),
    path('driverviewfeedback', views.driverviewfeedback),

    
    path('start-drowsiness/', views.start_drowsiness,name='start_drowsiness'),
    
]
