"""
URL configuration for hotel_prj project.

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
from django import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from hotel_prj import settings
from hotel_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('club_manager_dashboard/', views.club_manager_dashboard, name='club_manager_dashboard'),
    path(
        "register_club_manager/",
        views.register_club_manager,
        name="register_club_manager"
    ),

    path(
        "admin_view_club_manager/",
        views.admin_view_club_manager,
        name="admin_view_club_manager"
    ),

    path(
        "admin_toggle_club_manager/<int:id>/",
        views.admin_toggle_club_manager,
        name="admin_toggle_club_manager"
    ),

    path(
        "admin_delete_club_manager/<int:id>/",
        views.admin_delete_club_manager,
        name="admin_delete_club_manager"
    ),

    path(
    "register_scout/",
    views.register_scout,
    name="register_scout"
    ),


    path(
    "toggle_scout/<int:id>/",
    views.toggle_scout,
    name="toggle_scout"
    ),

    path(
        "delete_scout/<int:id>/",
        views.delete_scout,
        name="delete_scout"
    ),

    path(
        "scout_dashboard/",
        views.scout_dashboard,
        name="scout_dashboard"
    ),


    path(
    "club_manager_profile/",
    views.club_manager_profile,
    name="club_manager_profile"
    ),

    path(
        "scout_profile/",
        views.scout_profile,
        name="scout_profile"
    ),

    path(
    "admin_view_scouts/",
    views.admin_view_scouts,
    name="admin_view_scouts"
    ),

    path(
        "admin_toggle_scout/<int:id>/",
        views.admin_toggle_scout,
        name="admin_toggle_scout"
    ),

    path(
        "admin_delete_scout/<int:id>/",
        views.admin_delete_scout,
        name="admin_delete_scout"
    ),
    
    path('performance_prediction/', views.performance_prediction, name='performance_prediction'),

    path(
    "similar_player/",
    views.similar_player_recommendation,
    name="similar_player"
    ),

    path(
        "search_players/",
        views.search_players,
        name="search_players"
    ),
    
    path(
    "recruitment_recommendation/",
    views.recruitment_recommendation,
    name="recruitment_recommendation"
    ),

    path(
    "admin_stats/",
    views.admin_stats,
    name="admin_stats"
    ),

    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)