from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
import random
import string
from django.core.mail import send_mail
import os
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Avg


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
                return redirect('login_view')

        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('login')

    return render(request, 'login.html')



def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


def user_dashboard(request):
    return render(request, 'user/user_dashboard.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Login, User


def user_register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        username = request.POST.get("username")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        profile = request.FILES.get("profile")

        # Password Match
        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return redirect("user_register")

        # Username Exists
        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("user_register")

        # Email Exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("user_register")

        # Phone Validation
        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, "Enter a valid 10 digit mobile number.")
            return redirect("user_register")

        login = Login.objects.create_user(
            username=username,
            password=password
        )

        login.usertype = "user"
        login.viewpassword = password
        login.save()

        User.objects.create(
            login=login,
            name=name,
            phone=phone,
            email=email,
            address=address,
            profile=profile
        )

        messages.success(request, "Registration Successful.")
        return redirect("login")

    return render(request, "user_register.html")




def view_users(request):

    data = User.objects.select_related("login").all().order_by("-id")

    return render(request, "admin/view_users.html", {"data": data})


def toggle_user_status(request, id):

    user = get_object_or_404(Login, id=id)

    if user.is_active:
        user.is_active = False
        messages.success(request, "User Deactivated Successfully.")
    else:
        user.is_active = True
        messages.success(request, "User Activated Successfully.")

    user.save()

    return redirect("view_users")


def delete_user(request, id):

    user = get_object_or_404(User, login_id=id)

    login = user.login

    user.delete()
    login.delete()

    messages.success(request, "User Deleted Successfully.")

    return redirect("view_users")



def user_profile(request):

    if 'login_id' not in request.session:
        messages.error(request, "Please login first.")
        return redirect('login')

    try:
        data = User.objects.get(login_id=request.session['login_id'])
    except User.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('login')

    return render(request, "user/user_profile.html", {"data": data})

from .predict import predict_image

def predict_image_view(request):

    if request.method == "POST":

        user = User.objects.get(login=request.user)

        img = request.FILES['image']

        from django.core.files.storage import FileSystemStorage

        fs = FileSystemStorage()

        filename = fs.save("predictions/" + img.name, img)

        filepath = fs.path(filename)

        label, confidence = predict_image(filepath)

        history = PredictionHistory.objects.create(
            user=user,
            image=filename,
            prediction=label,
            confidence=round(confidence * 100, 2)
        )

        return render(request,
                      "user/predict_image.html",
                      {"history": history})

    return render(request, "user/predict_image.html")



def prediction_history(request):

    user=User.objects.get(login=request.user)

    history=PredictionHistory.objects.filter(
        user=user
    ).order_by("-date")

    return render(
        request,
        "user/prediction_history.html",
        {"history":history}
    )



def admin_view_history(request):

    if not request.user.is_superuser:
        return redirect("login")

    history = PredictionHistory.objects.select_related(
        "user",
        "user__login"
    ).order_by("-date")

    context = {
        "history": history,
        "total_predictions": history.count(),
        "real_count": history.filter(prediction__iexact="Real").count(),
        "fake_count": history.filter(prediction__iexact="Fake").count(),
    }

    return render(request, "admin/admin_view_history.html", context)