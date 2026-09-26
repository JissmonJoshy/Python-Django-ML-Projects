"""
URL configuration for vegfru_prj project.

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
from vegfru_app import views
from vegfru_prj import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('store_manager_dashboard/', views.store_manager_dashboard, name='store_manager_dashboard'),
    path('quality_inspector_dashboard/', views.quality_inspector_dashboard, name='quality_inspector_dashboard'),

    path("add_quality_inspector/", views.add_quality_inspector,name="add_quality_inspector"),

    path("delete_quality_inspector/<int:id>/",
         views.delete_quality_inspector,
         name="delete_quality_inspector"),

    path("toggle_quality_inspector/<int:id>/",
         views.toggle_quality_inspector,
         name="toggle_quality_inspector"),


    path(
    "add_store_manager/",
    views.add_store_manager,
    name="add_store_manager"
    ),

    path(
        "delete_store_manager/<int:id>/",
        views.delete_store_manager,
        name="delete_store_manager"
    ),

    path(
        "toggle_store_manager/<int:id>/",
        views.toggle_store_manager,
        name="toggle_store_manager"
    ),


    path(
    "store_manager_profile/",
    views.store_manager_profile,
    name="store_manager_profile"
    ),

    path(
        "quality_inspector_profile/",
        views.quality_inspector_profile,
        name="quality_inspector_profile"
    ),


    path(
        "upload-image/",
        views.upload_image,
        name="upload_image"
    ),

    path(
        "prediction-result/<int:id>/",
        views.prediction_result,
        name="prediction_result"
    ),

    path(
        'prediction_history/',
        views.prediction_history,
        name='prediction_history'
    ),


    # STORE MANAGER REPORTS

    path(
        "inspection-reports/",
        views.inspection_report_list,
        name="inspection_report_list"
    ),

    path(
        "inspection-report/<int:id>/",
        views.inspection_report_detail,
        name="inspection_report_detail"
    ),

    path(
        "verify-report/<int:id>/",
        views.verify_report,
        name="verify_report"
    ),

    path(
        "verify-prediction-history/",
        views.verify_prediction_history,
        name="verify_prediction_history"
    ),

    path(
        "verify-prediction/<int:id>/",
        views.verify_prediction,
        name="verify_prediction"
    ),


     path(
        'admin-view-reports/',
        views.admin_view_reports,
        name='admin_view_reports'
    ),

]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)