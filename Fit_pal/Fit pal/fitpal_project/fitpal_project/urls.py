"""
URL configuration for fitpal_project project.

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
from django.contrib import admin
from django.urls import path
from fitpal_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('ad',views.admin),

    path('', views.index, name='index'),              ###Just 
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_in', views.sign_in, name='sign_in'),
    

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('expert_dashboard/', views.expert_dashboard, name='expert_dashboard'),
    path('dietician_dashboard/', views.dietician_dashboard, name='dietician_dashboard'),

    path('view_login/', views.view_login, name='view_login'),
    path('register', views.register, name='register'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('expert_sign_up', views.expert_sign_up, name='expert_sign_up'),
    path('dietician_sign_up/', views.dietician_sign_up, name='dietician_sign_up'),

    path('view_users/', views.view_users, name='view_users'),
    path('view_experts/', views.view_experts, name='view_experts'),
    path('accept_expert/<int:expert_id>/', views.accept_expert, name='accept_expert'),
    path('reject_expert/<int:expert_id>/', views.reject_expert, name='reject_expert'),

    path('expert_profile/', views.expert_profile, name='expert_profile'),

    path('upload_image_plan/', views.upload_image_plan, name='upload_image_plan'),
    path('upload_video_plan/', views.upload_video_plan, name='upload_video_plan'),
    path('view_image_plans/', views.view_image_plans, name='view_image_plans'),
    path('view_video_plans/', views.view_video_plans, name='view_video_plans'),
    path('edit_image_plan/<int:plan_id>/', views.edit_image_plan, name='edit_image_plan'),
    path('delete_image_plan/<int:plan_id>/', views.delete_image_plan, name='delete_image_plan'),
    path('edit_video_plan/<int:plan_id>/', views.edit_video_plan, name='edit_video_plan'),
    path('delete_video_plan/<int:plan_id>/', views.delete_video_plan, name='delete_video_plan'),

    path('user_profile/', views.user_profile, name='user_profile'),
    path('image_plans/', views.image_plans, name='image_plans'),
    path('video_plans/', views.video_plans, name='video_plans'),
    path("all_experts/", views.all_experts, name="all_experts"),

    path('add_diet_program/', views.add_diet_program, name='add_diet_program'),
    path("view_diet_programs/", views.view_diet_programs, name="view_diet_programs"),
    path("add_health_metrics/", views.add_health_metrics, name="add_health_metrics"),
    path("my_health_metrics/", views.my_health_metrics, name="my_health_metrics"),

    path("user_view_diet_programs/", views.user_view_diet_programs, name="user_view_diet_programs"),
    path("join_diet_program/<int:program_id>/", views.join_diet_program, name="join_diet_program"),
    path("my_diet_programs/", views.my_diet_programs, name="my_diet_programs"),
    path("complete_step/<int:progress_id>/", views.complete_step, name="complete_step"),

    path("joined_users/", views.joined_users, name="joined_users"),

    path('reply/', views.reply, name='reply'),
    path('chat/', views.chat, name='chat'),

    path("view_videos_images/", views.view_videos_images, name="view_videos_images"),
    path("admin_view_programs/", views.admin_view_programs, name="admin_view_programs"),
    path("diet_feedback/<int:program_id>/", views.diet_feedback, name="diet_feedback"),
    path('all_diet_feedbacks/', views.all_diet_feedbacks, name='all_diet_feedbacks'),
    path('workout-recommend/', views.workout_recommendation, name='workout_recommend'),

    path('ChatBot/',views.ChatBot,name='ChatBot'),

    #########DIETICIAN URLS#########

    path('view_dietician/', views.view_dietician, name='view_dietician'),
    path('approve_dietician/<int:id>/', views.approve_dietician, name='approve_dietician'),
    path('reject_dietician/<int:id>/', views.reject_dietician, name='reject_dietician'),
    path('dietician_profile/', views.dietician_profile, name='dietician_profile'),
    path('edit_dietician_profile/', views.edit_dietician_profile, name='edit_dietician_profile'),

    path('add_diet_plan/', views.add_diet_plan, name='add_diet_plan'),
    path('view_diet_plans/', views.view_diet_plans, name='view_diet_plans'),
    path('edit_diet_plan/<int:id>/', views.edit_diet_plan, name='edit_diet_plan'),
    path('delete_diet_plan/<int:id>/', views.delete_diet_plan, name='delete_diet_plan'),

    path('nutrition_plans/', views.user_nutrition_plans, name='user_nutrition_plans'),
    path('join_plan/<int:plan_id>/', views.join_nutrition_plan, name='join_nutrition_plan'),

    path('dietician_join_requests/',views.dietician_join_requests,name='dietician_join_requests'),
    path('update_join_request_status/<int:req_id>/<str:status>/',views.update_join_request_status,name='update_join_request_status'),
    path('user_approved_plans/',views.user_approved_plans,name='user_approved_plans'),
    path('user_plan_detail/<int:plan_id>/',views.user_plan_detail,name='user_plan_detail'),
    path('toggle_step_completion/<int:step_id>/',views.toggle_step_completion,name='toggle_step_completion'),

    path('display_dieticians/', views.display_dieticians, name='display_dieticians'),
    

    path('dietician_chat/', views.dietician_chat, name='dietician_chat'),
    path('user_dietician_chat/', views.user_dietician_chat, name='user_dietician_chat'),
    path('all_nutrition_feedback/', views.all_nutrition_feedback, name='all_nutrition_feedback'),
    path('admin_nutrition_plans/', views.admin_nutrition_plans, name='admin_nutrition_plans'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

