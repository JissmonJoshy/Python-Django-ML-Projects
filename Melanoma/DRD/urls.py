"""DRD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from drdApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('userreg', views.userreg),
    path('docreg', views.docreg),
    path('login', views.login),

    path('adminhome', views.adminhome),
    path('adminviewusers', views.adminviewusers),
    path('adminviewfedback', views.adminviewfedback),
    path('admindetections', views.admindetections),
    path('adminviewdocs', views.adminviewdocs),
    path('adminUpdateUsers', views.adminUpdateUsers),
    path('adminchat', views.adminchat),


    path('userHome', views.userHome),
    path('userfeedback', views.userfeedback),
    path('userprofile', views.userprofile),
    path('detectImage/', views.detectImage, name='detectImage'),
    path('printRes', views.printRes),
    path('userHistory', views.userHistory),
    path('userdocs', views.userdocs),
    path('userbookingdate', views.userbookingdate),
    path('payment', views.payment),
    path('userbooking', views.userbooking),
    path('userbookinghistory', views.userbookinghistory),
    path('userviewpres', views.userviewpres),
    path('userPrinttoken', views.userPrinttoken),
    path('userchat', views.userchat),





    path('docHome', views.docHome),
    path('docBooking', views.docBooking),
    path('docPatient', views.docPatient),
    path('docPrescription', views.docPrescription),
    path('docBookingHistory', views.docBookingHistory),
    path('docPatientHistory', views.docPatientHistory),
    path('docViewPrescription', views.docViewPrescription),









]
