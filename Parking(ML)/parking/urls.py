"""
URL configuration for parking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from parkingapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('userReg', views.userReg),
    path('managerReg', views.managerReg),
    path('login', views.login),

    path('adminHome', views.adminHome),
    path('adminUser', views.adminUser),
    path('adminActiveUser', views.adminActiveUser),
    path('adminManager', views.adminManager),
    path('adminActive', views.adminActive),
    path('adminReport', views.adminReport),
    path('adminComplaints', views.adminComplaints),

    path('userHome', views.userHome),
    path('userParkings', views.userParkings),
    path('userAvailableSlots', views.userAvailableSlots),
    path('userPay', views.userPay),
    path('userBookings', views.userBookings),
    path('userComplaint', views.userComplaint),
    path('userProfile', views.userProfile),
  

    path('managerHome', views.managerHome),
    path('manAmount', views.manAmount),
    path('manSlot', views.manSlot),
    path('managerActive', views.managerActive),
    path('manBookking', views.manBookking),
    path('manProfile', views.manProfile),
    path('manComplete', views.manComplete),

    path(
    "userOccupancyPrediction",
    views.userOccupancyPrediction,
    name="userOccupancyPrediction"
),
]
