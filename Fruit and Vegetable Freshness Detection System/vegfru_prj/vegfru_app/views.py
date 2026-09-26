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


def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def store_manager_dashboard(request):
    return render(request, 'store_manager/store_manager_dashboard.html')

def quality_inspector_dashboard(request):
    return render(request, 'quality_inspector/quality_inspector_dashboard.html')

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
            elif user.usertype == 'store_manager':
                messages.success(request, "Store Manager Login Successfully")
                return redirect('store_manager_dashboard')
            
            elif user.usertype == 'quality_inspector':
                messages.success(request, "Quality Inspector Login Successfully")
                return redirect('quality_inspector_dashboard')

            else:
                messages.error(request, "Invalid user type")
                return redirect('login_view')

        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('login')

    return render(request, 'login.html')





def password_generator():

    letters = string.ascii_letters
    numbers = string.digits

    password = ''.join(random.choice(letters + numbers) for i in range(8))

    return password


def add_quality_inspector(request):

    if request.method == "POST":

        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        address = request.POST["address"]
        profile = request.FILES["profile"]

        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("add_quality_inspector")

        if Quality_Inspector.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists.")
            return redirect("add_quality_inspector")

        password = password_generator()

        login = Login.objects.create(
            first_name=name,
            username=email,
            email=email,
            password=make_password(password),
            viewpassword=password,
            usertype="quality_inspector",
            is_active=True,
        )

        Quality_Inspector.objects.create(
            login=login,
            name=name,
            phone=phone,
            email=email,
            address=address,
            profile=profile,
        )

        subject = "Quality Inspector Login Credentials"

        message = f"""
Dear {name},

Your Quality Inspector account has been created successfully.

Login Details

Username : {email}
Password : {password}

Please login and change your password after your first login.

Thank You.
"""

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            messages.success(request, "Quality Inspector added successfully. Login credentials sent to email.")

        except Exception:
            messages.warning(
                request,
                "Quality Inspector added successfully, but email could not be sent."
            )

        return redirect("add_quality_inspector")

    data = Quality_Inspector.objects.all()

    return render(
        request,
        "admin/add_quality_inspector.html",
        {"data": data},
    )




def delete_quality_inspector(request, id):

    obj = Quality_Inspector.objects.get(id=id)

    obj.login.delete()

    messages.success(request, "Deleted Successfully")

    return redirect("add_quality_inspector")


def toggle_quality_inspector(request, id):

    obj = Quality_Inspector.objects.get(id=id)

    if obj.login.is_active:

        obj.login.is_active = False

    else:

        obj.login.is_active = True

    obj.login.save()

    return redirect("add_quality_inspector")






def add_store_manager(request):

    if request.method == "POST":

        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        address = request.POST["address"]
        store_name = request.POST["store_name"]
        profile = request.FILES["profile"]

        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("add_store_manager")

        if Store_Manager.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists.")
            return redirect("add_store_manager")

        password = password_generator()

        login = Login.objects.create(
            first_name=name,
            username=email,
            email=email,
            password=make_password(password),
            viewpassword=password,
            usertype="store_manager",
            is_active=True,
        )

        Store_Manager.objects.create(
            login=login,
            name=name,
            phone=phone,
            email=email,
            address=address,
            store_name=store_name,
            profile=profile,
        )

        subject = "Store Manager Login Credentials"

        message = f"""
Dear {name},

Your Store Manager account has been created successfully.

Login Details

Username : {email}
Password : {password}

Please login and change your password after your first login.

Thank You.
"""

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            messages.success(request, "Store Manager added successfully. Login credentials sent to email.")

        except Exception:
            messages.warning(
                request,
                "Store Manager added successfully, but email could not be sent."
            )

        return redirect("add_store_manager")

    data = Store_Manager.objects.all()

    return render(
        request,
        "admin/add_store_manager.html",
        {"data": data},
    )

def delete_store_manager(request, id):

    obj = Store_Manager.objects.get(id=id)

    obj.login.delete()

    messages.success(request, "Deleted Successfully")

    return redirect("add_store_manager")


def toggle_store_manager(request, id):

    obj = Store_Manager.objects.get(id=id)

    if obj.login.is_active:
        obj.login.is_active = False
    else:
        obj.login.is_active = True

    obj.login.save()

    return redirect("add_store_manager")





def store_manager_profile(request):

    profile = Store_Manager.objects.get(login=request.user)

    return render(
        request,
        "store_manager/store_manager_profile.html",
        {"profile": profile},
    )


def quality_inspector_profile(request):

    profile = Quality_Inspector.objects.get(login=request.user)

    return render(
        request,
        "quality_inspector/quality_inspector_profile.html",
        {"profile": profile},
    )


from ml.predict import predict_image
def upload_image(request):

    inspector = Quality_Inspector.objects.get(login=request.user)

    if request.method=="POST":

        img=request.FILES["image"]

        obj=PredictionHistory.objects.create(

            inspector=inspector,

            image=img,

            predicted_class="Fresh Apple",

            freshness="Fresh",

            confidence=0

        )

        image_path=obj.image.path

        predicted_class,confidence=predict_image(image_path)

        if "fresh" in predicted_class.lower():

            freshness="Fresh"

        else:

            freshness="Rotten"

        predicted_class=predicted_class.replace("fresh","Fresh ")

        predicted_class=predicted_class.replace("rotten","Rotten ")

        predicted_class=predicted_class.title()

        obj.predicted_class=predicted_class

        obj.freshness=freshness

        obj.confidence=round(confidence,2)

        obj.save()

        return redirect("prediction_result",obj.id)

    return render(
        request,
        "quality_inspector/upload_image.html"
    )



def prediction_result(request,id):

    data=PredictionHistory.objects.get(id=id)

    return render(

        request,

        "quality_inspector/prediction_result.html",

        {"data":data}

    )


def prediction_history(request):

    login_id = request.session.get("login_id")

    inspector = Quality_Inspector.objects.get(
        login_id=login_id
    )

    history = PredictionHistory.objects.filter(
        inspector=inspector
    ).order_by("-uploaded_at")

    context = {
        "history": history
    }

    return render(
        request,
        "quality_inspector/prediction_history.html",
        context
    )

def inspection_report_list(request):

    reports = InspectionReport.objects.select_related(
        "prediction",
        "prediction__inspector",
        "verified_by"
    ).order_by("-created_at")

    context = {

        "reports": reports

    }

    return render(

        request,

        "store_manager/inspection_report_list.html",

        context

    )




def inspection_report_detail(request,id):

    report = get_object_or_404(

        InspectionReport,

        id=id

    )

    return render(

        request,

        "store_manager/inspection_report_detail.html",

        {

            "report":report

        }

    )




def verify_report(request,id):

    report = get_object_or_404(

        InspectionReport,

        id=id

    )

    manager = Store_Manager.objects.get(

        login=request.user

    )

    # Already verified

    if report.verified:

        messages.error(

            request,

            "This report has already been verified."

        )

        return redirect(

            "inspection_report_detail",

            report.id

        )

    report.verified=True

    report.verified_by=manager

    report.save()

    report.prediction.verified=True

    report.prediction.save()

    messages.success(

        request,

        "Inspection Report Verified Successfully."

    )

    return redirect(

        "inspection_report_detail",

        report.id

    )



def verify_prediction_history(request):

    data = PredictionHistory.objects.select_related(
        "inspector"
    ).order_by("-uploaded_at")

    return render(
        request,
        "store_manager/verify_prediction_history.html",
        {"data": data}
    )


def verify_prediction(request, id):

    prediction = get_object_or_404(
        PredictionHistory,
        id=id
    )

    manager = Store_Manager.objects.get(
        login=request.user
    )

    if request.method == "POST":

        remarks = request.POST.get("remarks")

        recommendation = request.POST.get("recommendation")

        prediction.verified = True

        prediction.verified_by = manager

        prediction.verified_date = timezone.now()

        prediction.save()

        report_no = "RPT" + timezone.now().strftime("%Y%m%d%H%M%S")

        InspectionReport.objects.create(
            prediction=prediction,
            report_number=report_no,
            remarks=remarks,
            recommendation=recommendation
        )

        messages.success(
            request,
            "Prediction Verified Successfully."
        )

        return redirect("verify_prediction_history")

    return render(
        request,
        "store_manager/verify_prediction.html",
        {
            "prediction": prediction
        }
    )






def admin_view_reports(request):

    reports = InspectionReport.objects.select_related(
        'prediction',
        'prediction__inspector',
        'prediction__verified_by'
    ).order_by('-created_at')

    total_reports = reports.count()

    total_predictions = PredictionHistory.objects.count()

    fresh_count = PredictionHistory.objects.filter(
        freshness="Fresh"
    ).count()

    rotten_count = PredictionHistory.objects.filter(
        freshness="Rotten"
    ).count()

    verified_count = PredictionHistory.objects.filter(
        verified=True
    ).count()

    unverified_count = PredictionHistory.objects.filter(
        verified=False
    ).count()

    average_confidence = PredictionHistory.objects.aggregate(
        Avg('confidence')
    )['confidence__avg'] or 0

    class_stats = PredictionHistory.objects.values(
        'predicted_class'
    ).annotate(
        total=Count('id')
    )

    context = {

        "reports": reports,

        "total_reports": total_reports,

        "total_predictions": total_predictions,

        "fresh_count": fresh_count,

        "rotten_count": rotten_count,

        "verified_count": verified_count,

        "unverified_count": unverified_count,

        "average_confidence": round(average_confidence,2),

        "class_stats": class_stats,

    }

    return render(
        request,
        "admin/admin_view_reports.html",
        context
    )