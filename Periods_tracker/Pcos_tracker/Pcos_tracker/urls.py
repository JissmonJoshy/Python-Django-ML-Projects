"""
URL configuration for Pcos_tracker project.

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
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name="index"),
    path('user_register/', views.user_register,name="user_register"),
    path('login/',views.login,name='login'),




    ################ADMIN##############
    path('admin_home/',views.admin_home,name='admin_home'),
    path('add_remedies/',views.add_remedies,name='add_remedies'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('view_doctors/', views.view_doctors, name='view_doctors'),
    path('update_doctor/<int:did>', views.update_doctor,name='update_doctor'),
    path('delete_doctor/<int:did>', views.delete_doctor,name='delete_doctor'),





    ################USER##################
    path('User_home/',views.User_home,name='User_home'),
    path('add_period/',views.add_period,name='add_period'),
    path('cycle_history/',views.cycle_history,name='cycle_history'),
    path('diet_remedies/',views.diet_remedies,name='diet_remedies'),
    path('next_period/', views.next_period_tracker, name='next_period'),
    path('ml_period_analysis/', views.ml_period_analysis, name='ml_period_analysis'),
    path('predict_pcos/', views.predict_pcos, name='predict_pcos'),
    path('user_view_doctors/', views.user_view_doctors, name='user_view_doctors'),
    path('book_appointment/<int:did>/', views.book_appointment, name='book_appointment'),
    path('user_view_appointments/', views.user_view_appointments, name='user_view_appointments'),
    path('admin_view_appointments/', views.admin_view_appointments, name='admin_view_appointments'),
    path('approve_appointment/<int:aid>/', views.approve_appointment, name='approve_appointment'),
    path('reject_appointment/<int:aid>/', views.reject_appointment, name='reject_appointment'),
    path('admin_view_appointments/', views.admin_view_appointments, name='admin_view_appointments'),
    path('approve_appointment/<int:aid>/', views.approve_appointment, name='approve_appointment'),
    path('reject_appointment/<int:aid>/', views.reject_appointment, name='reject_appointment'),


    path('user_profile', views.user_profile),
    path('update_profile', views.update_profile),
    path('admin_view_users', views.admin_view_users),
    path('approve_user/<int:uid>', views.approve_user),
    path('reject_user/<int:uid>', views.reject_user),
    path('download_pcos_report', views.download_pcos_report),
    path('doctor_view_appointments',views.doctor_view_appointments),
    path('doctor_give_advice/<int:aid>',views.doctor_give_advice),
    path('doctor_profile', views.doctor_profile),
    path('doctor_home', views.doctor_home),
    # path('user_view_appointments', views.user_view_appointments),
    path('user_view_advice', views.user_view_advice),
            
    




]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)