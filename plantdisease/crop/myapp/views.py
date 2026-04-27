from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Avg
from .models import User, Product, Category, Order, OrderItem, Cart, CartItem, Feedback

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


# Login
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        if check_password(password, user.password):
            request.session["user_id"] = user.id
            request.session["user_name"] = user.name
            return redirect("home")
        else:
            messages.error(request, "Invalid password")
            return redirect("login")

    return render(request, "login.html")


# Home
from django.shortcuts import render, redirect
from .models import Category

def home(request):
    if "user_id" not in request.session:
        return redirect("login")

    categories = Category.objects.all()

    return render(request, "home.html", {
        "name": request.session["user_name"],
        "categories": categories
    })



# Logout
def logout(request):
    request.session.flush()
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
            OrderItem.objects.create(
                order=order,
                product_id=int(key),
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


