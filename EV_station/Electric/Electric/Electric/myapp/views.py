from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.base import ContentFile



# Create your views here.
def index(request):
    return render(request,'index.html')


def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


def login(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.usertype == 'admin':
                messages.success(request, 'Welcome to admin Page')
                return redirect('/adminHome')
            elif user.usertype == 'User':
                request.session['uid'] = user.id
                messages.success(request, 'Welcome to User page')
                return redirect('/userHome')
            elif user.usertype == 'Owner':
                request.session['uid'] = user.id
                messages.success(request, 'Welcome to Owner page')
                return redirect('/evOwnerHome')
            else:
                messages.success(request, 'Invalid')
        else:
            messages.success(request, 'Invalid')
    return render(request, 'login.html')

# admin
# def admin(request):
#     adm=Login.objects.create_user(username='admin',view_password='admin',password='admin',usertype="admin")
#     adm.save()
#     return redirect('/')


def userRegister(request):
    if request.POST:
        otp = random.randint(100000, 999999)

        fs = FileSystemStorage()
        image_file = request.FILES['image']
        image_name = fs.save(image_file.name, image_file)

        request.session['user_data'] = {
            'firstName': request.POST['firstName'],
            'lastName': request.POST['lastName'],
            'email': request.POST['email'],
            'phone': request.POST['phone'],
            'place': request.POST['place'],
            'image': image_name,   # ✅ store path only
            'otp': str(otp)
        }

        send_mail(
            'OTP Verification',
            f'Your OTP is {otp}',
            settings.EMAIL_HOST_USER,
            [request.POST['email']]
        )

        request.session['otp'] = str(otp)
        messages.success(request, 'OTP sent to your email')
        return redirect('/verify_otp')

    return render(request, 'register.html')


def verify_otp(request):
    if request.POST:
        if request.POST['otp'] == request.session['otp']:
            data = request.session['user_data']
            password = generate_password()

            log = Login.objects.create_user(
                username=data['email'],
                password=password,
                view_password=password,
                usertype='User',
                is_active=1
            )

            User.objects.create(
                loginId=log,
                firstName=data['firstName'],
                lastName=data['lastName'],
                email=data['email'],
                phone=data['phone'],
                place=data['place'],
                image=data['image']  # ✅ path saved
            )

            send_mail(
                'Login Credentials',
                f'Your password is: {password}',
                settings.EMAIL_HOST_USER,
                [data['email']]
            )

            del request.session['user_data']
            del request.session['otp']

            messages.success(request, 'Registration successful. Password sent to email.')
            return redirect('/login')

        else:
            messages.error(request, 'Invalid OTP')

    return render(request, 'otp.html')




def deleteUser(request):
    id = request.GET.get('id')
    user = User.objects.filter(id=id).first()

    if user:
        login_id = user.loginId.id if user.loginId else None
        user.delete()

        if login_id:
            Login.objects.filter(id=login_id).delete()

        messages.success(request, "User has been deleted")
    else:
        messages.error(request, "User not found")

    return redirect('/users')  


from django.shortcuts import render, redirect
from .models import Station

def delete_station(request, id):
    station = Station.objects.get(id=id)
    station.delete()
    return redirect('viewStation')

def ownerRegister(request):
    if request.POST:
        password = generate_password()

        log = Login.objects.create_user(
            username=request.POST['email'],
            password=password,
            view_password=password,
            usertype='Owner',
            is_active=0
        )

        Owner.objects.create(
            loginId=log,
            firstName=request.POST['firstName'],
            lastName=request.POST['lastName'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            place=request.POST['place'],
            image=request.FILES['image']
        )

        send_mail(
            'Owner Account Created',
            f'Your login password is: {password}',
            settings.EMAIL_HOST_USER,
            [request.POST['email']]
        )

        messages.success(request, 'Registration successful. Password sent to email.')
        return redirect('/login')

    return render(request, 'register.html')


#admin####

def adminHome(request):
    return render(request,'Admin/adminHome.html')

def owners(request):
    data=Owner.objects.all()
    return render(request,'Admin/owners.html',{'data':data})


def ApproveOwner(request):
    id = request.GET.get('id')
    print(id,'kk')
    Owner.objects.filter(loginId__id=id).update(status="APPROVED")
    Login.objects.filter(id=id).update(is_active=1)
    messages.success(request, "Owner has been approved")
    return redirect('/owners')

def deleteOwner(request):
    id = request.GET.get('id')
    owner = Owner.objects.filter(id=id).first()
    
    if owner:
        login_id = owner.loginId.id if owner.loginId else None
        owner.delete()
        
        if login_id:
            Login.objects.filter(id=login_id).delete()
        
        messages.success(request, "Owner has been deleted")
    else:
        messages.error(request, "Owner not found")
    
    return redirect('/owners')

def users(request):
    data=User.objects.all()
    return render(request,'Admin/users.html',{'data':data})

def deleteStation(request):
    id = request.GET.get('id')
    station = Station.objects.filter(id=id).first()

    if station:
        station.delete()
        messages.success(request, "Station has been deleted")
    else:
        messages.error(request, "Station not found")

    return redirect('/stations')



def viewfeedback(request):
    data=Feedback.objects.all()
    return render(request,'Admin/viewfeedback.html',{'data':data})

##USER##

def userHome(request):
    return render(request,'User/userHome.html')

def userviewStation(request):
    data=Station.objects.all()
    return render(request,'User/userviewStation.html',{'data':data})


from datetime import datetime, time

def bookStation(request):
    if request.method == "POST":
        user_id = request.session['uid']
        user = User.objects.get(loginId=user_id)

        station_id = request.POST['station_id']
        station = Station.objects.get(id=station_id)

        date = request.POST['date']

        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        start_time_obj = datetime.strptime(start_time, "%H:%M").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M").time()

        
        conflicting_bookings = Booking.objects.filter(
            station=station,
            date=date,
            start_time__lt=end_time_obj,
            end_time__gt=start_time_obj
        )

        if conflicting_bookings.exists():
            messages.error(request, "This station is already booked for the selected time slot.")
            return redirect('userviewStation')

        booking = Booking.objects.create(
            user=user,
            station=station,
            date=date,
            start_time=start_time_obj,
            end_time=end_time_obj
        )
        booking.save()
        messages.success(request, "Booking successful!")
        return redirect('/userHome')

    stations = Station.objects.all()
    return render(request, 'User/bookStation.html', {'stations': stations})



# def view(request):
#     data=Station.objects.all()
#     return render(request,'User/view.html',{'data':data})
def view(request):
    location = request.GET.get('location', '')
    charging_type = request.GET.get('charging_type', '')

    stations = Station.objects.filter(
        location__icontains=location,
        status="Approved"
    )

    if charging_type:
        stations = stations.filter(charging_types__icontains=charging_type)

    return render(request, 'User/view.html', {'stations': stations})


 
def bookview(request):
    if 'uid' in request.session:
        user_id = request.session['uid']
        data = Booking.objects.filter(user__loginId__id=user_id).prefetch_related('payment_set')
    else:
        data = Booking.objects.none()  # Empty queryset for non-authenticated users

    return render(request, 'User/bookview.html', {'data': data})

def cancel_booking(request, id):
    if 'uid' in request.session:
        Booking.objects.filter(id=id, user__loginId__id=request.session['uid']).update(status='Cancelled')
    return redirect('/bookview')


def paidview(request):
    data = Payment.objects.select_related('booking__user', 'booking__station').all()
    return render(request, 'User/paidview.html', {'data': data})


def make_payment(request, booking_id):
    if request.method == "POST":
        user = User.objects.get(loginId=request.session['uid'])
        booking = Booking.objects.get(id=booking_id)
        payment = Payment.objects.create(booking=booking, status="PAID")
        payment.save()
        messages.success(request, "Payment Successful!")
        return redirect('/userHome')
    
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'User/make_payment.html', {'booking': booking})


def give_feedback(request, station_id):
    if request.method == "POST":
        login_id = request.session.get('uid')  
        if not login_id:
            messages.error(request, "User not logged in.")
            return redirect('/login') 

        try:
            login_user = Login.objects.get(id=login_id) 
            user = User.objects.get(loginId=login_user)  
            station = Station.objects.get(id=station_id)
            feedback_text = request.POST.get('feedback')

            Feedback.objects.create(user=user, station=station, feedback=feedback_text)

            messages.success(request, "Thank you for your feedback!")
            return redirect('/userHome')

        except Login.DoesNotExist:
            messages.error(request, "Login account not found.")
        except User.DoesNotExist:
            messages.error(request, "User profile not found.")
        except Station.DoesNotExist:
            messages.error(request, "Station not found.")

    station = Station.objects.get(id=station_id)
    return render(request, 'User/give_feedback.html', {'station': station})


#OWNER##

def evOwnerHome(request):
    return render(request,'EV_Owner/evOwnerHome.html')

def addStation(request):
    uid = request.session['uid']
    owner = Owner.objects.get(loginId=uid)

    if request.method == "POST":
        station = Station.objects.create(
            station_name=request.POST['station_name'],
            location=request.POST['location'],
            contact_number=request.POST['contact_number'],
            licence_number=request.POST['licence_number'],
            operating_hours=request.POST['operating_hours'],
            charging_types=','.join(request.POST.getlist('charging_types')),
            price=request.POST['price'],
            waiting_area=request.POST['waiting_area'],
            image=request.FILES['image'],
            owner=owner
        )

        messages.success(request, "Station Added Successfully")
        return redirect('/evOwnerHome')

    return render(request, 'EV_Owner/addStation.html')



def viewStation(request):
    owner = Owner.objects.get(loginId=request.session['uid'])  
    data = Station.objects.filter(owner=owner)  
    return render(request, 'EV_Owner/viewStation.html', {'data': data})


from django.shortcuts import get_object_or_404

def stationUpdate(request):
    id = request.GET.get('id')
    station = get_object_or_404(Station, id=id)

    if request.method == 'POST':
        station.station_name = request.POST['station_name']
        station.location = request.POST['location']
        station.contact_number = request.POST['contact_number']
        station.licence_number = request.POST['licence_number']
        station.operating_hours = request.POST['operating_hours']
        station.charging_types = ','.join(request.POST.getlist('charging_types'))
        station.price = request.POST['price']
        station.waiting_area = request.POST['waiting_area']

        if 'image' in request.FILES:
            station.image = request.FILES['image']

        station.save()
        messages.success(request, 'Station updated successfully')
        return redirect('viewStation')

    return render(request, 'EV_Owner/stationUpdate.html', {'data': [station]})



def owner_viewfeedback(request):
    owner = Owner.objects.get(loginId=request.session['uid'])  
    stations = Station.objects.filter(owner=owner)  
    data = Feedback.objects.filter(station__in=stations) 
    return render(request, 'EV_Owner/owner_viewfeedback.html', {'data': data})

def owner_paidview(request):
    owner = Owner.objects.get(loginId=request.session['uid'])  
    stations = Station.objects.filter(owner=owner) 
    bookings = Booking.objects.filter(station__in=stations) 
    data = Payment.objects.filter(booking__in=bookings, status="PAID")  

    return render(request, 'EV_Owner/owner_paidview.html', {'data': data})




def upload_payment_receipt(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    if request.method == "POST" and request.FILES.get("receipt_image"):
        payment.receipt_image = request.FILES["receipt_image"]
        payment.save()
        return redirect("owner_paidview")  # Adjust to your correct URL

    return render(request, "EV_Owner/upload_receipt.html", {"payment": payment})


def dlt(request):
    data=Login.objects.filter(id="4").delete()
    return redirect('/')

def show_stations(request):
    location = request.GET.get('location', '')  
    if location:
        stations = Station.objects.filter(location__icontains=location)
    else:
        stations = Station.objects.all()

    return render(request, 'Admin/show_stations.html', {'stations': stations})

def approve_station(request, station_id):
    station = Station.objects.get(id=station_id)
    station.status = "Approved"
    station.save()
    return redirect('show_stations')

def reject_station(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    station.delete()
    return redirect('show_stations')


def admin_view_bookings(request):
    data = Booking.objects.all().order_by('-id')
    return render(request, 'Admin/bookings.html', {'data': data})


def delete_booking(request):
    id = request.GET.get('id')
    Booking.objects.filter(id=id).delete()
    messages.success(request, 'Booking deleted successfully')
    return redirect('/adminViewBookings')

def owner_view_bookings(request):
    uid = request.session.get('uid')

    owner = Owner.objects.get(loginId_id=uid)

    stations = Station.objects.filter(owner=owner)

    data = Booking.objects.filter(station__in=stations).order_by('-id')

    return render(request, 'EV_Owner/bookings.html', {'data': data})
from django.shortcuts import render
from django.db.models import Count, F, IntegerField
from django.db.models.functions import Cast
from .models import Booking, Payment

def admin_booking_report(request):

    # -------- Average Daily Bookings --------
    daily_bookings = (
        Booking.objects
        .values('date')
        .annotate(total=Count('id'))
        .order_by('date')
    )

    avg_daily = 0
    if daily_bookings:
        total = sum(d['total'] for d in daily_bookings)
        avg_daily = total / len(daily_bookings)

    # -------- Station-wise Booking & Revenue --------
    paid_station_data = (
        Payment.objects
        .filter(status="PAID")
        .values(
            'booking__station__station_name',
            'booking__station__owner__firstName',
            'booking__station__price'
        )
        .annotate(
            total_paid_bookings=Count('id'),
            station_price=Cast(
                F('booking__station__price'),
                IntegerField()
            )
        )
        .annotate(
            total_amount=F('total_paid_bookings') * F('station_price')
        )
        .order_by('booking__station__station_name')
    )

    return render(
        request,
        'Admin/booking_report.html',
        {
            'avg_daily': round(avg_daily, 2),
            'paid_station_data': paid_station_data
        }
    )

def user_profile(request):
    uid = request.session.get('uid')
    user = User.objects.get(loginId_id=uid)
    return render(request, 'User/user_profile.html', {'user': user})

def edit_user_profile(request):
    uid = request.session.get('uid')
    user = User.objects.get(loginId_id=uid)

    if request.POST:
        user.firstName = request.POST['firstName']
        user.lastName = request.POST['lastName']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.place = request.POST['place']

        if 'image' in request.FILES:
            user.image = request.FILES['image']

        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('user_profile ')

    return render(request, 'User/edit_user_profile.html', {'user': user})


def owner_profile(request):
    uid = request.session.get('uid')
    owner = Owner.objects.get(loginId_id=uid)
    return render(request, 'EV_Owner/owner_profile.html', {'owner': owner})

def edit_owner_profile(request):
    uid = request.session.get('uid')
    owner = Owner.objects.get(loginId_id=uid)

    if request.POST:
        owner.firstName = request.POST['firstName']
        owner.lastName = request.POST['lastName']
        owner.email = request.POST['email']
        owner.phone = request.POST['phone']
        owner.place = request.POST['place']

        if 'image' in request.FILES:
            owner.image = request.FILES['image']

        owner.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('owner_profile')

    return render(request, 'EV_Owner/edit_owner_profile.html', {'owner': owner})



# myapp/views.py
import pandas as pd
import numpy as np
from django.shortcuts import render
from sklearn.linear_model import LinearRegression
import os
from django.conf import settings

CSV_PATH = os.path.join(settings.BASE_DIR, 'myapp/data/EV_Charging_Station_Usage.csv')

def analytics_view(request):
    df = pd.read_csv(CSV_PATH)

    total_sessions = len(df)
    total_energy = round(df['Energy_Consumed_kWh'].sum(), 2)
    total_revenue = round(df['Cost_INR'].sum(), 2)

    city_usage = df.groupby('City')['Energy_Consumed_kWh'].sum().sort_values(ascending=False).head(5)
    vehicle_usage = df.groupby('Vehicle_Type')['Energy_Consumed_kWh'].sum()
    payment_methods = df['Payment_Method'].value_counts()
    peak_city = city_usage.idxmax()

    context = {
        'total_sessions': total_sessions,
        'total_energy': total_energy,
        'total_revenue': total_revenue,
        'city_usage': city_usage.to_dict(),
        'vehicle_usage': vehicle_usage.to_dict(),
        'payment_methods': payment_methods.to_dict(),
        'peak_city': peak_city
    }
    return render(request, 'Admin/analytics.html', context)


def predict_energy(request):
    prediction = None

    if request.POST:
        hours = float(request.POST['hours'])

        df = pd.read_csv(CSV_PATH)
        X = df[['Cost_INR']]
        y = df['Energy_Consumed_kWh']

        model = LinearRegression()
        model.fit(X, y)

        prediction = round(model.predict([[hours * 10]])[0], 2)

    return render(request, 'Admin/predict_energy.html', {'prediction': prediction})


def predict_cost(request):
    prediction = None

    if request.POST:
        energy = float(request.POST['energy'])

        df = pd.read_csv(CSV_PATH)
        X = df[['Energy_Consumed_kWh']]
        y = df['Cost_INR']

        model = LinearRegression()
        model.fit(X, y)

        prediction = round(model.predict([[energy]])[0], 2)

    return render(request, 'Admin/predict_cost.html', {'prediction': prediction})

import csv
import os
import time
from django.conf import settings
from django.shortcuts import render
from .models import User

def recommend_station(request):
    uid = request.session.get('uid')

    # simulate ML processing delay (1.5 seconds)
    time.sleep(1.5)

    user_city = User.objects.get(loginId_id=uid).place

    charging_type = request.GET.get('charging_type', '')  # AC / DC

    stations = []

    csv_path = os.path.join(settings.BASE_DIR, 'ev-charging-stations-india.csv')

    with open(csv_path, encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            city = row['city'].strip()
            name = row['name'].upper()

            if user_city.lower() == city.lower():

                if charging_type:
                    if charging_type.upper() not in name:
                        continue

                stations.append(row)

                
                time.sleep(0.8)

    return render(request, 'User/recommend_station.html', {
        'stations': stations,
        'selected_type': charging_type
    })
