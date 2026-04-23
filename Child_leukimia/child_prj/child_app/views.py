from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password 
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate,login
from .models import *


def index(request):
    return render(request,'index.html')

from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .models import Login, User
import re

def customer_registration(request):
    if request.method == "POST":
        name = request.POST.get("txtName")
        address = request.POST.get("txtAddress")
        phone = request.POST.get("txtContact")
        email = request.POST.get("txtEmail")
        password = request.POST.get("txtPwd")

        # -------- PHONE VALIDATION ----------
        if not re.match(r'^[6-9][0-9]{9}$', phone):
            return render(request, "customer_registration.html", {"msg": "Invalid phone number"})

        if User.objects.filter(phone=phone).exists():
            return render(request, "customer_registration.html", {"msg": "Phone already exists"})

        # -------- EMAIL VALIDATION ----------
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|in)$', email):
            return render(request, "customer_registration.html", {"msg": "Invalid email format (.com or .in only)"})

        if Login.objects.filter(username=email).exists():
            return render(request, "customer_registration.html", {"msg": "Email already registered"})

        # -------- PASSWORD VALIDATION ----------
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            return render(request, "customer_registration.html", {"msg": "Weak password"})

        # -------- SAVE LOGIN ----------
        login_obj = Login.objects.create(
            username=email,
            email=email,
            usertype="customer",
            viewpassword=password,
            password=make_password(password)
        )

        # -------- SAVE USER ----------
        User.objects.create(
            login=login_obj,
            full_name=name,
            phone=phone,
            address=address
        )
        messages.success(request,'Customer Registered successfully')
        return render(request, "customer_registration.html", {"msg": "Registration Successful"})

    return render(request, "customer_registration.html")



from .models import Doctor

def doctor_registration(request):
    if request.method == "POST":
        name = request.POST.get("txtName")
        address = request.POST.get("txtAddress")
        phone = request.POST.get("txtContact")
        email = request.POST.get("txtEmail")
        experience = request.POST.get("txtExperience")
        qualification = request.POST.get("txtQualification")
        specialization = request.POST.get("txtSpecialization")
        password = request.POST.get("txtPwd")

        # PHONE VALIDATION
        if not re.match(r'^[6-9][0-9]{9}$', phone):
            return render(request, "doctor_registration.html", {"msg": "Invalid phone number"})

        if Doctor.objects.filter(phone=phone).exists():
            return render(request, "doctor_registration.html", {"msg": "Phone already exists"})

        # EMAIL VALIDATION
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|in)$', email):
            return render(request, "doctor_registration.html", {"msg": "Invalid email format (.com or .in only)"})

        if Login.objects.filter(username=email).exists():
            return render(request, "doctor_registration.html", {"msg": "Email already registered"})

        # PASSWORD VALIDATION
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            return render(request, "doctor_registration.html", {"msg": "Weak password"})

        # SAVE LOGIN
        login_obj = Login.objects.create(
            username=email,
            email=email,
            usertype="doctor",
            viewpassword=password,
            password=make_password(password),
            is_active=False
        )

        # SAVE DOCTOR
        Doctor.objects.create(
            login=login_obj,
            full_name=name,
            phone=phone,
            address=address,
            experience=experience,
            qualification=qualification,
            specialization=specialization
        )
        messages.success(request,'Doctor Registered successfully')
        return render(request, "doctor_registration.html", {"msg": "Doctor Registration Successful"})

    return render(request, "doctor_registration.html")

def adm(request):
    adm=Login.objects.create_superuser(username='admin',email='admin@gmail.com',viewpassword='admin',password='admin',usertype='admin')
    adm.save()
    return redirect('/')

from django.shortcuts import render, redirect
from .models import Login
from django.contrib.auth.hashers import check_password

from django.contrib.auth import authenticate
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['uid'] = user.id
            request.session['usertype'] = user.usertype

            if user.usertype == 'admin':
                messages.success(request, 'Admin Login Successful')
                return redirect('admin_dashboard')

            elif user.usertype == 'doctor':
                messages.success(request, 'Doctor Login Successful')
                return redirect('doctor_dashboard')

            elif user.usertype == 'customer':
                messages.success(request, 'Customer Login Successful')
                return redirect('customer_dashboard')

        else:
            return render(request, 'login.html', {'msg': 'Invalid Username or Password'})

    return render(request, 'login.html')

def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')


def customer_dashboard(request):
    return render(request,'customer/customer_dashboard.html')


def doctor_dashboard(request):
    return render(request,'doctor/doctor_dashboard.html')

def admin_view_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin/admin_view_doctors.html', {'doctors': doctors})


# Admin View Customers
def admin_view_customers(request):
    customers = User.objects.all()
    return render(request, 'admin/admin_view_customers.html', {'customers': customers})


# Approve Doctor
def approve_doctor(request, id):
    login_obj = Login.objects.get(id=id)
    login_obj.is_active = True
    login_obj.save()
    return redirect('admin_view_doctors')


# Reject Doctor
def reject_doctor(request, id):
    login_obj = Login.objects.get(id=id)
    login_obj.delete()      # Doctor table auto deletes (CASCADE)
    return redirect('admin_view_doctors')


# Reject Customer
def reject_customer(request, id):
    login_obj = Login.objects.get(id=id)
    login_obj.delete()
    return redirect('admin_view_customers')



# Doctor Profile
def doctor_profile(request):
    if request.session.get('usertype') != 'doctor':
        return redirect('login_view')

    login_id = request.session.get('uid')
    doctor = Doctor.objects.get(login_id=login_id)

    return render(request, 'doctor/doctor_profile.html', {'doctor': doctor})


# User Profile
def customer_profile(request):
    if request.session.get('usertype') != 'customer':
        return redirect('login_view')

    login_id = request.session.get('uid')
    user = User.objects.get(login_id=login_id)

    return render(request, 'customer/customer_profile.html', {'user': user})


from .models import Appointment
from datetime import datetime

def book_appointment(request):
    if request.session.get('usertype') != 'customer':
        return redirect('login_view')

    doctors = Doctor.objects.all()

    if request.method == "POST":
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')

        login_id = request.session.get('uid')
        user = User.objects.get(login_id=login_id)
        doctor = Doctor.objects.get(id=doctor_id)

        # 1️⃣ Check max 10 per day
        count = Appointment.objects.filter(doctor=doctor, date=date).count()

        if count >= 10:
            return render(request, 'customer/book_appointment.html',
                          {'doctors': doctors, 'msg': 'Doctor fully booked for this date'})

        # 2️⃣ Check same date + time
        exists = Appointment.objects.filter(doctor=doctor, date=date, time=time).exists()

        if exists:
            return render(request, 'customer/book_appointment.html',
                          {'doctors': doctors, 'msg': 'This time slot already booked'})

        Appointment.objects.create(
            doctor=doctor,
            user=user,
            date=date,
            time=time
        )
        messages.success(request,'Booked successfully')
        return render(request, 'customer/book_appointment.html',
                      {'doctors': doctors, 'msg': 'Appointment Booked Successfully'})

    return render(request, 'customer/book_appointment.html', {'doctors': doctors})



def doctor_view_appointments(request):
    if request.session.get('usertype') != 'doctor':
        return redirect('login_view')

    login_id = request.session.get('uid')
    doctor = Doctor.objects.get(login_id=login_id)

    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, 'doctor/doctor_view_appointments.html',
                  {'appointments': appointments})


def approve_appointment(request, id):
    appointment = Appointment.objects.get(id=id)

    if request.method == "POST":
        fee = request.POST.get('fee')

        appointment.consultation_fee = fee
        appointment.status = 'Approved'
        appointment.payment_status = 'Pending'   # ✅ ADD THIS
        appointment.save()
        messages.success(request,'Approved successfully')

        return redirect('doctor_view_appointments')

    return render(request, 'doctor/approve_appointment.html', {'appointment': appointment})


def user_view_appointments(request):
    if request.session.get('usertype') != 'customer':
        return redirect('login_view')

    login_id = request.session.get('uid')
    user = User.objects.get(login_id=login_id)

    appointments = Appointment.objects.filter(user=user)

    return render(request, 'customer/user_view_appointments.html',
                  {'appointments': appointments})


def make_payment(request, id):
    appointment = Appointment.objects.get(id=id)

    # Only allow payment if doctor approved
    if appointment.status != 'Approved':
        return redirect('user_view_appointments')

    if request.method == "POST":
        card_number = request.POST.get('card_number')
        name = request.POST.get('name')
        cvv = request.POST.get('cvv')
        expiry = request.POST.get('expiry')

        # No real validation, simple simulation
        appointment.payment_status = 'Paid'
        appointment.save()
        messages.success(request,'Payment done successfully')

        return redirect('user_view_appointments')

    return render(request, 'customer/make_payment.html', {'appointment': appointment})

def cancel_appointment(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    messages.success(request,'Appointment cancelled successfully')   # Slot becomes available automatically
    return redirect('user_view_appointments')
from django.shortcuts import render
from .forms import ImageUploadForm
import numpy as np
import cv2
import time
from tensorflow.keras.models import load_model

model = load_model('leukemia_model.h5')

classes = ['Benign','Early','Pre','Pro']


def predict_image(img_path):

    img = cv2.imread(img_path)
    img = cv2.resize(img,(224,224))
    img = img/255.0
    img = np.reshape(img,(1,224,224,3))

    pred = model.predict(img)

    class_index = np.argmax(pred)
    prediction = classes[class_index]

    confidence = float(np.max(pred))*100

    if prediction == "Benign":
        diagnosis = "No Leukemia Detected"
        stage = "Normal Cell"
    elif prediction == "Early":
        diagnosis = "Leukemia Detected"
        stage = "Early Stage ALL"
    elif prediction == "Pre":
        diagnosis = "Leukemia Detected"
        stage = "Pre-B ALL"
    else:
        diagnosis = "Leukemia Detected"
        stage = "Pro-B ALL"

    return prediction, diagnosis, stage, round(confidence,2)


def upload_image(request):

    result = None
    diagnosis = None
    stage = None
    confidence = None

    if request.method == 'POST':

        form = ImageUploadForm(request.POST,request.FILES)

        if form.is_valid():

            obj = form.save()

            img_path = obj.image.path

        
            time.sleep(5)

            result, diagnosis, stage, confidence = predict_image(img_path)

            obj.result = result
            obj.save()

    else:
        form = ImageUploadForm()

    return render(request,'upload.html',{
        'form':form,
        'result':result,
        'diagnosis':diagnosis,
        'stage':stage,
        'confidence':confidence
    })