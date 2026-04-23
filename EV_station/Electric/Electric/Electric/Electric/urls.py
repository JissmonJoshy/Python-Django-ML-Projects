"""
URL configuration for Electric project.

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
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.index),
    path('login/',views.login),
    path('userRegister/',views.userRegister),
    
    path('verify_otp/', views.verify_otp),




    # path('ad',views.admin),
    path('adminHome/',views.adminHome),
    path('users/',views.users),
    path('deleteUser/', views.deleteUser, name='deleteUser'),
    path('owners/',views.owners),
    path('ApproveOwner/',views.ApproveOwner),
    path('deleteOwner/',views.deleteOwner),
    path('viewfeedback/',views.viewfeedback),
    path('deleteStation/', views.deleteStation, name='deleteStation'),

    ##USER##
    path('userHome/',views.userHome),
    path('edit_user_profile/', views.edit_user_profile),

    path('userviewStation/',views.userviewStation,name='userviewStation'),
    path('bookStation/',views.bookStation),
    path('cancel_booking/<int:id>/', views.cancel_booking, name='cancel_booking'),

    path('view/',views.view),
    path('bookview/',views.bookview),
    path('make_payment/<int:booking_id>/',views.make_payment,name='make_payment'),
    path('paidview/',views.paidview),
    path('give_feedback/<int:station_id>/',views.give_feedback),


    ##OWNER##
    path('ownerRegister/',views.ownerRegister),
    path('evOwnerHome/',views.evOwnerHome),
    path('addStation/',views.addStation),
    path('viewStation/',views.viewStation,name='viewStation'),
    path('stationUpdate/',views.stationUpdate,name='stationUpdate'),  
    path('owner_viewfeedback/',views.owner_viewfeedback),  
    path('owner_paidview/',views.owner_paidview,name='owner_paidview'),  
    path('delete_station/<int:id>/', views.delete_station, name='delete_station'),
    path('dlt',views.dlt),  

    path('show_stations/',views.show_stations,name='show_stations'),
    path('stations/approve/<int:station_id>/', views.approve_station, name='approve_station'),
    path('stations/reject/<int:station_id>/', views.reject_station, name='reject_station'),

    path('upload_payment_receipt/<int:payment_id>/',views.upload_payment_receipt, name='upload_payment_receipt'),
    path('adminViewBookings/', views.admin_view_bookings),
    path('deleteBooking/', views.delete_booking),
    path('ownerViewBookings/', views.owner_view_bookings),
    path('adminBookingReport/', views.admin_booking_report, name='admin_booking_report'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('ownerProfile/', views.owner_profile, name='owner_profile'),
    path('edit_owner_profile/', views.edit_owner_profile, name='edit_owner_profile'),


    path('analytics_view/', views.analytics_view, name='analytics_view'),
    path('predict_energy/', views.predict_energy, name='predict_energy'),
    path('predict_cost/', views.predict_cost, name='predict_cost'),
    
    path('recommend_station/', views.recommend_station, name='recommend_station'),

]
    

if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
