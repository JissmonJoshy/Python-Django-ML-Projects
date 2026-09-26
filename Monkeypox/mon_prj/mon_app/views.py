from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
import random
import string
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request,'index.html')


def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # SESSION
            request.session['login_id'] = user.id

            # ADMIN
            if user.is_superuser:
                messages.success(request, "Admin Login Successfully")
                return redirect('admin_dashboard')

            # MVD USER
            elif user.usertype == 'user':
                messages.success(request, "User Login Successfully")
                return redirect('user_dashboard')

            else:
                messages.error(request, "Invalid user type")
                return redirect('login')

        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('login')

    return render(request, 'login.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import re


def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        image = request.FILES.get('image')

        # ---------------- VALIDATION ---------------- #

        if not username or not password:
            messages.error(request, "Username and Password are required")
            return redirect('register')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return redirect('register')

        # Email validation
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            messages.error(request, "Enter a valid email address")
            return redirect('register')

        # Phone validation (10 digits)
        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be 10 digits")
            return redirect('register')

        if not image:
            messages.error(request, "Profile image is required")
            return redirect('register')

        # Check duplicate username
        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # Check duplicate email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        # ---------------- CREATE LOGIN ---------------- #
        login_obj = Login.objects.create_user(
            username=username,
            password=password,
            viewpassword=password
        )
        login_obj.usertype = "user"
        login_obj.viewpassword = password
        login_obj.save()

        # ---------------- CREATE USER ---------------- #
        User.objects.create(
            login=login_obj,
            name=name,
            email=email,
            phone=phone,
            address=address,
            image=image
        )

        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'register.html')



def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')



def user_dashboard(request):
    return render(request, 'user/user_dashboard.html')


def view_users(request):
    users = User.objects.select_related('login').all()
    return render(request, 'admin/view_users.html', {'users': users})


# ---------------- ACTIVATE / DEACTIVATE USER ---------------- #
def toggle_user_status(request, login_id):
    login_obj = get_object_or_404(Login, id=login_id)

    if login_obj.is_active:
        login_obj.is_active = False
        messages.warning(request, "User deactivated successfully")
    else:
        login_obj.is_active = True
        messages.success(request, "User activated successfully")

    login_obj.save()
    return redirect('view_users')


# ---------------- DELETE USER ---------------- #
def delete_user(request, login_id):
    login_obj = get_object_or_404(Login, id=login_id)
    login_obj.delete()
    messages.success(request, "User deleted successfully")
    return redirect('view_users')




def user_profile(request):

    # Get logged-in user from session
    login_id = request.session.get('login_id')

    if not login_id:
        messages.error(request, "Please login first")
        return redirect('login')

    try:
        user_obj = User.objects.get(login_id=login_id)
    except User.DoesNotExist:
        messages.error(request, "User profile not found")
        return redirect('login')

    return render(request, 'user/user_profile.html', {'user': user_obj})



from .ml_model.predict import predict_emotion

def emotion_predict(request):
    result = None

    if request.method == "POST":
        text = request.POST.get("text")
        result = predict_emotion(text)

        # Get logged-in user id from session
        login_id = request.session.get('login_id')

        if login_id:
            user = Login.objects.get(id=login_id)

            # Save to DB
            EmotionHistory.objects.create(
                login=user,
                text=text,
                predicted_emotion=result
            )

    return render(request, "user/emotion.html", {"result": result})


##########################################


from .models import EmotionHistory

def emotion_history(request):
    login_id = request.session.get('login_id')
    history = EmotionHistory.objects.filter(login_id=login_id).order_by('-created_at')

    return render(request, "user/history.html", {"history": history})




from .models import EmotionHistory

def emotion_history(request):
    login_id = request.session.get('login_id')
    history = EmotionHistory.objects.filter(login_id=login_id).order_by('-created_at')

    return render(request, "user/history.html", {"history": history})



def admin_history(request):

    history = EmotionHistory.objects.select_related('login').order_by('-created_at')

    context = {
        'history': history
    }

    return render(request, 'admin/admin_history.html', context)