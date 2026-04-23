"""
URL configuration for crop_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from crop_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),

    path('login/',views.login_view,name='login'),
    path('farmer_register/', views.farmer_register, name='farmer_register'),
    path('buyer_register/', views.buyer_register, name='buyer_register'),

    path('adm/',views.adm,name='adm'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('farmerhome/',views.farmerhome,name='farmerhome'),
    path('buyerhome/',views.buyerhome,name='buyerhome'),
    path('governmentofficerhome/',views.governmentofficerhome,name='governmentofficerhome'),
    path('deliveryboyhome/',views.deliveryboyhome,name='deliveryboyhome'),


    path('admin_farmers/', views.admin_farmers, name='admin_farmers'),
    path('admin_buyers/', views.admin_buyers, name='admin_buyers'),
    path('approve_farmer/<int:id>/', views.approve_farmer, name='approve_farmer'),
    path('reject_farmer/<int:id>/', views.reject_farmer, name='reject_farmer'),
    path('reject_buyer/<int:id>/', views.reject_buyer, name='reject_buyer'),

    path('farmer_profile/', views.farmer_profile, name='farmer_profile'),
    path('edit_farmer_profile/', views.edit_farmer_profile, name='edit_farmer_profile'),
    path('buyer_profile/', views.buyer_profile, name='buyer_profile'),
    path('edit_buyer_profile/', views.edit_buyer_profile, name='edit_buyer_profile'),

    path('admin_add_officer/', views.admin_add_officer, name='admin_add_officer'),
    path('admin_view_officers/', views.admin_view_officers, name='admin_view_officers'),
    path('admin_delete_officer/<int:id>/', views.admin_delete_officer, name='admin_delete_officer'),
    path('admin_edit_officer/<int:id>/', views.admin_edit_officer, name='admin_edit_officer'),

    path('officer_profile/', views.officer_profile, name='officer_profile'),
    path('edit_officer_profile/', views.edit_officer_profile, name='edit_officer_profile'),

    path('officer_add_seeds_fertilisers/', views.officer_add_seeds_fertilisers, name='officer_add_seeds_fertilisers'),
    path('officer_view_seeds_fertilisers/', views.officer_view_seeds_fertilisers, name='officer_view_seeds_fertilisers'),
    path('officer_edit_seeds_fertilisers/<int:id>/', views.officer_edit_seeds_fertilisers, name='officer_edit_seeds_fertilisers'),
    path('officer_delete_seeds_fertilisers/<int:id>/', views.officer_delete_seeds_fertilisers, name='officer_delete_seeds_fertilisers'),

    path('admin_seeds_fertilisers/', views.admin_seeds_fertilisers, name='admin_seeds_fertilisers'),
    path('farmer_view_seeds_fertilisers/',views.farmer_view_seeds_fertilisers,name='farmer_view_seeds_fertilisers'),

    path('farmer_add_to_cart<int:pid>/', views.farmer_add_to_cart, name='farmer_add_to_cart'),
    path('farmer_cart/', views.farmer_cart, name='farmer_cart'),
    path('farmer_payment/', views.farmer_payment, name='farmer_payment'),
    path('update_cart_quantity/<int:cid>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('delete_cart_item/<int:cid>/', views.delete_cart_item, name='delete_cart_item'),
    path('farmer_orders/', views.farmer_orders, name='farmer_orders'),

    path('admin_add_delivery_boy/', views.admin_add_delivery_boy, name='admin_add_delivery_boy'),
    path('admin_delivery_boy/', views.admin_delivery_boy, name='admin_delivery_boy'),
    path('edit_delivery_boy/<int:id>/', views.edit_delivery_boy, name='edit_delivery_boy'),
    path('delete_delivery_boy/<int:id>/', views.delete_delivery_boy, name='delete_delivery_boy'),

    path('delivery_profile/', views.deliveryboy_profile, name='deliveryboy_profile'),
    path('edit_deliveryboy_profile/', views.edit_deliveryboy_profile, name='edit_deliveryboy_profile'),

    path('admin_assign_delivery/', views.admin_assign_delivery, name='admin_assign_delivery'),
    path('assign_delivery_boy/<int:oid>/', views.assign_delivery_boy, name='assign_delivery_boy'),
    path('assigned_seeds_fertilisers_deliveryboy/',views.assigned_seeds_fertilisers_deliveryboy,name='assigned_seeds_fertilisers_deliveryboy'),
    path('deliveryboy_mark_delivered/<int:cid>/',views.deliveryboy_mark_delivered,name='deliveryboy_mark_delivered'),
    path('add_product/', views.add_product, name='add_product'),
    path('view_my_products/', views.view_my_products, name='view_my_products'),
    path('edit_product/<int:pid>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:pid>/', views.delete_product, name='delete_product'),

    path('buyer_product_list/', views.buyer_product_list, name='buyer_product_list'),

    path('add_to_cart/<int:pid>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('increase_cart_quantity/<int:cid>/', views.increase_cart_quantity, name='increase_cart_quantity'),
    path('decrease_cart_quantity/<int:cid>/', views.decrease_cart_quantity, name='decrease_cart_quantity'),
    path('remove_from_cart/<int:cid>/', views.remove_from_cart, name='remove_from_cart'),
    path('products_payment/', views.products_payment, name='products_payment'),
    path('buyer_product_orders/', views.buyer_product_orders, name='buyer_product_orders'),
    path('admin-assign-delivery/',views.admin_products_assign_delivery,name='admin_products_assign_delivery'),
    
    path('assigned_products_deliveryboy/',views.assigned_products_deliveryboy,name='assigned_products_deliveryboy'),

    path('mark_products_delivered/<int:cart_id>/',views.mark_products_delivered,name='mark_products_delivered'),

    path('product_feedback/<int:cart_id>/', views.product_feedback, name='product_feedback'),
    path('farmer_product_feedbacks/', views.farmer_product_feedbacks, name='farmer_product_feedbacks'),
    path('admin_product_feedbacks/', views.admin_product_feedbacks, name='admin_product_feedbacks'),
    path('add_seed_feedback/<int:oid>/',views.add_seed_feedback,name='add_seed_feedback'),
    path('admin_seed_feedback/',views.admin_seed_feedback,name='admin_seed_feedback'),
    path('officer_seed_feedback/',views.officer_seed_feedback,name='officer_seed_feedback'),
    path('officer_chat/', views.officer_chat, name='officer_chat'),
    path('farmer_chat/', views.farmer_chat, name='farmer_chat'),

    path('update_delivery_status/<int:cart_id>/',views.update_delivery_status,name='update_delivery_status'),
    path('update_seed_delivery_status/<int:cid>/',views.update_seed_delivery_status,name='update_seed_delivery_status'),

    path('add_farming_alert',views.add_farming_alert,name='add_farming_alert'),
    path('view_farming_alerts/', views.view_farming_alerts, name='view_farming_alerts'),
    path('edit_farming_alert/<int:alert_id>/', views.edit_farming_alert, name='edit_farming_alert'),
    path('delete_farming_alert/<int:alert_id>/', views.delete_farming_alert, name='delete_farming_alert'),
    # urls.py

    path('farmer_view_farming_alerts/', views.farmer_view_farming_alerts, name='farmer_view_farming_alerts'),
    # urls.py

    path('admin_products/', views.admin_products, name='admin_products'),
    path('predict-disease/', views.predict_crop_disease, name='predict_disease'),



    
   
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

