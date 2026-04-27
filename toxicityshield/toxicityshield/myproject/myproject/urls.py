"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
     path('sample',views.sample),
     path('as',views.index),
     path('profile/',views.profile),
     path('notification/',views.notification),
     path('',views.login),
     path('login/',views.login),
     path('register_user/',views.register_user),
     path('user_home/',views.user_home),
     path('update_profile/',views.update_profile),
     path('add_post/',views.add_post),
     path('view_post/',views.view_post),
     path('delete_post/',views.delete_post),
     path('admin_home/',views.admin_home),
     path('add_catetaker/',views.add_catetaker),
     path('view_catetaker/',views.view_catetaker),
     path('care_delete/',views.care_delete),
     path('chat/',views.chat),
     path('caretaker_home/',views.caretaker_home),
     path('reply/',views.reply),
     path('view_user/',views.view_user),
     path('feed_back/',views.feedback),
     path('chatbot/',views.chatbot),
     path('chat_caretaker/',views.chat_caretaker),
     path('pay/',views.pay),
     path('payment/<int:id>/',views.payment,name="payment"),
     path('view_feed_back/',views.view_feed_back),
     path('view_payment_paisa/',views.view_payment_paisa),
     path('send_counseling_message/',views.send_counseling_message),
     path('add_comment/', views.add_comment, name='add_comment'),
     path('post_chat/', views.post_chat, name='post_chat'),
    
#   path('send_counseling_message/<int:user_id>/', views.send_counseling_message, name='send_counseling_message'),

]
