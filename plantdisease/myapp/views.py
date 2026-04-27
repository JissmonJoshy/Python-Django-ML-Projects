from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Avg, Q, Count
from .models import User, Product, Category, Order, OrderItem, Cart, CartItem, Feedback
import json

# Register
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        number = request.POST.get("number")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        user = User(
            name=name,
            email=email,
            number=number,
            password=make_password(password)
        )
        user.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "register.html")


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from .models import User   # If using custom user model


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        # Check password
        if not check_password(password, user.password):
            messages.error(request, "Incorrect password")
            return redirect("login")

        # If admin -> go to admin dashboard
        if user.is_staff:
            request.session["admin_id"] = user.id
            request.session["admin_name"] = user.name
            messages.success(request, "Admin login successful")
            return redirect("/admin/dashboard/")

        # If normal user -> go to user home
        request.session["user_id"] = user.id
        request.session["user_name"] = user.name
        messages.success(request, f"Welcome, {user.name}!")
        return redirect("home")

    return render(request, "login.html")



# Home
from django.shortcuts import render, redirect
from .models import Category

def home(request):
    if "user_id" not in request.session:
        return redirect("login")

    categories = Category.objects.all()

    return render(request, "home_new.html", {
        "name": request.session["user_name"],
        "categories": categories
    })



# Logout (Unified for both User and Admin)
def logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect("login")


from django.shortcuts import render, get_object_or_404
from .models import Category

def category_products(request, cat_id):
    category = get_object_or_404(Category, id=cat_id)
    products = category.products.all()  # Related name from Product model
    return render(request, 'product_list.html', {'category': category, 'products': products})


from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

# myapp/views.py

from django.shortcuts import get_object_or_404, redirect

# Note: The view you provided uses session-based cart, which is what I'm updating below.

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    # --- START: Updated logic to handle quantity from POST request ---
    if request.method == 'POST':
        try:
            # Get the quantity from the form, default to 1 if not provided or invalid
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1 # Ensure quantity is at least 1
        except ValueError:
            quantity = 1 # Fallback if input is not a valid number
    else:
        # If the view is accessed via GET (shouldn't happen with form), default to 1
        quantity = 1
    # --- END: Updated logic ---

    # If product already in cart, increase quantity
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity,
            'image': product.image.url
        }

    request.session['cart'] = cart
    request.session.modified = True
    
    # You might want to redirect back to the product detail page or the cart page
    return redirect('view_cart') # Keep redirecting to cart page as in your original code


def view_cart(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'cart.html', {'cart': cart, 'total': total})

def update_cart(request):
    if request.method == "POST":
        cart = request.session.get('cart', {})

        for key in list(cart.keys()):
            quantity = request.POST.get(f'quantity_{key}')
            remove = request.POST.get(f'remove_{key}')

            if remove:  # If checked, remove the item
                cart.pop(key)
            elif quantity:  # Update quantity
                try:
                    qty = int(quantity)
                    if qty > 0:
                        cart[key]['quantity'] = qty
                    else:
                        cart.pop(key)  # Remove if quantity set to 0
                except ValueError:
                    pass  # Ignore invalid input

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('view_cart')

from django.shortcuts import render, redirect
from .models import Order, OrderItem, User

def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart')

    total = sum(item['price'] * item['quantity'] for item in cart.values())

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Get the logged-in user if available
        user = None
        if "user_id" in request.session:
            try:
                user = User.objects.get(id=request.session.get("user_id"))
            except User.DoesNotExist:
                pass

        order = Order.objects.create(
            user=user,  # Link the order to the logged-in user
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            total_price=total
        )

        for key, item in cart.items():
            product = get_object_or_404(Product, id=int(key))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )

        request.session['cart'] = {}
        request.session.modified = True

        return render(request, 'order_success.html', {'order': order})

    # GET request → show order page
    return render(request, 'place_order.html', {'cart': cart, 'total': total})

# In your_app/views.py

from django.shortcuts import render, get_object_or_404
from .models import Order # Assuming your model is in the same app

# myapp/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from .models import Order, OrderItem, Product, User # Ensure Product is imported for restock logic

# --- Existing Order Detail View ---
def order_detail(request, order_id):
    # Check if user is logged in via session
    if "user_id" not in request.session:
        messages.error(request, "Please log in to view order details.")
        return redirect("login")
    
    order = get_object_or_404(Order, pk=order_id)
    
    # Optional: Security check - verify the order belongs to the session user
    # (Skip if order has no associated user - guest checkout)
    if order.user and order.user.id != request.session.get("user_id"):
        messages.error(request, "Permission denied to view this order.")
        return redirect("home")
    
    context = {'order': order}
    return render(request, 'order_detail.html', context)


# --- NEW: My Orders List View ---
def my_orders_view(request):
    """
    Shows a list of all orders placed by the current logged-in user.
    Uses session-based authentication.
    """
    # Check if user is logged in via session
    if "user_id" not in request.session:
        messages.info(request, "Please log in to view your orders.")
        return redirect("login")

    # Get the logged-in user from session
    user_id = request.session.get("user_id")
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.flush()
        messages.error(request, "User not found. Please log in again.")
        return redirect("login")

    # Filter orders by the current user and order by creation date (newest first)
    orders = Order.objects.filter(user=user).order_by('-created_at')
    
    context = {
        'orders': orders,
        'user_name': user.name
    }
    return render(request, 'my_orders.html', context)


# --- Existing Cancel Order View (Updated with Restock Logic) ---
def cancel_order(request, order_id):
    # Check if user is logged in via session
    if "user_id" not in request.session:
        messages.error(request, "Please log in to cancel an order.")
        return redirect("login")
    
    order = get_object_or_404(Order, pk=order_id)
    
    # Security Check (Ensure logged-in user owns the order)
    if order.user and order.user.id != request.session.get("user_id"):
        messages.error(request, "Permission denied to cancel this order.")
        return redirect("order_detail", order_id=order.id)
        
    if request.method == 'POST':
        if order.status == 'Pending':
            order.status = 'Cancelled'
            order.save()
            
            # --- RESTOCK LOGIC ---
            for item in order.items.all():
                if item.product:
                    item.product.quantity += item.quantity
                    item.product.save()
            # ---------------------
            
            messages.success(request, f"Order #{order.id} has been successfully cancelled and items restocked.")
        else:
            messages.error(request, f"Order cannot be cancelled because its status is {order.status}.")
            
    return redirect("order_detail", order_id=order.id)


# --- Account View ---
def account_view(request):
    """
    Display and edit user account details.
    Uses session-based authentication.
    """
    # Check if user is logged in via session
    if "user_id" not in request.session:
        messages.error(request, "Please log in to access your account.")
        return redirect("login")

    # Get the logged-in user from session
    user_id = request.session.get("user_id")
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.flush()
        messages.error(request, "User not found. Please log in again.")
        return redirect("login")

    if request.method == "POST":
        # Update user details
        user.name = request.POST.get('name', user.name)
        user.email = request.POST.get('email', user.email)
        user.number = request.POST.get('number', user.number)
        
        # Handle password change if provided
        new_password = request.POST.get('new_password', '')
        if new_password:
            old_password = request.POST.get('old_password', '')
            if check_password(old_password, user.password):
                user.password = make_password(new_password)
                messages.success(request, "Password updated successfully!")
            else:
                messages.error(request, "Old password is incorrect.")
                return render(request, 'account.html', {'user': user})
        
        user.save()
        
        # Update session name if it was changed
        request.session["user_name"] = user.name
        request.session.modified = True
        
        messages.success(request, "Account details updated successfully!")
        return redirect("account")

    context = {'user': user}
    return render(request, 'account.html', context)


# --- Feedback Views ---
def all_feedback(request):
    """
    Show all feedback from all products (accessible from navbar).
    """
    # Get current user from session
    user = None
    if "user_id" in request.session:
        try:
            user = User.objects.get(id=request.session["user_id"])
        except User.DoesNotExist:
            pass
    
    # Get all feedback ordered by most recent
    feedbacks = Feedback.objects.all().order_by('-created_at')
    
    # Calculate overall stats
    total_feedback = feedbacks.count()
    avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        'feedbacks': feedbacks,
        'avg_rating': round(avg_rating, 1),
        'total_feedback': total_feedback,
        'user': user,
        'is_all_feedback': True
    }
    return render(request, 'all_feedback.html', context)


def feedback_list(request):
    """
    Show feedback for a specific product.
    """
    product_id = request.GET.get('product_id')
    if not product_id:
        messages.error(request, "No product specified.")
        return redirect("home")
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect("home")
    
    feedbacks = Feedback.objects.filter(product=product).order_by('-created_at')
    avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Get current user from session
    user = None
    if "user_id" in request.session:
        try:
            user = User.objects.get(id=request.session["user_id"])
        except User.DoesNotExist:
            pass
    
    context = {
        'product': product,
        'feedbacks': feedbacks,
        'avg_rating': round(avg_rating, 1),
        'total_reviews': feedbacks.count(),
        'user': user
    }
    return render(request, 'feedback_list.html', context)


def submit_feedback(request, product_id):
    """
    Submit or update feedback for a product.
    """
    # Check if user is logged in via session
    if "user_id" not in request.session:
        messages.error(request, "Please log in to submit feedback.")
        return redirect("login")
    
    # Get the logged-in user
    user_id = request.session.get("user_id")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.flush()
        messages.error(request, "User not found. Please log in again.")
        return redirect("login")
    
    # Get the product
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect("home")
    
    if request.method == "POST":
        rating = request.POST.get('rating', 5)
        comment = request.POST.get('comment', '')
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                rating = 5
        except ValueError:
            rating = 5
        
        # Create or update feedback
        feedback, created = Feedback.objects.update_or_create(
            user=user,
            product=product,
            defaults={
                'rating': rating,
                'comment': comment
            }
        )
        
        if created:
            messages.success(request, "Thank you! Your feedback has been submitted.")
        else:
            messages.success(request, "Your feedback has been updated.")
        
        redirect_url = reverse('feedback_list') + f"?product_id={product_id}"
        return redirect(redirect_url)
    
    # GET request - show feedback form
    existing_feedback = Feedback.objects.filter(user=user, product=product).first()
    
    context = {
        'product': product,
        'existing_feedback': existing_feedback
    }
    return render(request, 'submit_feedback.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

def check_admin(view_func):
    """Decorator - no authentication required (admin pages are now public)"""
    def wrapper(request, *args, **kwargs):
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
        'admin_name': request.session.get('admin_name', 'Admin'),
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
        'admin_name': request.session.get('admin_name', 'Admin'),
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
        'admin_name': request.session.get('admin_name', 'Admin'),
    }
    
    return render(request, "admin/admin_user_detail.html", context)


# ========== ORDER MANAGEMENT ==========
@check_admin
def admin_orders(request):
    """View all orders with filtering and status update"""
    # Handle inline status update
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status', '').strip()
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order_id} status updated to {new_status}")
        except Order.DoesNotExist:
            messages.error(request, "Order not found")
        return redirect("admin_orders")
    
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
    all_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
    
    context = {
        'orders': orders,
        'statuses': statuses,
        'all_statuses': all_statuses,
        'status_filter': status_filter,
        'search_query': search_query,
        'admin_name': request.session.get('admin_name', 'Admin'),
    }
    
    return render(request, "admin/admin_orders.html", context)


@check_admin
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
        'admin_name': request.session.get('admin_name', 'Admin'),
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
        'admin_name': request.session.get('admin_name', 'Admin'),
    }
    
    return render(request, "admin/admin_feedback.html", context)


@check_admin
def admin_feedback_detail(request, feedback_id):
    """View feedback detail"""
    feedback = get_object_or_404(Feedback, id=feedback_id)
    
    context = {
        'feedback': feedback,
        'admin_name': request.session.get('admin_name', 'Admin'),
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


# ========== PRODUCTS MANAGEMENT ==========
@check_admin
def admin_categories(request):
    """View and manage product categories"""
    # Handle POST request to add category
    if request.method == "POST":
        try:
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()
            image = request.FILES.get('image')
            
            if not all([name, description, image]):
                messages.error(request, "All fields are required")
                return redirect("admin_categories")
            
            # Create category
            category = Category(
                name=name,
                description=description,
                image=image
            )
            category.save()
            messages.success(request, f"Category '{name}' added successfully!")
            return redirect("admin_categories")
        except Exception as e:
            messages.error(request, f"Error adding category: {str(e)}")
            return redirect("admin_categories")
    
    search_query = request.GET.get('search', '').strip()
    categories = Category.objects.all().order_by('-id')
    
    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Get product count for each category
    category_stats = []
    for cat in categories:
        product_count = cat.products.count()
        category_stats.append({
            'category': cat,
            'product_count': product_count
        })
    
    context = {
        'category_stats': category_stats,
        'search_query': search_query,
        'admin_name': request.session.get('admin_name', 'Admin'),
        'total_categories': Category.objects.count(),
    }
    
    return render(request, "admin/admin_categories.html", context)


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
        'admin_name': request.session.get('admin_name', 'Admin'),
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
        'admin_name': request.session.get('admin_name', 'Admin'),
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
        'admin_name': request.session.get('admin_name', 'Admin'),
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




    # Optionally log or raise error when accessing predict route

def crop_predict(request):
    result = None
    error = None
    if request.method == "POST":
        import ui
        # try:
        #     temp = float(request.POST.get("temperature"))
        #     hum = float(request.POST.get("humidity"))
        #     rain = float(request.POST.get("rainfall"))
        #     if model is None:
        #         error = "Model not found. Please train and place trained_model.pkl in myapp/ml/"
        #     else:
        #         pred = model.predict([[temp, hum, rain]])
        #         result = pred[0]
        # except Exception as e:
        #     error = str(e)

    return render(request, "predict.html", {"result": result, "error": error})



