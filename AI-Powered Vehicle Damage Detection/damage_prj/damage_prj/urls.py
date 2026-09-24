"""
URL configuration for damage_prj project.

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
from damage_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('insurance_dashboard/', views.insurance_dashboard, name='insurance_dashboard'),
    path('register/', views.user_register, name='user_register'),
    path('insurance_register/', views.insurance_register, name='insurance_register'),
    
    path('view_users/', views.view_users, name='view_users'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),

    path("view_insurance/", views.view_insurance, name="view_insurance"),
    path("toggle_insurance_status/<int:id>/",views.toggle_insurance_status,name="toggle_insurance_status"),
    path("delete_insurance/<int:id>/",views.delete_insurance,name="delete_insurance"),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('insurance_profile/', views.insurance_profile, name='insurance_profile'),
    path('view_insurance_companies/', views.view_insurance_companies, name='view_insurance_companies'),

    path(
        'create-claim/<int:insurance_id>/',
        views.create_claim,
        name='create_claim'
    ),

    path(
        'my-claims/',
        views.my_claims,
        name='my_claims'
    ),

    path(
        'insurance-claims/',
        views.insurance_claims,
        name='insurance_claims'
    ),


    path(
        'run-ai/<int:claim_id>/',
        views.run_ai_detection,
        name='run_ai_detection'
    ),


        path(
        "approve-claim/<int:claim_id>/",
        views.approve_claim,
        name="approve_claim",
    ),

    path(
        "reject-claim/<int:claim_id>/",
        views.reject_claim,
        name="reject_claim",
    ),


    path(
    'admin-claims/',
    views.admin_claims,
    name='admin_claims'
    ),

    path(
        "admin-stat/",
        views.admin_stat,
        name="admin_stat"
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)