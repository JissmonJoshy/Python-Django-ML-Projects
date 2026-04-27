"""
URL configuration for Social_media project.

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
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("log/", views.log),
    path("signup/", views.reg),
    path("udp/", views.udp),
    path("user_home/", views.user_home),
    path("admin_home/", views.admin_home),
    path("profile/", views.my_profile),
    path("user_profile/", views.user_profile),
    path("update_user_profile/", views.update_user_profile),
    path("like/", views.like),
    path("follow/", views.follow),
    path("users_profile/", views.users_profile),
    path("common/", views.common),
    path("messages/", views.messageses),
    path("add_to_friend_list/", views.add_to_friend_list),
    path("delete_post/", views.delete_post),
    path("adm_view_user_profile/", views.adm_view_user_profile),
    path("out/", views.out),
    path('delete-post/<int:id>/', views.delete_post, name='delete_post'),
    path('admin_send_message/', views.admin_send_message, name='admin_send_message'),
    path('user_chat/', views.user_chat, name='user_chat'),
    path('send_reply/', views.send_reply, name='send_reply'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)