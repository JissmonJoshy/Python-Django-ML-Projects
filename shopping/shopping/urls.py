"""
URL configuration for shopping project.

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
from shoppingapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('userReg',views.userReg),
    path('verify_otpuser',views.verify_otpuser),
    path('verify_otp',views.verify_otp),
    path('verify_otpDBoy',views.verify_otpDBoy),
    path('shopReg',views.shopReg),
    path('deliveryboyReg',views.deliveryboyReg),
    path('login',views.login),


    path('adminHome',views.adminHome),
    path('adminUser',views.adminUser),
    path('adminSupplier',views.adminSupplier),
    path('adminApproveShop',views.adminApproveShop),
    path('adminDelivery',views.adminDelivery),
    path('adminApproveDelivery',views.adminApproveDelivery),
    path('adminProduct',views.adminProduct),
    path('adminFeedback',views.adminFeedback),
    path('adminReport',views.adminReport),
    path('adminSalaryReport',views.adminSalaryReport),

    path('userHome',views.userHome),
    path('userProducts',views.userProducts),
    path('userPreBook',views.userPreBook),
    path('userPrePay',views.userPrePay),
    path('userCart',views.userCart),
    path('userRemove',views.userRemove),
    path('custPay',views.custPay),
    path('userBookings',views.userBookings),
    path('userChat',views.userChat),
    path('userFeedback',views.userFeedback),


    path('shopHome',views.shopHome),
    path('shopAdd',views.shopAdd),
    path('shopAddCount',views.shopAddCount),
    path('shopBooking',views.shopBooking),
    path('shopChat',views.shopChat),
    path('shopReport',views.shopReport),
    path('shopDelProd',views.shopDelProd),
    path('shopFeedbacks',views.shopFeedbacks),
    path('shopDBoys',views.shopDBoys),


    path('deliveryBoyHome',views.deliveryBoyHome),
    path('deliveryOrder',views.deliveryOrder),
    path('deliveryUpdate',views.deliveryUpdate),
    path('deliveyCompleted',views.deliveyCompleted),
    path('deliveyEarnings',views.deliveyEarnings),
    path('viewPayment', views.viewPayment),
]
