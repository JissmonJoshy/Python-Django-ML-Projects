"""legal_advisor URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('contact/',views.contact),
    path('userReg/',views.Userregister),
    path('login/',views.logins),
    path('AdvocateReg/',views.AdvocateReg, name='AdvocateReg'),
    path('Regpay/',views.Regpay,name='Regpay'),
    path('userhome/',views.userhome),
    path('advocatehome/',views.advocatehome),
    path('admhome/',views.admhome),
    path('admviewusers/',views.admviewusers),
    path('admviewadvocate/',views.admviewadvocate),
    path('add_case_category/',views.add_case_category),
    path('addipc_section/',views.addipc_section),
    path('userview_Advocate/',views.userview_Advocate),
    path('user_home/',views.user_home),
    path('user_add_feed/',views.user_add_feed),
    path('user_view_ipc/',views.user_view_ipc),
    path('user_book_case/',views.user_book_case),
    path('user_view_request/',views.user_view_request),
    path('cancel_case_request', views.cancel_case_request, name='cancel_case_request'),
    path('download_invoice/<int:cid>/', views.download_invoice, name='download_invoice'),
    path('adv_view_request/',views.adv_view_request,name='adv_view_request'),
    path('approve_case_request/',views.approve_case_request),
    path('reject_case_request/',views.reject_case_request),
    path('approve_advocate/',views.approve_advocate),
    path('reject_advocate/',views.reject_advocate),
    path('advocate_add_feed/',views.advocate_add_feed),
    path('adv_view_ipc/',views.adv_view_ipc),
    path('adv_view_approved_case/',views.adv_view_approved_case),
    path('user_profile/',views.user_profile),
    path('user_case_files/',views.user_case_files),
    path('chat/',views.chat),
    path('payment_page/',views.payment_page),
    path('payment_view/',views.payment_view),
    path('Applied_success/',views.Applied_success),
    path('userchat/',views.userchat),
    path('reply/',views.reply),
    path('admviewfeedback/',views.admviewfeedback),
    path('asdfcasdcas/',views.udp),
    path('delete_feedback/',views.delete_feedback),
    path('delete_rating',views.delete_rating),
    path('add_rating/',views.add_rating),
    path('user_case_files/',views.user_case_files),
    path('view_payment_details/',views.view_payment_details),
    path('view_feedback_user/',views.view_feedback_user),
    path('view_feedback_advocate/',views.view_feedback_advocate),

    path('show_case_requests/', views.show_case_requests, name='show_case_requests'),

    path("approve_user/<int:id>/", views.approve_user, name="approve_user"),
    path("reject_user/<int:id>/", views.reject_user, name="reject_user"),
    path("change_advocate_request/", views.change_advocate_request, name="change_advocate_request"),

    path("users_request/", views.users_request, name="users_request"),
    path("approve_advocate_change/<int:case_id>/", views.approve_advocate_change, name="approve_advocate_change"),
    path("reject_advocate_change/<int:case_id>/", views.reject_advocate_change, name="reject_advocate_change"),

    path("upload_case_file/", views.upload_case_file, name="upload_case_file"),
    path("view_ratings/", views.view_ratings, name="view_ratings"),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # urls.py
    path('adv_profile/', views.adv_profile),
    path('edit_adv_profile/', views.edit_adv_profile),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path("set_new_password", views.set_new_password, name="set_new_password"),

]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)