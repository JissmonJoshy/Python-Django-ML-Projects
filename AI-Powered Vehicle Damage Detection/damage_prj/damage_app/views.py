from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
import random
import string
from django.core.mail import send_mail
import os


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
            
            elif user.usertype == 'insurance':
                messages.success(request, "Insurance Assessor Login Successfully")
                return redirect('insurance_dashboard')

            else:
                messages.error(request, "Invalid user type")
                return redirect('login_view')

        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('login_view')

    return render(request, 'login.html')






def user_register(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        profile_pic = request.FILES.get('profile_pic')

        # VALIDATIONS
        if not username or not password:
            messages.error(request, "Username and password required")
            return redirect('user_register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('user_register')

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('user_register')  

        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('user_register')

        # CREATE USER
        user = Login.objects.create_user(
            username=username,
            password=password,
            usertype='user'
        )
        user.viewpassword = password
        user.save()

        # PROFILE
        UserProfile.objects.create(
            login=user,
            full_name=full_name,
            email=email,
            phone=phone,
            profile_pic=profile_pic
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'user_register.html')



def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def user_dashboard(request):
    return render(request, 'user/user_dashboard.html')

def insurance_dashboard(request):
    return render(request, 'insurance/insurance_dashboard.html')


def view_users(request):
    users = UserProfile.objects.select_related('login').all()
    return render(request, 'admin/view_users.html', {'users': users})


def delete_user(request, user_id):
    user = get_object_or_404(Login, id=user_id)
    user.delete()          # UserProfile is deleted automatically because of CASCADE
    messages.success(request, "User deleted successfully.")
    return redirect('view_users')


def toggle_user_status(request, user_id):
    user = get_object_or_404(Login, id=user_id)

    user.is_active = not user.is_active
    user.save()

    if user.is_active:
        messages.success(request, "User activated successfully.")
    else:
        messages.success(request, "User deactivated successfully.")

    return redirect('view_users')




def insurance_register(request):
    if request.method == "POST":

        company_name = request.POST['company_name']
        assessor_name = request.POST['assessor_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        license_number = request.POST['license_number']
        profile_pic = request.FILES.get('profile_pic')

        # validations

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('insurance_register')

        if InsuranceProfile.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('insurance_register')

        if InsuranceProfile.objects.filter(license_number=license_number).exists():
            messages.error(request, "License Number already exists.")
            return redirect('insurance_register')

        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, "Enter a valid 10-digit phone number.")
            return redirect('insurance_register')

        # Generate Password

        password = ''.join(
            random.choices(
                string.ascii_letters +
                string.digits +
                "@#$%",
                k=10
            )
        )

        # Create Login

        user = Login.objects.create_user(
            username=username,
            password=password,
            usertype='insurance'
        )

        user.viewpassword = password
        user.save()

        # Create Insurance Profile

        InsuranceProfile.objects.create(
            login=user,
            company_name=company_name,
            assessor_name=assessor_name,
            email=email,
            phone=phone,
            license_number=license_number,
            profile_pic=profile_pic
        )

        # Send Mail

        subject = "Vehicle Damage Detection System - Registration"

        message = f"""
Dear {assessor_name},

Your Insurance Assessor account has been created successfully.

Username : {username}

Password : {password}

Please login using the above credentials.

Thank You.
"""

        send_mail(
            subject,
            message,
            None,
            [email],
            fail_silently=False
        )

        messages.success(request, "Registration Successful. Password has been sent to your email.")

        return redirect('admin_dashboard')

    return render(request, 'admin/insurance_register.html')




def view_insurance(request):
    insurance = InsuranceProfile.objects.all()
    return render(request, "admin/view_insurance.html", {"insurance": insurance})


def toggle_insurance_status(request, id):
    user = get_object_or_404(Login, id=id)
    user.is_active = not user.is_active
    user.save()

    messages.success(request, "Insurance account status updated successfully.")
    return redirect("view_insurance")


def delete_insurance(request, id):
    user = get_object_or_404(Login, id=id)
    user.delete()

    messages.success(request, "Insurance assessor deleted successfully.")
    return redirect("view_insurance")





def user_profile(request):

    if 'login_id' not in request.session:
        messages.error(request, "Please login first.")
        return redirect('login_view')

    try:
        profile = UserProfile.objects.get(login_id=request.session['login_id'])
    except UserProfile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('user_dashboard')

    return render(request, 'user/user_profile.html', {
        'profile': profile
    })





def insurance_profile(request):

    if 'login_id' not in request.session:
        messages.error(request, "Please login first.")
        return redirect('login_view')

    try:
        profile = InsuranceProfile.objects.get(
            login_id=request.session['login_id']
        )
    except InsuranceProfile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('insurance_dashboard')

    return render(
        request,
        'insurance/insurance_profile.html',
        {
            'profile': profile
        }
    )




def view_insurance_companies(request):

    companies = InsuranceProfile.objects.select_related('login').all()

    return render(
        request,
        'user/view_insurance_companies.html',
        {
            'companies': companies
        }
    )


from .models import *

def create_claim(request, insurance_id):

    insurance = InsuranceProfile.objects.get(id=insurance_id)

    user = UserProfile.objects.get(
        login=request.user
    )

    if request.method == "POST":

        image = request.FILES['image']

        Claim.objects.create(
            user=user,
            insurance=insurance,
            image=image
        )

        messages.success(request, "Claim Submitted Successfully")

        return redirect('my_claims')

    return render(
        request,
        'user/create_claim.html',
        {
            'insurance': insurance
        }
    )



def my_claims(request):

    user = UserProfile.objects.get(
        login=request.user
    )

    claims = Claim.objects.filter(
        user=user
    ).order_by('-id')

    return render(
        request,
        'user/my_claims.html',
        {
            'claims': claims
        }
    )



def insurance_claims(request):

    insurance = InsuranceProfile.objects.get(
        login=request.user
    )

    claims = Claim.objects.filter(
        insurance=insurance
    ).order_by('-id')

    return render(
        request,
        'insurance/insurance_claims.html',
        {
            'claims': claims
        }
    )



from ai_model.predict import predict_image
import os

def run_ai_detection(request, claim_id):

    claim = get_object_or_404(
        Claim,
        id=claim_id
    )

    image_path = claim.image.path

    prediction, confidence = predict_image(image_path)

    claim.prediction = prediction
    claim.confidence = round(confidence * 100, 2)

    claim.save()

    messages.success(
        request,
        "AI Detection Completed Successfully."
    )

    return redirect('insurance_claims')





def approve_claim(request, claim_id):

    claim = get_object_or_404(Claim, id=claim_id)

    claim.status = "Approved"
    claim.save()

    messages.success(request, "Claim Approved Successfully.")

    return redirect("insurance_claims")


def reject_claim(request, claim_id):

    claim = get_object_or_404(Claim, id=claim_id)

    claim.status = "Rejected"
    claim.save()

    messages.success(request, "Claim Rejected Successfully.")

    return redirect("insurance_claims")



def admin_claims(request):

    if not request.user.is_superuser:
        return redirect("login_view")

    claims = Claim.objects.select_related(
        'user',
        'insurance'
    ).order_by('-created_at')

    return render(
        request,
        'admin/admin_claims.html',
        {
            'claims': claims
        }
    )






from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models.functions import TruncMonth
from calendar import month_abbr

@login_required
def admin_stat(request):

    if not request.user.is_superuser:
        return redirect("login_view")

    # ===========================
    # Cards
    # ===========================

    total_claims = Claim.objects.count()

    approved = Claim.objects.filter(status="Approved").count()

    rejected = Claim.objects.filter(status="Rejected").count()

    pending = Claim.objects.filter(status="Pending").count()

    damage = Claim.objects.filter(prediction="Damage").count()

    whole = Claim.objects.filter(prediction="Whole").count()

    # ===========================
    # Claims Per Month
    # ===========================

    monthly_claims = (
        Claim.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    month_labels = []
    month_values = []

    for item in monthly_claims:
        month_labels.append(item["month"].strftime("%b %Y"))
        month_values.append(item["total"])

    # ===========================
    # Claims Per Insurance Company
    # ===========================

    company_claims = (
        Claim.objects
        .values("insurance__company_name")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    company_labels = []
    company_values = []

    for item in company_claims:
        company_labels.append(item["insurance__company_name"])
        company_values.append(item["total"])

    # ===========================
    # Confidence Distribution
    # ===========================

    confidence_ranges = {
        "0-20":0,
        "21-40":0,
        "41-60":0,
        "61-80":0,
        "81-100":0,
    }

    for c in Claim.objects.exclude(confidence=None):

        value = c.confidence

        if value <=20:
            confidence_ranges["0-20"] +=1

        elif value<=40:
            confidence_ranges["21-40"] +=1

        elif value<=60:
            confidence_ranges["41-60"] +=1

        elif value<=80:
            confidence_ranges["61-80"] +=1

        else:
            confidence_ranges["81-100"] +=1

    context = {

        "total_claims": total_claims,

        "approved": approved,

        "rejected": rejected,

        "pending": pending,

        "damage": damage,

        "whole": whole,

        "month_labels": month_labels,
        "month_values": month_values,

        "company_labels": company_labels,
        "company_values": company_values,

        "confidence_labels": list(confidence_ranges.keys()),
        "confidence_values": list(confidence_ranges.values()),

    }

    return render(request,"admin/admin_stat.html",context)