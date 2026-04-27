"""
URL configuration for studentAttendance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from stApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path('login/', views.login),
    path('MarkAttendance', views.MarkAttendance),


    path('adminhome', views.adminhome),
    path('adminadddepartment', views.adminadddepartment),
    path('admindeletedepartment', views.admindeletedepartment),
    path('adminbatch', views.adminbatch),
    path('admindeletebatch', views.admindeletebatch),
    path('adminaddteachers', views.adminaddteachers),
    path('adminviewteachers', views.adminviewteachers),
    path('deleteTeacher', views.deleteTeacher),
    path('adminViewAtt', views.adminViewAtt),


    path('teacherhome', views.teacherhome),
    path('teacheraddstudent', views.teacheraddstudent),
    path('teacherViewStudents', views.teacherViewStudents),
    path('teacherattendance', views.teacherattendance),
    path('updateStatus', views.updateStatus),



    path('studenthome', views.studenthome),
    path('studentviewattendance', views.studentviewattendance),
]
