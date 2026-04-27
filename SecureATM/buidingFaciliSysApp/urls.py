from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name=''),
    path('log_in/', views.log_in, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('usersprofile/', views.usersprofile, name='usersprofile'),
    path('atm_machine/', views.atm_machine, name='atm_machine'),
    path('otpmodule/', views.otpmodule, name='otpmodule'),

    path('add_branch_page/', views.add_branch_page, name='add_branch_page'),
    path('view_branches/', views.view_branches, name='view_branches'),
    path('view_customers/', views.view_customers, name='view_customers'),
    path('reject_customer/', views.reject_customer, name='reject_customer'),
    path('approve_customer/', views.approve_customer, name='approve_customer'),
    path('reject_banker/', views.reject_banker, name='reject_banker'),
    path('approve_banker/', views.approve_banker, name='approve_banker'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('reject_atmcard/', views.reject_atmcard, name='reject_atmcard'),
    path('branch_reject_atmcard/', views.branch_reject_atmcard, name='branch_reject_atmcard'),

    path('apply_atmcard/', views.apply_atmcard, name='apply_atmcard'),
    path('view_requests/', views.view_requests, name='view_requests'),
    path('issue_atmcard/', views.issue_atmcard, name='issue_atmcard'),
    path('branch_approve_atmcard/', views.branch_approve_atmcard, name='branch_approve_atmcard'),
    path('admin_approve_atmcard/', views.admin_approve_atmcard, name='admin_approve_atmcard'),
    path('view_atmcard/', views.view_atmcard, name='view_atmcard'),
    path('add_cash/', views.add_cash, name='add_cash'),
]