"""
URL configuration for child_prj project.

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
from child_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('doctor_registration',views.doctor_registration, name='doctor_registration'),
    path('customer_registration',views.customer_registration, name='customer_registration'),
    path('admin_dashboard',views.admin_dashboard, name='admin_dashboard'),
    path('customer_dashboard',views.customer_dashboard, name='customer_dashboard'),
    path('doctor_dashboard',views.doctor_dashboard, name='doctor_dashboard'),
    path('login_view',views.login_view,name='login_view'),
    path('adm',views.adm, name='adm'),
    path('admin_view_doctors/', views.admin_view_doctors, name='admin_view_doctors'),
    path('admin_view_customers/', views.admin_view_customers, name='admin_view_customers'),

    path('approve_doctor/<int:id>/', views.approve_doctor, name='approve_doctor'),
    path('reject_doctor/<int:id>/', views.reject_doctor, name='reject_doctor'),

    path('reject_customer/<int:id>/', views.reject_customer, name='reject_customer'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
    path('customer_profile/', views.customer_profile, name='customer_profile'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('doctor_view_appointments/', views.doctor_view_appointments, name='doctor_view_appointments'),
    path('approve_appointment/<int:id>/', views.approve_appointment, name='approve_appointment'),
    path('user_view_appointments/', views.user_view_appointments, name='user_view_appointments'),
    path('make_payment/<int:id>/', views.make_payment, name='make_payment'),
    path('cancel_appointment/<int:id>/', views.cancel_appointment, name='cancel_appointment'),
    path('upload', views.upload_image, name='upload'),


]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

