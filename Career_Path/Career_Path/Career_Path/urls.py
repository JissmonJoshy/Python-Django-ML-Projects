"""
URL configuration for Career_Path project.

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
from django.conf import settings
from django.conf.urls.static import static
import myapp.views as views

urlpatterns = [
    path('admin/', admin.site.urls),

    path("",views.index, name="index"),
    path("client_reg", views.Client_reg, name="client_reg"),
    path('company_reg', views.company_reg, name='company_reg'),
    path('tutor_register/', views.tutor_register, name='tutor_register'),

    path("login/", views.login, name="login"),

    path('view_companies', views.view_companies, name='view_companies'),
    path('approve_company', views.approve_company, name='approve_company'),
    path('delete_company', views.delete_company, name='delete_company'),
    path('view_tutors/', views.view_tutors, name='view_tutors'),
    path('approve_tutor/<int:tid>/', views.approve_tutor, name='approve_tutor'),
    path('reject_tutor/<int:tid>/', views.reject_tutor, name='reject_tutor'),



    #Admin
    path("adminhome", views.adminhome, name="adminhome"),
    path("admin_viewClients", views.admin_viewClients, name="admin_viewClients"),
    path("adm_dlClient", views.adm_dlClient, name="adm_dlClient"),
    path('tutor_add_course/', views.tutor_add_course, name='tutor_add_course'),

    path("adm_viewCourses", views.adm_viewCourses, name="adm_viewCourses"),
    path('course_list', views.course_list, name='course_list'),
    path('adm_viewapplycourse', views.adm_viewapplycourse, name='adm_viewapplycourse'),
    path('approve', views.approve, name='approve'),

    path('add_jobs', views.add_jobs, name='add_jobs'),
    path('company_added_jobs/', views.company_added_jobs, name='company_added_jobs'),
    path('edit_company_job/<int:id>/', views.edit_company_job, name='edit_company_job'),
    path('delete_company_job/<int:id>/', views.delete_company_job, name='delete_company_job'),


    path('adm_viewJobs', views.adm_viewJobs, name='adm_viewJobs'),
    path('dlt_course', views.dlt_course, name='dlt_course'),

    path('add_question', views.add_question, name='add_question'),
    path('view_questions', views.view_questions, name='view_questions'),


 

    # Client
    path("clienthome", views.clienthome, name="clienthome"),
    path("clientprofile", views.clientprofile, name="clientprofile"),
    path("client_view_courses", views.client_view_courses, name="client_view_courses"),
    path("client_view_coursedetails", views.client_view_coursedetails, name="client_view_coursedetails"),
    path("applycourse", views.applycourse ,name="applycourse"),
    path("approved_courses", views.approved_courses ,name="approved_courses"),
    path("payment", views.payment ,name="payment"),
    path("client_view_jobs", views.client_view_jobs ,name="client_view_jobs"),
    path("edit_client_profile", views.edit_client_profile, name="edit_client_profile"),
    path("client_interest", views.client_interest, name="client_interest"),
    path("client_interests", views.client_interest, name="client_interests"),
    path('feedback/', views.give_feedback, name='submit_feedback'),
    path('view_feedbacks/', views.view_feedbacks, name='view_feedbacks'),
    path('attempt_quiz/<int:course_id>', views.attempt_quiz, name='attempt_quiz'),
    path('view_marks', views.view_marks, name='view_marks'),
    path('adm', views.adm, name='adm'),
    # path('delete_login', views.delete_login, name='delete_login'),

# Company
    path('companyhome', views.companyhome, name='companyhome'),
    path('company_profile', views.company_profile, name='company_profile'),
    path('edit_company_profile', views.edit_company_profile, name='edit_company_profile'),

    path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('job_applicants_company/', views.job_applicants_company, name='job_applicants_company'),
    path('add_job_feedback/<int:job_id>/', views.add_job_feedback, name='add_job_feedback'),

    path('admin_view_feedback/', views.admin_view_feedback, name='admin_view_feedback'),
    path('company_view_feedback/', views.company_view_feedback, name='company_view_feedback'),


###########Tutor#######

    path('tutorhome', views.tutorhome, name='tutorhome'),
    path('tutor_profile/', views.tutor_profile, name='tutor_profile'),
    path('edit_tutor_profile/', views.edit_tutor_profile, name='edit_tutor_profile'),

    path('tutor_view_courses/', views.tutor_view_courses, name='tutor_view_courses'),
    path('tutor_edit_course/<int:cid>', views.tutor_edit_course),
    path('tutor_delete_course/<int:cid>', views.tutor_delete_course),
    path('admin_view_courses/', views.admin_view_courses, name='admin_view_courses'),
    path('approve_course/<int:id>/', views.approve_course, name='approve_course'),
    path('reject_course/<int:id>/', views.reject_course, name='reject_course'),
    # urls.py
    path('course_payment/', views.course_payment, name='course_payment'),
    path('client_my_courses/', views.client_my_courses, name='client_my_courses'),

    path('tutor_enrolled_students/', views.tutor_enrolled_students, name='tutor_enrolled_students'),
    path('tutor_feedbacks/', views.tutor_feedbacks, name='tutor_feedbacks'),

    path('chat/', views.chat, name='chat'),
    path('reply/', views.reply, name='reply'),

    path('chat-company/', views.chat_company, name='chat_company'),
    path('reply-company/', views.reply_company, name='reply_company'),

    path('add-notes/', views.add_notes, name='add_notes'),
    path('tutor-enrolled-students/', views.tutor_enrolled_students, name='tutor_enrolled_students'),
    path('view-notes', views.view_notes, name='view_notes'),
    path('delete-note/<int:id>', views.delete_note, name='delete_note'),
    path('client-view-notes/<int:course_id>', views.client_view_notes, name='client_view_notes'),

    path('admin_job_applicants', views.admin_job_applicants, name='admin_job_applicants'),
    path('admin_course_enrollments', views.admin_course_enrollments, name='admin_course_enrollments'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)