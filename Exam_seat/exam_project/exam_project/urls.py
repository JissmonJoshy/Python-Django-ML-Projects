"""
URL configuration for exam_project project.

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
from exam_app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path("student_register/", views.student_register, name="student_register"),
    path("staff_register/", views.staff_register, name="staff_register"),

    path("otp_verify/", views.otp_verify, name="otp_verify"),
    path("login/", views.login_view, name="login"),

    
    path('adm/', views.adm, name='adm'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),

    path("add_department/", views.add_department, name="add_department"),
    path("edit_department/<int:id>/", views.edit_department, name="edit_department"),
    path("delete_department/<int:id>/", views.delete_department, name="delete_department"),

    path("add_course/", views.add_course, name="add_course"),
    path("edit_course/<int:id>/", views.edit_course, name="edit_course"),
    path("delete_course/<int:id>/", views.delete_course, name="delete_course"),

    path("add_semester/", views.add_semester, name="add_semester"),
    path("edit_semester/<int:id>/", views.edit_semester, name="edit_semester"),
    path("delete_semester/<int:id>/", views.delete_semester, name="delete_semester"),

    path("add_subject/", views.add_subject, name="add_subject"),
    path("edit_subject/<int:id>/", views.edit_subject, name="edit_subject"),
    path("delete_subject/<int:id>/", views.delete_subject, name="delete_subject"),

    path("add_hall/", views.add_hall, name="add_hall"),
    path("edit_hall/<int:id>/", views.edit_hall, name="edit_hall"),
    path("delete_hall/<int:id>/", views.delete_hall, name="delete_hall"),

    path("student_profile/", views.student_profile, name="student_profile"),
    path("edit_student_profile/", views.edit_student_profile, name="edit_student_profile"),

    path('display_all_students/', views.display_all_students, name='display_all_students'),
    path('reject_student/<int:student_id>/', views.reject_student, name='reject_student'),

    path('display_all_staffs/', views.display_all_staffs, name='display_all_staffs'),
    path('approve_staff<int:staff_id>/', views.approve_staff, name='approve_staff'),
    path('reject_staff/<int:staff_id>/', views.reject_staff, name='reject_staff'),

    path("staff_profile/", views.staff_profile, name="staff_profile"),
    path("edit_staff_profile/", views.edit_staff_profile, name="edit_staff_profile"),

    
    path("add_exam_schedule/", views.add_exam_schedule, name="add_exam_schedule"),
    path("view_exam_schedules/", views.view_exam_schedules, name="view_exam_schedules"),
    path("edit_exam_schedule/<int:id>/", views.edit_exam_schedule, name="edit_exam_schedule"),
    path("delete_exam_schedule/<int:id>/", views.delete_exam_schedule, name="delete_exam_schedule"),

    path('assign_staff/', views.assign_staff_view, name='assign_staff'),
    path('assign_staff/<int:exam_id>/', views.assign_staff_action, name='assign_staff_action'),
    path("exam_schedules_staff/", views.exam_schedules_staff, name="exam_schedules_staff"),
    path("exam_schedules_student/", views.exam_schedules_student, name="exam_schedules_student"),



    
    path("exam_list_for_seat_allocation/", views.exam_list_for_seat_allocation,name="exam_list_for_seat_allocation"),
    path("allocate_seats/<int:exam_id>/", views.allocate_seats, name="allocate_seats"),
    path("delete_seat_allocation/<int:allocation_id>/", views.delete_seat_allocation, name="delete_seat_allocation"),
    path('reset-allocations/<int:exam_id>/', views.reset_allocations, name='reset_allocations'),
    path('ChatBot/',views.ChatBot,name='ChatBot'),




    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)