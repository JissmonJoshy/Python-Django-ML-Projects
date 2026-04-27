from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    # ===== USER ROUTES =====
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('category/<int:cat_id>/', views.category_products, name='category_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # new
    path('cart/', views.view_cart, name='view_cart'),  # optional cart view
    path('update-cart/', views.update_cart, name='update_cart'), 
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.my_orders_view, name='my_orders'), # <--- ADD THIS
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('account/', views.account_view, name='account'),
    path('all-feedback/', views.all_feedback, name='all_feedback'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('feedback/submit/<int:product_id>/', views.submit_feedback, name='submit_feedback'),
    
    # ===== ADMIN ROUTES =====
    path('admin/login/', admin_views.admin_login, name='admin_login'),
    path('admin/logout/', admin_views.admin_logout, name='admin_logout'),
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Admin Users
    path('admin/users/', admin_views.admin_users, name='admin_users'),
    path('admin/user/<int:user_id>/', admin_views.admin_user_detail, name='admin_user_detail'),
    
    # Admin Orders
    path('admin/orders/', admin_views.admin_orders, name='admin_orders'),
    path('admin/order/<int:order_id>/', admin_views.admin_order_detail, name='admin_order_detail'),
    
    # Admin Feedback
    path('admin/feedback/', admin_views.admin_feedback, name='admin_feedback'),
    path('admin/feedback/<int:feedback_id>/', admin_views.admin_feedback_detail, name='admin_feedback_detail'),
    path('admin/feedback/<int:feedback_id>/delete/', admin_views.admin_delete_feedback, name='admin_delete_feedback'),
    
    # Admin Products
    path('admin/products/', admin_views.admin_products, name='admin_products'),
    path('admin/product/add/', admin_views.admin_add_product, name='admin_add_product'),
    path('admin/product/<int:product_id>/edit/', admin_views.admin_edit_product, name='admin_edit_product'),
    path('admin/product/<int:product_id>/delete/', admin_views.admin_delete_product, name='admin_delete_product'),
]
