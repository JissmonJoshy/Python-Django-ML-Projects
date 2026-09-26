from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,"index.html")

def userReg(request):
    msg = ''
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        try:
            usr = User.objects.create_user(
                username=email, password=password, is_active=1)
            usr.save()
            par = Customer.objects.create(
                name=name, email=email, phone=phone, address=address, user=usr)
            par.save()
            msg = 'Registration Successful..'
            return render(request, 'userReg.html', {"msg": msg})
        except:
            msg = 'Username already registred..'
            return render(request, 'userReg.html', {"msg": msg})

    else:
        return render(request, 'userReg.html', {"msg": msg})


def managerReg(request):
    msg = ''
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        location = request.POST['location']
        try:
            usr = User.objects.create_user(
                username=email, password=password, is_staff=1, is_active=0)
            usr.save()
            par = Manager.objects.create(
                name=name, email=email, phone=phone, address=address, location=location,user=usr)
            par.save()
            msg = 'Registration Successful..'
            return render(request, 'managerReg.html', {"msg": msg})
        except:
            msg = 'Username already registred..'
            return render(request, 'managerReg.html', {"msg": msg})

    else:
        return render(request, 'managerReg.html', {"msg": msg})
 

def login(request):
    msg = ''
    if request.method == 'POST':
        email = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_superuser:
                return redirect("/adminHome")
            elif user.is_staff:
                data = Manager.objects.get(email=email)
                request.session['id'] = data.id
                return redirect("/managerHome")
            else:
                data = Customer.objects.get(email=email)
                request.session['id'] = data.id
                return redirect("/userHome")
        else:
            msg = 'Invalid Username/Password!'
            return render(request, 'login.html', {"msg": msg})

    else:
        return render(request, 'login.html')
    

def adminHome(request):
    return render(request,"adminHome.html")

def adminUser(request):
    data=Customer.objects.filter().order_by("-id")
    return render(request,"adminUser.html",{"data":data})

def adminManager(request):
    data=Manager.objects.filter().order_by("-id")
    return render(request,"adminManager.html",{"data":data})

def adminActive(request):
    id = request.GET['id']
    status = request.GET['status']
    data = User.objects.get(id=id)
    data.is_active = status
    data.save()
    return redirect("/adminManager")

def adminActiveUser(request):
    id = request.GET['id']
    status = request.GET['status']
    data = User.objects.get(id=id)
    data.is_active = status
    data.save()
    return redirect("/adminUser")

def adminReport(request):
    selected_month = request.GET.get('month', '')
    bok = Booking.objects.filter().order_by("-id")
    
    if selected_month:
        try:
            year, month = map(int, selected_month.split('-'))
            bok = bok.filter(date__year=year, date__month=month)
        except ValueError:
            return render(request, "shopReport.html", {"bok": bok, "error": "Invalid month format", "selected_month": selected_month})
    
    total_price = sum(b.slot.price for b in bok)
    return render(request, "adminReport.html", {"bok": bok, "selected_month": selected_month, "growth_total_price": total_price})


def adminComplaints(request):
    data=Complaint.objects.filter().order_by("-id")
    return render(request,"adminComplaints.html",{"data":data})



def userHome(request):
    return render(request,"userHome.html")

def userParkings(request):
    data=Manager.objects.filter().order_by("-id")
    return render(request,"userParkings.html",{"data":data})

def userAvailableSlots(request):
    id=request.GET['id']
    data=Slot.objects.filter(amount__man_id=id).order_by('slot')

    if request.POST:
        type=request.POST['type']
        data=Slot.objects.filter(type=type,amount__man_id=id)
        return render(request,"userAvailableSlots.html",{"data":data})

    return render(request,"userAvailableSlots.html",{"data":data})

def userPay(request):
    uid=request.session['id']
    user=Customer.objects.get(id=uid)
    id=request.GET['id']
    data=Slot.objects.get(id=id)
    rate=data.price
    if request.POST:
        messages.info(request,"Payment Successfull...")
        bok=Booking.objects.create(user=user,slot=data,status="Booked")
        data.status="Unavailable"
        data.save()
        bok.save()
        return redirect("/userBookings")
    return render(request,"userPay.html",{"rate":rate})

def userBookings(request):
    selected_month = request.GET.get('month', '')
    uid=request.session['id']
    bok=Booking.objects.filter(user=uid).order_by("-id")

    if selected_month:
        try:
            year, month = map(int, selected_month.split('-'))
            bok = bok.filter(date__year=year, date__month=month)
        except ValueError:
            return render(request, "shopReport.html", {"bok": bok, "error": "Invalid month format", "selected_month": selected_month})
    
    total_price = sum(b.slot.price for b in bok)
    return render(request,"userBookings.html",{"bok":bok, "selected_month": selected_month, "growth_total_price": total_price})

def userProfile(request):
    uid=request.session['id']
    user=Customer.objects.get(id=uid)
    cus=user.user

    name=user.name
    email=user.email
    phone=user.phone
    address=user.address

    if request.method == "POST":
        name=request.POST['name']
        new_email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        password=request.POST.get('password', None)

        existing_user=User.objects.filter(username=new_email).exclude(id=cus.id).first()

        if existing_user:
            messages.error(request, "This email is already registered. Please use a different email.")
            return redirect("/userProfile")
        user.name=name
        user.email=new_email
        user.phone=phone
        user.address=address
        user.save()

        cus.username =new_email
        if password:
            cus.set_password(password)
        cus.save()
        messages.info(request,"Profile Updated")
        return redirect("/userProfile")

    return render(request,"userProfile.html",{"name":name,"email":email,"phone":phone,"address":address})
    
def userComplaint(request):
    uid=request.session['id']
    user=Customer.objects.get(id=uid)
    if request.POST:
        message=request.POST['message']
        comp=Complaint.objects.create(user=user,complaint=message)
        comp.save()
        messages.info(request,"Complaint Registered")
        return redirect("/userComplaint")

    return render(request,"userComplaint.html")



def managerHome(request):
    return render(request,"managerHome.html")

def manAmount(request):
    uid=request.session['id']
    man=Manager.objects.get(id=uid)
    am=Amount.objects.filter(man_id=uid).order_by("-id")
    if request.POST:
        type=request.POST['type']
        price=request.POST['price']
        amount=Amount.objects.filter(type=type,man=man).first()
        if amount:
            amount.price=price
            amount.save()
            messages.info(request,"Amount Updated...")
            return redirect("/manAmount")
        else:
            amoun=Amount.objects.create(price=price,type=type,man=man)
            amoun.save()
            messages.info(request,"Amount added...")
            return redirect("/manAmount")
    else:
        return render(request,"manAmount.html",{"am":am})

def manSlot(request):
    uid=request.session['id']
    man=Manager.objects.get(id=uid)
    sl=Slot.objects.filter(amount__man_id=uid).order_by("slot")

    if request.POST:
        number=request.POST['number']
        type=request.POST['type']
        amount=Amount.objects.filter(man_id=uid,type=type).first()
        if amount:
            slot=Slot.objects.filter(slot=number,amount__man_id=uid).first()
            if slot:
                messages.info(request,"Slot no. already added, choose another slot")
                return redirect("/manSlot")
            else:
                am=Amount.objects.filter(type=type,man_id=uid).first()
                if amount:
                    price=am.price
                slo=Slot.objects.create(slot=number,price=price,type=type,amount=amount)
                slo.save()
                messages.info(request,"Slot added successfully.")
                return redirect("/manSlot")
        else:
            messages.info(request,"Add the vehiles price first")
            return redirect("/manSlot")
    else:
        return render(request,"manSlot.html",{"data":sl})


def managerActive(request):
    id=request.GET['id']
    status=request.GET['status']
    slot=Slot.objects.get(id=id)
    slot.status=status
    slot.save()
    return redirect("/manSlot")

def manBookking(request):
    uid=request.session['id']
    man=Manager.objects.get(id=uid)
    bok=Booking.objects.filter(slot__amount__man_id=uid).order_by("-id")
    return render(request,"manBookking.html",{"bok":bok})

def manComplete(request):
    uid=request.session['id']
    man=Manager.objects.get(id=uid)
    id=request.GET['id']
    bok=Booking.objects.get(id=id)
    bok.slot.status="Available"
    bok.status="Completed"
    bok.save()
    bok.slot.save()
    return redirect("/manBookking")

def manProfile(request):
    uid=request.session['id']
    user=Manager.objects.get(id=uid)
    cus=user.user

    name=user.name
    email=user.email
    phone=user.phone
    address=user.address
    loction=user.location

    if request.method == "POST":
        name=request.POST['name']
        new_email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        password=request.POST.get('password', None)
        location=request.POST['location']

        existing_user=User.objects.filter(username=new_email).exclude(id=cus.id).first()

        if existing_user:
            messages.error(request, "This email is already registered. Please use a different email.")
            return redirect("/manProfile")
        user.name=name
        user.email=new_email
        user.phone=phone
        user.address=address
        user.location=location
        user.save()

        cus.username =new_email
        if password:
            cus.set_password(password)
        cus.save()
        messages.info(request,"Profile Updated")
        return redirect("/manProfile")

    return render(request,"manProfile.html",{"name":name,"email":email,"phone":phone,"address":address,"location":loction})
    
    return render(request,"manProfile.html")


from ml.predict import predict_occupancy

def userOccupancyPrediction(request):

    prediction = None
    confidence = None
    recommendation = None

    if request.method == "POST":

        data = {

            "Parking_Spot_ID": int(request.POST["parking_spot"]),

            "Vehicle_Type": request.POST["vehicle_type"],

            "User_Type": request.POST["user_type"],

            "Weather_Temperature": float(request.POST["temperature"]),

            "Weather_Precipitation": int(request.POST["precipitation"]),

            "Nearby_Traffic_Level": request.POST["traffic"],

            "Electric_Vehicle": int(request.POST["electric_vehicle"]),

            "Reserved_Status": int(request.POST["reserved"]),

            "Parking_Lot_Section": request.POST["section"],

            "Spot_Size": request.POST["spot_size"],

            "Proximity_To_Exit": float(request.POST["proximity"]),

            "Entry_Time": int(request.POST["entry_time"])

        }

        prediction, confidence, recommendation = predict_occupancy(data)

    return render(

        request,

        "predict_occupancy.html",

        {

            "prediction": prediction,

            "confidence": confidence,

            "recommendation": recommendation

        }

    )