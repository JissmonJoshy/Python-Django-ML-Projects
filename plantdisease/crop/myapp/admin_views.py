from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q, Count, Avg
from .models import User, Product, Category, Order, OrderItem, Feedback
import json


# ========== ADMIN LOGIN ==========
def admin_login(request):
    """Admin login page"""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        try:
            user = User.objects.get(username=username)
            
            # Check if user is staff (admin)
            if not user.is_staff:
                messages.error(request, "Access denied. You are not an admin.")
                return redirect("admin_login")
            
            # Verify password
            if check_password(password, user.password):
                request.session["admin_id"] = user.id
                request.session["admin_name"] = user.name
                request.session["is_admin"] = True
                messages.success(request, f"Welcome back, {user.name}!")
                return redirect("admin_dashboard")
            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "Admin username not found")

    return render(request, "admin/admin_login.html")


def admin_logout(request):
    """Admin logout"""
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect("admin_login")


def check_admin(view_func):
    """Decorator to check if user is logged in as admin"""
    def wrapper(request, *args, **kwargs):
        if "admin_id" not in request.session or not request.session.get("is_admin"):
            messages.error(request, "Please login as admin first")
            return redirect("admin_login")
        return view_func(request, *args, **kwargs)
    return wrapper


# ========== ADMIN DASHBOARD ==========
@check_admin
def admin_dashboard(request):
    """Main admin dashboard with statistics"""
    total_users = User.objects.filter(is_staff=False).count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_feedback = Feedback.objects.count()
    
    # Calculate revenue
    total_revenue = sum(order.total_price for order in Order.objects.all())
    
    # Recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    
    # Pending orders
    pending_orders = Order.objects.filter(status="Pending").count()
    
    # Recent feedback
    recent_feedback = Feedback.objects.all().order_by('-created_at')[:5]
    
    # Average product rating
    avg_rating = Feedback.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        'admin_name': request.session.get('admin_name'),
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_feedback': total_feedback,
        'total_revenue': f"₹{total_revenue:,.2f}",
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
        'recent_feedback': recent_feedback,
        'avg_rating': f"{avg_rating:.1f}",
    }
    
    return render(request, "admin/admin_dashboard.html", context)


# ========== USER MANAGEMENT ==========
@check_admin
def admin_users(request):
    """View all users with search functionality"""
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        users = User.objects.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(number__icontains=search_query)
        ).filter(is_staff=False)
    else:
        users = User.objects.filter(is_staff=False).order_by('-date_joined')
    
    context = {
        'users': users,
        'search_query': search_query,
        'admin_name': request.session.get('admin_name'),
    }
    
    return render(request, "admin/admin_users.html", context)


@check_admin
def admin_user_detail(request, user_id):
    """View user details and their orders"""
    user = get_object_or_404(User, id=user_id, is_staff=False)
    orders = Order.objects.filter(user=user).order_by('-created_at')
    feedbacks = Feedback.objects.filter(user=user).order_by('-created_at')
    
    # User statistics
    total_orders = orders.count()
    total_spent = sum(order.total_price for order in orders)
    
    context = {
        'user': user,
        'orders': orders,
        'feedbacks': feedbacks,
        'total_orders': total_orders,
        'total_spent': f"₹{total_spent:,.2f}",
        'admin_name': request.session.get('admin_name'),
    }
    
    return render(request, "admin/admin_user_detail.html", context)


# ========== ORDER MANAGEMENT ==========
@check_admin
def admin_orders(request):
    """View all orders with filtering"""
    status_filter = request.GET.get('status', '').strip()
    search_query = request.GET.get('search', '').strip()
    
    orders = Order.objects.all().order_by('-created_at')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    if search_query:
        orders = orders.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(id__icontains=search_query)
        )
    
    # Get unique statuses for filter
    statuses = Order.objects.values_list('status', flat=True).distinct()
    
    context = {
        'orders': orders,
        'statuses': statuses,
        'status_filter': status_filter,
        'search_query': search_query,
        'admin_name': request.session.get('admin_name'),
    }
    
    return render(request, "admin/admin_orders.html", context)


@check_admin
def admin_order_detail(request, order_id):
    """View detailed order information"""
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()
    
    if request.method == "POST":
        new_status = request.POST.get('status', '').strip()
        if new_status:
            order.status = new_status
            order.save()
            messages.success(request, f"Order status updated to {new_status}")
            return redirect("admin_order_detail", order_id=order.id)
    
    statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
    
    context = {
        'order': order,
        'items': items,
        'statuses': statuses,
        'admin_name': request.session.get('admin_name'),
    }
    
    return render(request, "admin/admin_order_detail.html", context)


# ========== FEEDBACK MANAGEMENT ==========
@check_admin
def admin_feedback(request):
    """View all product feedback with filtering"""
    product_filter = request.GET.get('product', '').strip()
    rating_filter = request.GET.get('rating', '').strip()
    search_query = request.GET.get('search', '').strip()
    
    feedback_list = Feedback.objects.all().order_by('-created_at')
    
    if product_filter:
        feedback_list = feedback_list.filter(product_id=product_filter)
    
    if rating_filter:
        try:
            feedback_list = feedback_list.filter(rating=int(rating_filter))
        except ValueError:
            pass
    
    if search_query:
        feedback_list = feedback_list.filter(
            Q(user__name__icontains=search_query) |
            Q(product__name__icontains=search_query) |
            Q(comment__icontains=search_query)
        )
    
    # Get products for filter
    products = Product.objects.all().order_by('name')
    
    context = {
        'feedback_list': feedback_list,
        'products': products,
        'product_filter': product_filter,
        'rating_filter': rating_filter,
        'search_query': search_query,
        'admin_name': request.session.get('admin_name'),
    }
    
    return render(request, "admin/admin_feedback.html", context)


@check_admin
def admin_feedback_detail(request, feedback_id):
    """View feedback detail"""
    feedback = get_object_or_404(Feedback, id=feedback_id)
    
    context = {
        'feedback': feedback,
        'admin_name': request.session.get('admin_name'),
    }
    
    return render(request, "admin/admin_feedback_detail.html", context)


@check_admin
def admin_delete_feedback(request, feedback_id):
    """Delete feedback"""
    feedback = get_object_or_404(Feedback, id=feedback_id)
    product_name = feedback.product.name
    feedback.delete()
    messages.success(request, f"Feedback on {product_name} has been deleted.")
    return redirect("admin_feedback")


# ========== PRODUCT MANAGEMENT ==========
@check_admin
def admin_products(request):
    """View all products with search"""
    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '').strip()
    
    products = Product.objects.all().order_by('-created_at')
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'admin_name': request.session.get('admin_name'),
    }
    
    return render(request, "admin/admin_products.html", context)


@check_admin
def admin_add_product(request):
    """Add new product"""
    categories = Category.objects.all()
    
    if request.method == "POST":
        try:
            category_id = request.POST.get('category')
            name = request.POST.get('name', '').strip()
            weight = request.POST.get('weight', '').strip()
            price = request.POST.get('price', '')
            manufacture_date = request.POST.get('manufacture_date')
            expiry_date = request.POST.get('expiry_date')
            quantity = request.POST.get('quantity', '')
            image = request.FILES.get('image')
            
            # Validation
            if not all([name, weight, price, manufacture_date, expiry_date, quantity, category_id, image]):
                messages.error(request, "All fields are required")
                return redirect("admin_add_product")
            
            category = get_object_or_404(Category, id=category_id)
            
            product = Product(
                category=category,
                name=name,
                weight=weight,
                price=float(price),
                manufacture_date=manufacture_date,
                expiry_date=expiry_date,
                quantity=int(quantity),
                image=image
            )
            product.save()
            messages.success(request, f"Product '{name}' added successfully!")
            return redirect("admin_products")
        
        except Exception as e:
            messages.error(request, f"Error adding product: {str(e)}")
    
    context = {
        'categories': categories,
        'admin_name': request.session.get('admin_name'),
    }
    
    return render(request, "admin/admin_add_product.html", context)


@check_admin
def admin_edit_product(request, product_id):
    """Edit existing product"""
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    
    if request.method == "POST":
        try:
            product.category_id = request.POST.get('category', product.category_id)
            product.name = request.POST.get('name', product.name).strip()
            product.weight = request.POST.get('weight', product.weight).strip()
            product.price = float(request.POST.get('price', product.price))
            product.manufacture_date = request.POST.get('manufacture_date', product.manufacture_date)
            product.expiry_date = request.POST.get('expiry_date', product.expiry_date)
            product.quantity = int(request.POST.get('quantity', product.quantity))
            
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            
            product.save()
            messages.success(request, f"Product '{product.name}' updated successfully!")
            return redirect("admin_products")
        
        except Exception as e:
            messages.error(request, f"Error updating product: {str(e)}")
    
    context = {
        'product': product,
        'categories': categories,
        'admin_name': request.session.get('admin_name'),
    }
    
    return render(request, "admin/admin_edit_product.html", context)


@check_admin
def admin_delete_product(request, product_id):
    """Delete product"""
    product = get_object_or_404(Product, id=product_id)
    product_name = product.name
    product.delete()
    messages.success(request, f"Product '{product_name}' has been deleted.")
    return redirect("admin_products")
