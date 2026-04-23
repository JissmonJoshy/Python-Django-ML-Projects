from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate
from django.contrib import messages
from datetime import date as date, datetime as dt
from datetime import datetime
from django.db import transaction  
from django.utils.timezone import now 
from datetime import date as date, datetime as dt
from django.db.models import Q, Min, Max

# Create your views here.

def index(request):
    return render(request,'index.html')






#Login--
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email,password=password)
        if user is not None:
            if user.usertype == 'admin':
                messages.success(request, 'Welcome to Medical')
                return redirect('/adminHome')
            elif user.usertype == 'User':
                request.session['uid'] = user.id
                messages.success(request, 'Welcome to Medical')
                return redirect('/userHome')
            elif user.usertype == 'Doctor':
                request.session['uid'] = user.id
                messages.success(request, 'Welcome to Medical ')
                return redirect('/doctorHome')
            elif user.usertype == 'Pharmacist':
                request.session['uid'] = user.id
                messages.success(request, 'Welcome to Medical')
                return redirect('/pharmaHome')
            else:
                messages.info(request, "type Not Defined")

        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'login.html')




import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def doctor_register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        address = request.POST.get("address")
        medical_license_number = request.POST.get("medical_license_number")
        specialization = request.POST.get("specialization")
        image = request.FILES["image"]

        email_pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|[a-zA-Z0-9.-]+\.in)$'

        if not re.match(email_pattern, email):
            messages.error(request, "Email must be gmail.com or .in domain")

        elif not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be exactly 10 digits")

        elif Login.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")

        elif Doctor.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered")

        else:

            new_user = Login.objects.create_user(
                username=email,
                password=password,
                view_password=password,
                is_active=0,
                usertype="Doctor",
            )

            Doctor.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                image=image,
                medical_license_number=medical_license_number,
                specialization=specialization,
                loginId=new_user,
            )

            messages.success(request, "Doctor registration successful. Wait for admin approval.")
            return redirect("/login")

    return render(request, "doctor_reg.html")


import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def pharmacist_register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        address = request.POST.get("address")
        pharmacy_license_number = request.POST.get("pharmacy_license_number")
        pharmacy_name = request.POST.get("pharmacy_name")
        image = request.FILES["image"]

        email_pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|[a-zA-Z0-9.-]+\.in)$'

        if not re.match(email_pattern, email):
            messages.error(request, "Email must be gmail.com or .in domain")

        elif not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone number must be exactly 10 digits")

        elif Login.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")

        elif Pharmacist.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered")

        else:

            new_user = Login.objects.create_user(
                username=email,
                password=password,
                view_password=password,
                is_active=0,
                usertype="Pharmacist",
            )

            Pharmacist.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                image=image,
                loginId=new_user,
                pharmacy_license_number=pharmacy_license_number,
                pharmacy_name=pharmacy_name,
            )

            messages.success(request, "Registration successful. Wait for admin approval.")
            return redirect("/login")

    return render(request, "pharmacist_reg.html")



from django.shortcuts import render
from django.contrib import messages
from .models import *
import re

def user_register(request):

    if request.method == "POST":

        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        age = request.POST["age"]
        gender = request.POST["gender"]
        blood_group = request.POST["blood_group"]
        image = request.FILES["image"]

        email_pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|[a-zA-Z0-9.-]+\.in)$'

        if not re.match(email_pattern, email):
            messages.error(request,"Email must be gmail.com or .in domain")

        elif not phone.isdigit() or len(phone) != 10:
            messages.error(request,"Phone number must be 10 digits")

        elif Login.objects.filter(username=email).exists():
            messages.error(request,"Email already exists")

        elif User.objects.filter(phone=phone).exists():
            messages.error(request,"Phone number already registered")

        else:

            logUser = Login.objects.create_user(
                username=email,
                password=password,
                usertype="User",
                view_password=password,
                is_active=True
            )

            User.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                loginId=logUser,
                age=age,
                gender=gender,
                blood_group=blood_group,
                image=image,
            )

            messages.success(request,"Registration Successful")

    return render(request,"register.html")



# def dlt(request):
#     data=MedicineOrder.objects.filter(id="17").delete()
#     return redirect('/')


#----------ADMIN-----------#
# def admin(request):
#     adm=Login.objects.create_user(username='admin@gmail.com',view_password='admin',password='admin',usertype="admin")
#     adm.save()
#     return redirect('/')


def adminHome(request):
    return render(request,'Admin/index.html')

def admin_view_doctors(request):
    data=Doctor.objects.all()
    return render(request,'Admin/admin_view_doctors.html',{'data':data})

def approve_doctor(request):
    did=request.GET.get('did')
    did=Login.objects.filter(id=did).update(is_active=1)
    return redirect("/admin_view_doctors")

def reject_doctor(request):
    did=request.GET.get('did')
    Doctor.objects.filter(loginId_id=did).delete()
    did=Login.objects.filter(id=did).delete()
    return redirect("/admin_view_doctors")

def admin_view_phar(request):
    data=Pharmacist.objects.all()
    return render(request,'Admin/admin_view_phar.html',{'data':data})


def accept_pharma(request):
    did=request.GET.get('did')
    did=Login.objects.filter(id=did).update(is_active=1)
    return redirect("/admin_view_phar")

def reject_pharma(request):
    did=request.GET.get('did')
    Pharmacist.objects.filter(loginId_id=did).delete()
    did=Login.objects.filter(id=did).delete()
    return redirect("/admin_view_phar")
def adm_viewMedicine(request):
    data=Medicine.objects.all()
    return render(request,'Admin/adm_viewMedicine.html',{'data':data})

def adm_viewdetails(request):
    id=request.GET['id']
    data=Medicine.objects.filter(id=id)
    return render(request,'Admin/ad_viewdetails.html',{'data':data})

def SoldMedicine(request):
    data=MedicineOrder.objects.filter(status="Paid")
    return render(request,'Admin/soldMedicine.html',{'data':data})


def profit_report(request):
    orders = MedicineOrder.objects.filter(status="Paid")
    return render(request, "Admin/profit_reportt.html", {"orders": orders})

#------Pharmacist-----------#


def pharmaHome(request):
    return render(request, "Pharmacist/index.html")


def pharmacist_Profile(request):
    uid=request.session['uid']
    data=Pharmacist.objects.filter(loginId=uid)
    return render(request,'Pharmacist/pharmacist_Profile.html',{'data':data})

import re

def update_pharmacist_Profile(request):
    uid = request.session.get('uid')
    data = Pharmacist.objects.filter(loginId=uid)

    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        pharmacy_license_number = request.POST.get("pharmacy_license_number")
        pharmacy_name = request.POST.get("pharmacy_name")
        image = request.FILES.get("image")

        # ✅ NAME VALIDATION
        if not re.match(r"^[A-Za-z ]{3,50}$", name):
            messages.error(request, "Name must contain only letters (3–50 chars)")
            return redirect('/pharmacist_Profile')

        # ✅ PHONE VALIDATION
        if not phone.isdigit():
            messages.error(request, "Phone must contain only digits")
            return redirect('/pharmacist_Profile')

        if len(phone) != 10:
            messages.error(request, "Phone must be exactly 10 digits")
            return redirect('/pharmacist_Profile')

        # ✅ ADDRESS
        if len(address) < 5 or len(address) > 100:
            messages.error(request, "Address must be 5–100 characters")
            return redirect('/pharmacist_Profile')

        # ✅ LICENSE VALIDATION
        if not re.match(r"^[A-Za-z0-9\-]{5,20}$", pharmacy_license_number):
            messages.error(request, "Invalid license number")
            return redirect('/pharmacist_Profile')

        obj = Pharmacist.objects.get(loginId=uid)

        obj.name = name
        obj.phone = phone
        obj.address = address
        obj.pharmacy_license_number = pharmacy_license_number
        obj.pharmacy_name = pharmacy_name

        # ✅ IMAGE CHECK
        if image:
            if not image.content_type.startswith('image'):
                messages.error(request, "Upload a valid image file")
                return redirect('/pharmacist_Profile')
            obj.image = image

        obj.save()

        messages.success(request, "Profile updated successfully")
        return redirect('/pharmacist_Profile')

    return render(request, 'Pharmacist/update_pharmacist_Profile.html', {'data': data})


def addmedicine(request):
    uid=request.session['uid']
    Pid=Pharmacist.objects.get(loginId=uid)
    if request.POST:
        name=request.POST.get('name')
        price=request.POST.get('price')
        desc=request.POST.get('desc')
        qty=request.POST.get('qty')
        date=request.POST.get('date')
        expiry=request.POST.get('expiry')
        side_effects=request.POST.get('side_effects')
        orginal_Price=request.POST.get('orginal_Price')
        image = request.FILES["image"]
        ins=Medicine.objects.create(name=name,price=price,desc=desc,qty=qty,image=image,date=date,expiry=expiry,side_effects=side_effects,orginal_Price=orginal_Price,pid=Pid)
        ins.save()
        messages.success(request,"Medicine added successfully..")
        return redirect('/view_medicine')


        
    return render(request,'Pharmacist/addmedicine.html')




def Update_Medicine(request):
    id = request.GET['id']
    data = Medicine.objects.filter(id=id)

    if request.method == 'POST':
       
        name=request.POST.get('name')
        price=request.POST.get('price')
        desc=request.POST.get('desc')
        qty=request.POST.get('qty')
        date=request.POST.get('date')
        expiry=request.POST.get('expiry')
        orginal_Price=request.POST.get('orginal_Price')
        side_effects=request.POST.get('side_effects')

      
        if 'image' in request.FILES:
            image = request.FILES['image']

            data = Medicine.objects.get(id=id)
            data.name=name
            data.price=price
            data.desc=desc
            data.qty=qty
            data.date=date
            data.expiry=expiry
            data.orginal_Price=orginal_Price
            data.side_effects=side_effects
            data.image = image
            data.save()
        else:
            Medicine.objects.filter(id=id).update(name=name,price=price,desc=desc,qty=qty,side_effects=side_effects,orginal_Price=orginal_Price)

        messages.success(request, 'updated successfully')
        return redirect('/view_medicine')
    return render(request,'Pharmacist/update_medicine.html',{'data':data})


def delete_med(request):
    id=request.GET.get('id')
    Dele=Medicine.objects.filter(id=id).delete()
    messages.success(request,"Product Deleted")
    return redirect('/view_medicine')

def view_medicine(request):
    data=Medicine.objects.all()
    return render(request,'Pharmacist/view_medicine.html',{'data':data})

def view_medicineDetails(request):
    id=request.GET['id']
    data=Medicine.objects.filter(id=id)
    return render(request,"Pharmacist/view_medicineDetails.html",{'data':data})



def ph_view_prescription(request):
    uid=request.session['uid']
    ph=Pharmacist.objects.get(loginId=uid)
    data=Prescription.objects.filter(pharmacist=ph)
    return render(request,'Pharmacist/ph_view_prescription.html',{'data':data})


# def sales_Medicine(request):
#     prescription_id = request.GET.get('id')
#     uid = request.session.get('uid')

  
#     ph = Pharmacist.objects.filter(loginId=uid).first()
#     if not ph:
#         return redirect('/pharmacist_home')

#     prescription = get_object_or_404(Prescription, id=prescription_id)
#     # patient = prescription.patient
#     user=prescription.uid  
#     medicines = Medicine.objects.all()

#     if request.method == "POST":
#         med_id = request.POST.get('medicine')
#         qty = int(request.POST.get('qty', 1)) 
#         medicine = get_object_or_404(Medicine, id=med_id)

        
       
#         # sale = Sales.objects.create(
#         #     ph=ph,
#         #     medicine=medicine,
#         #     patient=patient,  
#         #     status="Sold"
#         # )

       
#         medicine.qty -= qty
#         medicine.save()

       
#         total_price = qty * medicine.price
#         MedicineOrder.objects.create(
#             Pharmacist=ph,
            
#             mid=medicine,
#             qty=qty,
#             uid=user,
#             # price=medicine.price,
#             total=total_price,
#             status="Sold"
#         )

#         return redirect('/')

#     return render(request, "Pharmacist/sales_Medicine.html", {
#         'medicines': medicines,
#         'prescription': prescription,
#         # 'patient': patient,
#         'user':user,
#         'ph': ph
#     })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Prescription, Medicine, MedicineOrder, Pharmacist

def sales_Medicine(request):
    prescription_id = request.GET.get('id')
    uid = request.session.get('uid')

    # Get the logged-in pharmacist
    ph = Pharmacist.objects.filter(loginId=uid).first()
    if not ph:
        return redirect('/pharmacist_home')

    # Get prescription details
    prescription = get_object_or_404(Prescription, id=prescription_id)
    user = prescription.uid  

    # Get the medicine prescribed
    try:
        medicine = Medicine.objects.get(name=prescription.medicine_name)
    except Medicine.DoesNotExist:
        messages.error(request, "Medicine not found in stock.")
        return redirect('/pharmaHome')

    prescribed_quantity = prescription.quantity  # Quantity from prescription

    if request.method == "POST":
        if medicine.qty >= prescribed_quantity:
            medicine.qty -= prescribed_quantity  # Deduct from stock
            medicine.save()

            # Create Medicine Order
            total_price = prescribed_quantity * medicine.price
            MedicineOrder.objects.create(
                Pharmacist=ph,
                mid=medicine,
                qty=prescribed_quantity,
                uid=user,
                total=total_price,
                status="Sold"
            )

            messages.success(request, f"Medicine '{medicine.name}' sold successfully!")
            return redirect('/pharmaHome')
        else:
            messages.error(request, "Not enough stock available!")

    return render(request, "Pharmacist/sales_Medicine.html", {
        'prescription': prescription,
        'medicine': medicine,
        'user': user,
        'ph': ph
    })


from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import MedicineOrder, Medicine, Pharmacist

def pharmacist_view_orders(request):
    uid=request.session['uid']

    pharmacist = Pharmacist.objects.get(loginId=uid)  # Get logged-in pharmacist
    orders = MedicineOrder.objects.filter(status="pending_pharmacist")

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        try:
            order = MedicineOrder.objects.get(id=order_id)
            medicine = order.mid
            total_price = order.qty * medicine.price  # Calculate total price

            with transaction.atomic():  # Ensure database integrity
                if medicine.qty >= order.qty:
                    
                    medicine.qty -= order.qty
                    medicine.save()

                    
                    order.total = total_price
                    order.Pharmacist = pharmacist 
                    order.status = "waiting_payment"
                    order.save()

                    messages.success(request, f"Order {order.id} confirmed by {pharmacist.name}. Total: ${total_price}")
                else:
                    messages.error(request, f"Not enough stock for {medicine.name}! Available: {medicine.qty}")

        except MedicineOrder.DoesNotExist:
            messages.error(request, "Order not found.")

    return render(request, "pharmacist/view_orders.html", {"orders": orders})





from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from .models import MedicineOrder, Pharmacist, Medicine

def pharmacist_view_orders(request):
    uid = request.session.get('uid')

    try:
        pharmacist = Pharmacist.objects.get(loginId=uid)  # Get logged-in pharmacist
    except Pharmacist.DoesNotExist:
        messages.error(request, "Pharmacist not found.")
        return redirect("login")  # Redirect if pharmacist not found

    orders = MedicineOrder.objects.filter(status="pending_pharmacist")

    if request.method == "POST":
        order_id = request.POST.get("order_id")

        try:
            order = MedicineOrder.objects.get(id=order_id)
            medicine = order.mid
            total_price = order.qty * medicine.price  # Calculate total price

            with transaction.atomic():  # Ensure database integrity
                if medicine.qty >= order.qty:
                    # Reduce stock
                    medicine.qty -= order.qty
                    medicine.save()

                    # Calculate Profit
                    profit = (medicine.price - medicine.orginal_Price) * order.qty  

                    # Update order
                    order.total = total_price
                    order.profit = profit  # Store profit
                    order.Pharmacist = pharmacist 
                    order.status = "waiting_payment"
                    order.save()

                    messages.success(request, f"Order {order.id} confirmed by {pharmacist.name}. Total: ₹{total_price}, Profit: ₹{profit}")
                else:
                    messages.error(request, f"Not enough stock for {medicine.name}! Available: {medicine.qty}")

        except MedicineOrder.DoesNotExist:
            messages.error(request, "Order not found.")

    # Calculate total profit of the pharmacist
    total_profit = MedicineOrder.objects.filter(Pharmacist=pharmacist).aggregate(Sum('profit'))['profit__sum'] or 0

    return render(request, "pharmacist/view_orders.html", {"orders": orders, "total_profit": total_profit})






from django.shortcuts import render, redirect, get_object_or_404
from .models import MedicineOrder, Invoice, Pharmacist

def paid_orders_view(request):
    paid_orders = MedicineOrder.objects.filter(status="Paid")
    return render(request, "pharmacist/paid_orders.html", {"paid_orders": paid_orders})



def invoice_details(request):
    id=request.GET['id']
    invoice =MedicineOrder.objects.filter(id=id)
    return render(request,"pharmacist/invoice_details.html",{"invoice": invoice})


 
# from django.shortcuts import render
# from .models import MedicineOrder

# from django.shortcuts import render
# from django.db.models import Sum, F, ExpressionWrapper, IntegerField
# from .models import MedicineOrder

# def profit_report(request):
#     # Calculate total profit dynamically
#     total_profit = MedicineOrder.objects.filter(status='paid').annotate(
#         profit_per_item=ExpressionWrapper(
#             (F('mid__price') - F('mid__orginal_Price')) * F('qty'),
#             output_field=IntegerField()
#         )
#     ).aggregate(Sum('profit_per_item'))['profit_per_item__sum'] or 0

#     # Calculate profit per medicine
#     medicine_profits = MedicineOrder.objects.filter(status='paid').values(
#         'mid__name'
#     ).annotate(
#         total_profit=Sum(
#             ExpressionWrapper(
#                 (F('mid__price') - F('mid__orginal_Price')) * F('qty'),
#                 output_field=IntegerField()
#             )
#         )
#     )

#     return render(request, 'Admin/profit_report.html', {
#         'total_profit': total_profit,
#         'medicine_profits': medicine_profits
#     })




from django.shortcuts import render
from django.db.models import F, ExpressionWrapper, IntegerField, Sum
from .models import MedicineOrder

# def profit_report(request):
#     # Calculate profit per order on the fly
#     profit_expression = ExpressionWrapper(
#         (F('mid__price') - F('mid__orginal_Price')) * F('qty'),
#         output_field=IntegerField()
#     )

#     # Total profit across all paid orders
#     total_profit = MedicineOrder.objects.filter(status='paid').annotate(
#         order_profit=profit_expression
#     ).aggregate(total_profit=Sum('order_profit'))['total_profit'] or 0

#     # Profit per medicine (grouped by medicine name)
#     medicine_profits = MedicineOrder.objects.filter(status='paid').annotate(
#         order_profit=profit_expression
#     ).values('mid__name').annotate(total_profit=Sum('order_profit'))

#     return render(request, 'Admin/profit_report.html', {
#         'total_profit': total_profit,
#         'medicine_profits': medicine_profits
#     })


def profit_report(request):
   

    data=MedicineOrder.objects.filter(status="Paid")
    return render(request,'Admin/profit_report.html',{'data':data})
  

from django.shortcuts import render 
from .models import MedicineOrder

# def pharmacist_total_profit(request):
#     pharmacist_id = request.GET.get('pharmacist_id')  # Get pharmacist ID from request

#     # Calculate total profit for the logged-in pharmacist
#     total_profit = MedicineOrder.objects.filter(Pharmacist_id=pharmacist_id).aggregate(total=models.Sum('profit'))['total']

#     if total_profit is None:
#         total_profit = 0  # If no orders, profit is 0

#     return render(request, 'pharmacist/profit.html', {'total_profit': total_profit})

from django.shortcuts import render

from django.db.models import Sum
from .models import MedicineOrder, Pharmacist

# def pharmacist_view_profit(request):
#     uid = request.session.get('uid')

#     try:
#         pharmacist = Pharmacist.objects.get(loginId=uid)
#     except Pharmacist.DoesNotExist:
#         messages.error(request, "Pharmacist not found.")
#         return redirect("login")

#     # Calculate total profit for logged-in pharmacist
#     total_profit = MedicineOrder.objects.filter(Pharmacist=pharmacist).aggregate(Sum('profit'))['profit__sum'] or 0

#     return render(request, "pharmacist/profit.html", {"total_profit": total_profit})

def pharmacist_view_profit(request):
    uid = request.session['uid']
    pharmacist = Pharmacist.objects.get(loginId=uid)  # Get the logged-in pharmacist

    # Calculate total profit for this pharmacist
    total_profit = MedicineOrder.objects.filter(Pharmacist=pharmacist,status="Paid").aggregate(Sum('profit'))['profit__sum'] or 0

    # Fetch all medicine orders with profit details for the pharmacist
    orders = MedicineOrder.objects.filter(Pharmacist=pharmacist,status="Paid").select_related('mid')

    return render(request, "pharmacist/profit.html", {"orders": orders, "total_profit": total_profit, "pharmacist": pharmacist})


#--------Doctor------------#


def doctorHome(request):
    return render(request,'doctor/index.html')
def DoctorProfile(request):
    uid=request.session['uid']
    data=Doctor.objects.filter(loginId=uid)
    return render(request,'Doctor/DoctorProfile.html',{'data':data})

import re

def update_DoctorProfile(request):
    uid = request.session.get('uid')
    data = Doctor.objects.filter(loginId=uid)

    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        medical_license_number = request.POST.get("medical_license_number")
        specialization = request.POST.get("specialization")
        image = request.FILES.get("image")

        # NAME VALIDATION
        if not re.match(r"^[A-Za-z ]{3,50}$", name):
            messages.error(request, "Invalid name")
            return redirect('/DoctorProfile')

        # PHONE VALIDATION
        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Phone must be 10 digits")
            return redirect('/DoctorProfile')

        # ADDRESS
        if len(address) < 5:
            messages.error(request, "Address too short")
            return redirect('/DoctorProfile')

        doctor = Doctor.objects.get(loginId=uid)

        doctor.name = name
        doctor.phone = phone
        doctor.address = address
        doctor.medical_license_number = medical_license_number
        doctor.specialization = specialization

        if image:
            if not image.content_type.startswith('image'):
                messages.error(request, "Upload valid image")
                return redirect('/DoctorProfile')
            doctor.image = image

        doctor.save()

        messages.success(request, "Profile updated successfully")
        return redirect('/DoctorProfile')

    return render(request,'Doctor/update_DoctorProfile.html',{'data':data})


def doc_view_bookings(request):
    uid = request.session['uid']
    Doc = Doctor.objects.get(loginId=uid)

    # ✅ Show Booked + Accepted
    view = Appointments.objects.filter(did=Doc, status__in=["Booked", "Accepted"])

    return render(request,'doctor/doc_view_bookings.html',{"view":view})


def accept_appointment(request):
    id = request.GET.get('id')
    app = Appointments.objects.get(id=id)
    app.status = "Accepted"
    app.save()
    return redirect('/accepted_appointments')


def reject_appointment(request):
    id = request.GET.get('id')
    app = Appointments.objects.get(id=id)
    app.status = "Rejected"
    app.save()
    return redirect('/accepted_appointments')

def payment(request):
    id = request.GET.get('id')
    app = Appointments.objects.get(id=id)

    if request.method == "POST":
        method = request.POST.get("payment_method")

        # ✅ UPI Payment
        if method == "upi":
            upi_id = request.POST.get("upi_id")
            if not upi_id:
                messages.error(request, "Enter UPI ID")
                return redirect(request.path + f"?id={id}")

        # ✅ Card Payment
        elif method == "card":
            name = request.POST.get("name")
            card = request.POST.get("card")
            expiry = request.POST.get("expiry")
            cvv = request.POST.get("cvv")

            if not (name and card and expiry and cvv):
                messages.error(request, "Fill all card details")
                return redirect(request.path + f"?id={id}")

        # ✅ COD Payment
        elif method == "cod":
            # No validation needed
            pass

        else:
            messages.error(request, "Select payment method")
            return redirect(request.path + f"?id={id}")

        # ✅ FINAL SAVE (COMMON FOR ALL METHODS)
        app.status = "Paid"
        app.save()

        messages.success(request, f"{method.upper()} Payment Successful")
        return redirect('/userHome')

    return render(request, 'User/payment.html', {'app': app})


def accepted_appointments(request): 
    uid = request.session['uid']
    dr = Doctor.objects.get(loginId=uid)

    # ✅ Show BOTH Paid + Completed
    data = Appointments.objects.filter(did=dr, status__in=["Paid", "Completed"])

    return render(request,'Doctor/accepted_appointments.html',{'data':data})


# def prescription_patient(request):
#     appointment_id = request.GET.get('id')  
#     appointment = get_object_or_404(Appointments, id=appointment_id)  

#     try: 
#         uid = request.session.get('uid')
#         doctor = Doctor.objects.get(loginId=uid)
#         pharmacists = Pharmacist.objects.all()
#         user = appointment.uid  

#         # Check if a prescription already exists for this appointment
#         existing_prescription = Prescription.objects.filter(uid=user, doctor=doctor).first()

#         if existing_prescription:
#             messages.warning(request, "Prescription already created for this appointment.")
#             return redirect('/doctorHome')  # Redirect to doctor home or any relevant page

#         if request.method == "POST":
#             pharmacist_id = request.POST["pharmacist"]
#             medicines = request.POST["medicines"]
#             instructions = request.POST["instructions"]
            
#             pharmacist = Pharmacist.objects.get(id=pharmacist_id)

#             # Create a new prescription only if it doesn't exist
#             Prescription.objects.create(
#                 doctor=doctor,
#                 uid=user,
#                 pharmacist=pharmacist,
#                 medicines=medicines,
#                 instructions=instructions,
#             )

#             messages.success(request, "Prescription created successfully and sent to the pharmacist!")
#             return redirect('/doctorHome')  

#     except Doctor.DoesNotExist:
#         messages.error(request, "Doctor not found")
#     except Pharmacist.DoesNotExist:
#         messages.error(request, "Pharmacist not found")

#     return render(
#         request, 
#         'doctor/prescription_patient.html', 
#         {'pharmacists': pharmacists, 'appointment': appointment}
#     )
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Prescription, Doctor, Pharmacist, Appointments, Medicine

def prescription_patient(request):

    appointment_id = request.GET.get('id')
    appointment = Appointments.objects.get(id=appointment_id)

    uid = request.session.get('uid')
    doctor = Doctor.objects.get(loginId=uid)

    pharmacists = Pharmacist.objects.all()
    user = appointment.uid

    # ❗ Check already exists
    existing = Prescription.objects.filter(appointment=appointment).first()
    if existing:
        messages.error(request, "Prescription already created")
        return redirect('/accepted_appointments')

    # ❗ Allow only if paid
    if appointment.status != "Paid":
        messages.error(request, "Payment not completed")
        return redirect('/accepted_appointments')

    if request.method == "POST":

        pharmacist_id = request.POST.get("pharmacist")
        medicine_id = request.POST.get("medicine")
        quantity = request.POST.get("quantity")
        dosage = request.POST.get("dosage")
        instructions = request.POST.get("instructions")

        pharmacist = Pharmacist.objects.get(id=pharmacist_id)
        medicine = Medicine.objects.get(id=medicine_id)

        quantity = int(quantity)

        # ❗ Stock validation
        if quantity > medicine.qty:
            messages.error(request, "Not enough stock")
            return redirect(request.path)

        # ✅ Create prescription
        Prescription.objects.create(
            doctor=doctor,
            uid=user,
            pharmacist=pharmacist,
            appointment=appointment,
            medicine_name=medicine.name,
            quantity=quantity,
            dosage=dosage,
            instructions=instructions,
        )

        # ✅ Update appointment
        appointment.status = "Completed"
        appointment.save()

        messages.success(request, "Prescription created successfully")

        return redirect('/accepted_appointments')

    return render(request, 'doctor/prescription_patient.html', {
        'pharmacists': pharmacists,
        'appointment': appointment
    })

from django.http import JsonResponse

def get_medicines(request):
    pharma_id = request.GET.get('pharma_id')

    medicines = Medicine.objects.filter(pid_id=pharma_id)

    data = []
    for m in medicines:
        data.append({
            'id': m.id,
            'name': m.name,
            'qty': m.qty
        })

    return JsonResponse({'medicines': data})
# def dr_viewMedicine(request):
#     data=Medicine.objects.all()
#     return render(request,'doctor/dr_viewMedicine.html',{'data':data})




def dr_viewMedicine(request):
    query = request.GET.get('q')  
    if query:
        data = Medicine.objects.filter(name__icontains=query)  
    else:
        data = Medicine.objects.all()  

    return render(request, 'doctor/dr_viewMedicine.html', {'data': data, 'query': query})


def dr_viewMedicinedetails(request):
    id=request.GET['id']
    data=Medicine.objects.filter(id=id)
    return render(request,'doctor/dr_viewMedicinedetails.html',{'data':data})


#-----------USER--------#
def userHome(request):
    return render(request,'User/index.html')

def viewPharmacist(request):
    return render(request,'User/viewPharmacist.html')


def UserProfile(request):
    uid=request.session['uid']
    data=User.objects.filter(loginId=uid)
    return render(request,'User/UserProfile.html',{'data':data})

import re
from django.contrib import messages
from django.shortcuts import redirect, render

def update_userProfile(request):
    uid = request.session.get('uid')
    data = User.objects.filter(loginId=uid)

    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        image = request.FILES.get("image")

        # 🔴 NAME VALIDATION
        if not re.match(r"^[A-Za-z ]{3,50}$", name):
            messages.error(request, "Name must contain only letters (3–50 chars)")
            return redirect('/UserProfile')

        # 🔴 PHONE VALIDATION (ONLY DIGITS)
        if not phone.isdigit():
            messages.error(request, "Phone must contain only digits")
            return redirect('/UserProfile')

        if len(phone) != 10:
            messages.error(request, "Phone must be exactly 10 digits")
            return redirect('/UserProfile')

        # 🔴 ADDRESS VALIDATION
        if len(address) < 5 or len(address) > 100:
            messages.error(request, "Address must be 5–100 characters")
            return redirect('/UserProfile')

        user_obj = User.objects.get(loginId=uid)

        user_obj.name = name
        user_obj.phone = int(phone)   # ✅ only digits stored
        user_obj.address = address

        # 🔴 IMAGE VALIDATION
        if image:
            if not image.content_type.startswith('image'):
                messages.error(request, "Upload a valid image file")
                return redirect('/UserProfile')
            user_obj.image = image

        user_obj.save()

        messages.success(request, "Profile updated successfully")
        return redirect('/UserProfile')

    return render(request, 'User/update_userProfile.html', {'data': data})
def bookAppointment(request):

    uid=request.session['uid']
    Uid=User.objects.get(loginid=uid)
    
    did=request.GET.get('did')
    Doc=Doctor.objects.get(loginid=did)
    Did=Doctor.objects.filter(loginid=did)
    
    if request.POST:
        date=request.POST.get('date')
        time=request.POST.get('time')
        desc=request.POST.get('desc')
        
        ins=Appointments.objects.create(did=Doc,uid=Uid,date=date,time=time,desc=desc,status='Booked')
        ins.save()
        messages.success(request,"Booked Successfully")
        return redirect("/users_view_doc")
    # return render(request, "User/book_doctor.html",{"view":Did})
    return render(request,'User,bookAppointment.html')

from datetime import date
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, Doctor, Appointments

from datetime import date

def book_appoinment(request):

    uid = request.session.get('uid')
    users = User.objects.get(loginId=uid)
    drs = Doctor.objects.all()

    if request.method == "POST":

        dr_id = request.POST.get("dr")
        dr = Doctor.objects.get(id=dr_id)

        selected_date = request.POST.get('date')
        time = request.POST.get('time')
        desc = request.POST.get('desc')

        selected_date_obj = date.fromisoformat(selected_date)

        if selected_date_obj < date.today():
            messages.error(request, "You cannot book an appointment for a past date.")
            return redirect("/book_appointment")

        # Prevent same doctor same date same time
        if Appointments.objects.filter(did=dr, date=selected_date, time=time).exists():
            messages.error(request, "This doctor is already booked at this time. Choose another time.")
            return redirect("/book_appointment")

        else:

            Appointments.objects.create(
                uid=users,
                did=dr,
                date=selected_date,
                time=time,
                desc=desc,
                status="Booked"
            )

            messages.success(request, "Appointment booked successfully!")
            return redirect("/userHome")

    return render(request, 'user/book_appointment.html', {"drs": drs})




def view_bookedappointment(request):
    uid=request.session['uid']
    user=User.objects.get(loginId=uid)
    data=Appointments.objects.filter(uid=user)
    return render(request,'user/view_bookedappointment.html',{'data':data})



def view_prescription(request):
    uid=request.session['uid']
    user=User.objects.get(loginId=uid)
    data=Prescription.objects.filter(uid=user)
    return render(request,'User/view_prescription.html',{'data':data})


def add_to_cart(request):
    uid=request.session['uid']
    id=request.GET['id']
    cus=User.objects.get(loginId=uid)
    med=Medicine.objects.get(id=id)
    # if MedicineOrder.objects.filter(mid=id,uid=cus,status="in_cart").exists():
    #     messages.info(request,"already added")
    # else:
    MedicineOrder.objects.create(uid=cus,mid=med)
    messages.info(request,"successfully Added")
    return redirect('/place_order')





def ph_givenMedicine(request):
    uid=request.session['uid']
    obj=User.objects.get(loginId=uid)
    data=MedicineOrder.objects.filter(uid=obj)
    return render(request,'User/ph_givenMedicine.html',{'data':data})


def user_payment_page(request):
    mid = request.GET['mid']
    product = MedicineOrder.objects.get(id=mid)
    if request.POST:
        obj=MedicineOrder.objects.filter(id=mid).update(status="Paid")
        return redirect("/userHome")
    return render(request,'User/user_payment_page.html',{'product':product})



def user_viewMedicine(request):
    data=Medicine.objects.all()
    return render(request,'User/user_viewMedicine.html',{'data':data})


def user_viewMedicineDetails(request):
    id=request.GET['id']
    data=Medicine.objects.filter(id=id)
    return render(request,'User/user_viewMedicineDetails.html',{'data':data})




def medicine_payment(request):
    uid = request.session['uid']
    cus = User.objects.get(loginId=uid)
    pro = MedicineOrder.objects.filter(uid=cus)

    if request.method == "POST":
        try:
            qty = int(request.POST.get('qty', 0))
            id = request.POST.get('id')

            if not id or qty <= 0:
                messages.error(request, "Invalid input. Please enter a valid quantity.")
                return redirect('/medicine_payment')

            cart_item = MedicineOrder.objects.get(id=id)
            product = cart_item.mid
            if product.qty is None:
                messages.error(request, f"Stock information is unavailable for {product.name}.")
            elif qty > product.qty:
                messages.error(request, f"Only {product.qty} items are available in stock for {product.name}.")
            else:
                with transaction.atomic(): 
                    total = qty * int(product.price)
                    cart_item.qty = qty
                    cart_item.total = total
                    cart_item.status = "Paid"
                    cart_item.save()

                    product.qty -= qty
                    product.save()

                    messages.success(request, f"Order placed successfully for {product.name}! Remaining stock: {product.qty}")
        except ValueError:
            messages.error(request, "Invalid quantity entered.")
        except MedicineOrder.DoesNotExist:
            messages.error(request, "The selected product does not exist.")
        return redirect('/medicine_payment')
    return render(request, 'User/medicine_payment.html', {'pro': pro})


from django.shortcuts import render, redirect
from .models import MedicineOrder, Medicine

# def place_order(request):
#     uid = request.session['uid']
#     user = User.objects.get(loginId=uid)
#     pro = MedicineOrder.objects.filter(uid=user)
#     ph=Pharmacist.objects.all()
#     if request.method == "POST":
#         pharmacist_id=request.POST.get('pharmacist_id')
#         medicine_id = request.POST.get("medicine_id")
#         qty = int(request.POST.get("qty"))
#         pharmacist = Pharmacist.objects.get(id=pharmacist_id)
#         medicine = Medicine.objects.get(id=medicine_id)

#         order = MedicineOrder.objects.create(
#             uid=user, mid=medicine, qty=qty, pharmacist=pharmacist, status="pending_pharmacist"
#         )

#         return redirect("/userHome")  # Redirect user to their orders page

#     medicines = Medicine.objects.all()
#     return render(request, "user/place_order.html", {"medicines": medicines,"ph":ph})

# from django.shortcuts import render, redirect
# from pharmacyapp.models import MedicineOrder, Medicine, Pharmacist, User

def place_order(request):
    uid = request.session['uid']
    user = User.objects.get(loginId=uid)
    ph = Pharmacist.objects.all()  
    medicines = Medicine.objects.all()  

    if request.method == "POST":
        pharmacist_id = request.POST.get('pharmacist_id')
        medicine_id = request.POST.get("medicine_id")
        qty = int(request.POST.get("qty"))

        pharmacist = Pharmacist.objects.get(id=pharmacist_id)
        medicine = Medicine.objects.get(id=medicine_id)

      
        order = MedicineOrder.objects.create(
            uid=user, mid=medicine, qty=qty, Pharmacist=pharmacist, status="pending_pharmacist"
        )

        return redirect("/userHome") 

    return render(request, "user/place_order.html", {"medicines": medicines, "ph": ph})


def confirmorder(request):
    uid = request.session['uid']
    user = User.objects.get(loginId=uid)
    orders = MedicineOrder.objects.filter(uid=user,status="waiting_payment")
    return render(request, "user/confirmorder.html", {"orders": orders})

def confirm_payment(request, order_id):
    try:
        order = MedicineOrder.objects.get(id=order_id, status="waiting_payment")
        order.status = "Paid"
        order.save()
        messages.success(request, "Payment successful!")
    except MedicineOrder.DoesNotExist:
        messages.error(request, "Invalid order.")

    return redirect("/userHome")


def invoice(request):
    uid=request.session['uid']
    user=User.objects.get(loginId=uid)
    invoice=MedicineOrder.objects.filter(uid=user)
    return render(request,'User/invoice_details.html',{'invoice':invoice})




import subprocess
from django.shortcuts import redirect

def chat(request):
    subprocess.Popen(['python', 'chatgui.py'])
    return redirect("/userHome")






def expiredStock(request):
    data = Medicine.objects.filter(expiry__lt=now().date())  
    return render(request, 'Admin/expiredStock.html', {'data': data})








#------------------Chat------------------#


def chats(request):
    uid = request.session["uid"]
    name = ""
    artistData = Doctor.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(sellerid__loginId=uid) & Q(customerid=id))
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    userid = User.objects.get(loginId=uid)
    if id:
        customerid = Doctor.objects.get(id=id)
        name = customerid.name
        # + " " + customerid.lastName
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            sellerid=userid, message=message, customerid=customerid, time=formatted_time, utype="SELLER")
        sendMsg.save()
    return render(request,"User/reciever.html", {"artistData": artistData, "getChatData": getChatData, "customerid": name, "id": id})


def reply(request):
    uid = request.session["uid"]
    name = ""
    userData = User.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(customerid__loginId=uid) & Q(sellerid=id))
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    customerid = Doctor.objects.get(loginId=uid)
    if id:
        userid = User.objects.get(id=id)
        name = userid.name 
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            sellerid=userid, message=message, customerid=customerid, time=formatted_time, utype="CUSTOMER")
        sendMsg.save()
    return render(request, "Doctor/sender.html", {"userData": userData, "getChatData": getChatData, "userid": name, "id": id})



def admin_view_user(request):


    data = User.objects.all()
    return render(request, 'Admin/admin_view_user.html', {'data': data})

def approve_user(request):
    uid = request.GET.get('uid')
    user = Login.objects.get(id=uid)
    user.is_active = 1
    user.save()
    return redirect('/admin_view_user')

def reject_user(request):
    uid = request.GET.get('uid')

    login = Login.objects.get(id=uid)

    # delete user table data
    User.objects.filter(loginId=login).delete()

    # delete login
    login.delete()

    return redirect('/admin_view_user')