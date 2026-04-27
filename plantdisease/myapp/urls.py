from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # ===== USER ROUTES =====
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('category/<int:cat_id>/', views.category_products, name='category_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update-cart/', views.update_cart, name='update_cart'), 
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.my_orders_view, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('account/', views.account_view, name='account'),
    path('all-feedback/', views.all_feedback, name='all_feedback'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('feedback/submit/<int:product_id>/', views.submit_feedback, name='submit_feedback'),
    path("predict/", views.crop_predict, name="crop_predict"),
    
    
    # ===== ADMIN ROUTES (Unified Login) =====
    path('admin/login/', RedirectView.as_view(url='/login/', permanent=False), name='admin_login'),
    path('admin/logout/', views.logout, name='admin_logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Admin Users
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/user/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    
    # Admin Orders
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    
    # Admin Feedback
    path('admin/feedback/', views.admin_feedback, name='admin_feedback'),
    path('admin/feedback/<int:feedback_id>/', views.admin_feedback_detail, name='admin_feedback_detail'),
    path('admin/feedback/<int:feedback_id>/delete/', views.admin_delete_feedback, name='admin_delete_feedback'),
    
    # Admin Products
    path('admin/categories/', views.admin_categories, name='admin_categories'),
    path('admin/category/add/', views.admin_categories, name='admin_add_category'),
    path('admin/products/', views.admin_products, name='admin_products'),
    path('admin/product/add/', views.admin_add_product, name='admin_add_product'),
    path('admin/product/<int:product_id>/edit/', views.admin_edit_product, name='admin_edit_product'),
    path('admin/product/<int:product_id>/delete/', views.admin_delete_product, name='admin_delete_product'),
]
