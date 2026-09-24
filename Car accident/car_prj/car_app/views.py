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
            elif user.usertype == 'mvd':
                messages.success(request, "MVD Login Successfully")
                return redirect('mvd_dashboard')

            else:
                messages.error(request, "Invalid user type")
                return redirect('login_view')

        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('login_view')

    return render(request, 'login.html')


def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


def mvd_dashboard(request):
    return render(request, 'mvd/mvd_dashboard.html')


import random
import string
import os

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from .models import *


def add_mvd(request):

    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        job_post = request.POST['job_post']
        address = request.POST['address']
        dob = request.POST['dob']
        gender = request.POST['gender']
        experience = request.POST['experience']

        profile_pic = request.FILES.get('profile_pic')
        aadhar_image = request.FILES.get('aadhar_image')

        # -------------------------
        # EMPTY FIELD VALIDATIONS
        # -------------------------

        if name == "":
            messages.error(request, "Name is required")
            return redirect('add_mvd')

        if email == "":
            messages.error(request, "Email is required")
            return redirect('add_mvd')

        if phone == "":
            messages.error(request, "Phone number is required")
            return redirect('add_mvd')

        if address == "":
            messages.error(request, "Address is required")
            return redirect('add_mvd')

        # -------------------------
        # EMAIL VALIDATION
        # -------------------------

        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return redirect('add_mvd')

        # -------------------------
        # PHONE VALIDATION
        # -------------------------

        if not phone.isdigit():
            messages.error(request, "Phone number must contain digits only")
            return redirect('add_mvd')

        if len(phone) != 10:
            messages.error(request, "Phone number must be 10 digits")
            return redirect('add_mvd')

        # -------------------------
        # NAME VALIDATION
        # -------------------------

        if len(name) < 3:
            messages.error(request, "Name too short")
            return redirect('add_mvd')

        # -------------------------
        # AGE VALIDATION
        # -------------------------

        birth_year = int(dob.split("-")[0])

        current_year = 2026

        age = current_year - birth_year

        if age < 18:
            messages.error(request, "MVD officer must be above 18")
            return redirect('add_mvd')

        # -------------------------
        # PROFILE PIC VALIDATION
        # -------------------------

        if not profile_pic:
            messages.error(request, "Profile picture required")
            return redirect('add_mvd')

        allowed_extensions = ['.jpg', '.jpeg', '.png']

        profile_ext = os.path.splitext(
            profile_pic.name
        )[1].lower()

        if profile_ext not in allowed_extensions:
            messages.error(
                request,
                "Profile picture must be JPG or PNG"
            )
            return redirect('add_mvd')

        # -------------------------
        # AADHAR VALIDATION
        # -------------------------

        if not aadhar_image:
            messages.error(request, "Aadhar image required")
            return redirect('add_mvd')

        aadhar_ext = os.path.splitext(
            aadhar_image.name
        )[1].lower()

        if aadhar_ext not in allowed_extensions:
            messages.error(
                request,
                "Aadhar image must be JPG or PNG"
            )
            return redirect('add_mvd')

        # -------------------------
        # GENERATE PASSWORD
        # -------------------------

        password = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=8
            )
        )

        username = email

        # -------------------------
        # CREATE LOGIN
        # -------------------------

        login_obj = Login.objects.create_user(
            username=username,
            password=password
        )

        login_obj.usertype = 'mvd'
        login_obj.viewpassword = password
        login_obj.save()

        # -------------------------
        # CREATE MVD
        # -------------------------

        MVD.objects.create(
            login=login_obj,
            name=name,
            email=email,
            phone=phone,
            profile_pic=profile_pic,
            job_post=job_post,
            address=address,
            dob=dob,
            aadhar_image=aadhar_image,
            gender=gender,
            experience=experience
        )

        # -------------------------
        # SEND EMAIL
        # -------------------------

        subject = "MVD Login Credentials"

        message = f"""
Hello {name},

Your MVD account has been created successfully.

Username: {username}

Password: {password}

Please login and change password later.

Thank You
AI Accident Detection Team
"""

        send_mail(
            subject,
            message,
            'teamlccalwaye@gmail.com',
            [email],
            fail_silently=False
        )

        messages.success(
            request,
            "MVD Officer Added Successfully"
        )

        return redirect('add_mvd')

    return render(request, 'admin/add_mvd.html')




def view_mvd(request):

    if not request.session.get('login_id'):
        return redirect('login_view')

    mvd = MVD.objects.all()

    return render(
        request,
        'admin/view_mvd.html',
        {
            'mvd': mvd
        }
    )


def delete_mvd(request, id):

    if not request.session.get('login_id'):
        return redirect('login_view')

    mvd = get_object_or_404(MVD, id=id)

    login_obj = mvd.login

    # DELETE MVD TABLE DATA
    mvd.delete()

    # DELETE LOGIN TABLE DATA
    login_obj.delete()

    messages.success(request, "MVD Deleted Successfully")

    return redirect('view_mvd')



import os

def mvd_profile(request):

    if not request.session.get('login_id'):
        return redirect('login_view')

    login_id = request.session['login_id']

    mvd = get_object_or_404(MVD, login_id=login_id)

    return render(
        request,
        'mvd/mvd_profile.html',
        {'mvd': mvd}
    )


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import os

from .models import *


def edit_mvd_profile(request):

    if not request.session.get('login_id'):
        return redirect('login_view')

    login_id = request.session['login_id']

    mvd = get_object_or_404(MVD, login_id=login_id)

    if request.method == "POST":

        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        experience = request.POST['experience']
        gender = request.POST['gender']
        job_post = request.POST['job_post']
        
        dob = request.POST['dob']

        profile_pic = request.FILES.get('profile_pic')
        aadhar_image = request.FILES.get('aadhar_image')

        # ---------------- VALIDATIONS ----------------

        if len(name) < 3:
            messages.error(request, "Name too short")
            return redirect('edit_mvd_profile')

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Invalid phone number")
            return redirect('edit_mvd_profile')

        if address == "":
            messages.error(request, "Address required")
            return redirect('edit_mvd_profile')

        if job_post == "":
            messages.error(request, "Job post required")
            return redirect('edit_mvd_profile')

        if gender == "":
            messages.error(request, "Gender required")
            return redirect('edit_mvd_profile')

        # ---------------- FILE VALIDATION ----------------

        allowed = ['.jpg', '.jpeg', '.png']

        if profile_pic:
            ext = os.path.splitext(profile_pic.name)[1].lower()
            if ext not in allowed:
                messages.error(request, "Invalid profile image format")
                return redirect('edit_mvd_profile')
            mvd.profile_pic = profile_pic

        if aadhar_image:
            ext = os.path.splitext(aadhar_image.name)[1].lower()
            if ext not in allowed:
                messages.error(request, "Invalid aadhar image format")
                return redirect('edit_mvd_profile')
            mvd.aadhar_image = aadhar_image

        # ---------------- UPDATE ----------------

        mvd.name = name
        mvd.phone = phone
        mvd.address = address
        mvd.experience = experience
        mvd.gender = gender
        mvd.job_post = job_post
       
        mvd.dob = dob

        mvd.save()

        messages.success(request, "Profile Updated Successfully")

        return redirect('mvd_profile')

    return render(
        request,
        'mvd/edit_mvd_profile.html',
        {'mvd': mvd}
    )



from .models import *
from django.shortcuts import render,redirect
from accident_model.predict import predict_accident

def upload_image(request):

    if request.method == "POST":

        image = request.FILES['image']

        mvd = MVD.objects.get(
            login_id=request.session['login_id']
        )

        prediction = Prediction.objects.create(
            mvd=mvd,
            image=image
        )

        result,confidence = predict_accident(
            prediction.image.path
        )

        prediction.result = result
        prediction.confidence = confidence
        prediction.save()

        return redirect(
            'prediction_result',
            prediction.id
        )

    return render(
        request,
        'mvd/upload_image.html'
    )


def prediction_result(request,id):

    data = Prediction.objects.get(
        id=id
    )

    return render(
        request,
        'mvd/prediction_result.html',
        {'data':data}
    )



def prediction_history(request):

    mvd = MVD.objects.get(
        login_id=request.session['login_id']
    )

    history = Prediction.objects.filter(
        mvd=mvd
    ).order_by('-date')

    return render(
        request,
        'mvd/prediction_history.html',
        {'history': history}
    )


def admin_prediction_history(request):

    if not request.user.is_superuser:
        return redirect('login')

    history = Prediction.objects.select_related(
        'mvd'
    ).order_by('-date')

    return render(
        request,
        'admin/admin_prediction_history.html',
        {'history': history}
    )


from django.db.models import Count
from django.db.models.functions import ExtractMonth
from .models import Prediction, MVD


def admin_analytics(request):

    total_predictions = Prediction.objects.count()

    total_accidents = Prediction.objects.filter(
        result='Accident'
    ).count()

    total_non_accidents = Prediction.objects.filter(
        result='Non Accident'
    ).count()

    accident_percentage = 0
    non_accident_percentage = 0

    if total_predictions > 0:

        accident_percentage = round(
            (total_accidents / total_predictions) * 100, 2
        )

        non_accident_percentage = round(
            (total_non_accidents / total_predictions) * 100, 2
        )

    monthly_data = (
        Prediction.objects
        .annotate(month=ExtractMonth('date'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    months = []
    monthly_counts = []

    month_names = [
        "",
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    for item in monthly_data:

        months.append(
            month_names[item['month']]
        )

        monthly_counts.append(
            item['total']
        )

    mvd_data = (
        Prediction.objects
        .values('mvd__name')
        .annotate(total=Count('id'))
        .order_by('-total')[:10]
    )

    mvd_names = [
        i['mvd__name']
        for i in mvd_data
    ]

    mvd_counts = [
        i['total']
        for i in mvd_data
    ]

    context = {

        'total_predictions': total_predictions,
        'total_accidents': total_accidents,
        'total_non_accidents': total_non_accidents,

        'accident_percentage': accident_percentage,
        'non_accident_percentage': non_accident_percentage,

        'months': months,
        'monthly_counts': monthly_counts,

        'mvd_names': mvd_names,
        'mvd_counts': mvd_counts,

        'recent_predictions':
        Prediction.objects.order_by('-date')[:10]

    }

    return render(
        request,
        'admin/admin_analytics.html',
        context
    )
