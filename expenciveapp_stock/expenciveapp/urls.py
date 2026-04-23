"""
URL configuration for expenciveapp project.

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
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('login/', views.login,name='login'),
    path('adminbase/', views.adminbase,name='adminbase'),

    path('userlist/', views.userlist),
    path('userreg/', views.userreg,name='userreg'),
    path('userhome/', views.userhome),

    ############# FIXED INCOME ###########
    path('fixedincome/', views.fixedincome),
    path('fixed_list/', views.fixed_list),
    path('updatein/', views.updatein),
    path('delete/', views.delete),

    ############ OTHER INCONME   ###########
    path('otherincome/', views.otherincome),
    path('other_list/', views.other_list),
    path('updateother/', views.updateother),
    path('deleteother/', views.deleteother),

    ############ FIXED EXPENSE  ############
    path('fixedexpense/', views.fixedexpense),
    path('expenselist/', views.expenselist),
    path('updateexpense/', views.updateexpense),
    path('deleteexpense/', views.deleteexpense),

    ###########     OTHER EXPENSE     ###############
    path('otherexpense/', views.otherexpense),
    path('otherexplist/', views.otherexplist),
    path('updaexp/', views.updaexp),
    path('delexpense/', views.delexpense),
    path('alllist/', views.alllist),
    path('graph/', views.graph),
    path('billrecipt/', views.billreceipt),
    path('process_invoice/', views.process_invoice),
    path('calculator_view/', views.calculator_view),
  
  ###################################
    path('predictprices/', views.predictprices),
    path("display_users/", views.display_users, name="display_users"),

    path("approve_user/<int:user_id>/", views.approve_user, name="approve_user"),
    path("reject_user/<int:user_id>/", views.reject_user, name="reject_user"),
    path("delete_user/<int:user_id>/", views.delete_user, name="delete_user"),

]

