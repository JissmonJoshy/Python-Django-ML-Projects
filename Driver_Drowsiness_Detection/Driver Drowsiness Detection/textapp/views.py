# import email
from http.client import HTTPResponse
from django.shortcuts import render,HttpResponse,HttpResponseRedirect

from .models import *
from django.contrib import messages
from django.db.models import Max, Min,Count,Sum,Avg




def udp(request):
    # email="admin@gmail.com"
    # password="admin"

    # s=Login.objects.create(username=email,password=password,usertype='admin',status='requested')
    # s.save()
    # messages.info(request,"already added")
    return render(request,"common/driverreg.html")







def index(request):
    return render(request,"common/index.html")

def adminhome(request):
    return render(request,"admin/index.html")

def userhome(request):
    return render(request,"user/index.html")

def driverhome(request):
    return render(request,"driver/index.html")
from django.shortcuts import render
from django.contrib import messages
from .models import Driver, Login
from django.db import IntegrityError

def driverreg(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # 🔹 Check empty fields
        if not name or not address or not contact or not email or not password:
            messages.error(request, "All fields are required!")
            return render(request, "common/driverreg.html")

        # 🔹 Check duplicate email
        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, "common/driverreg.html")

        try:
            driver = Driver.objects.create(
                dname=name,
                daddress=address,
                dcontact=contact,
                demail=email,
                dpassword=password,
                status="requested"
            )

            Login.objects.create(
                username=email,
                password=password,
                usertype="driver",
                status="requested",
                driverid=driver
            )

            messages.success(request, "Registration Successful! Wait for approval.")
            return HttpResponseRedirect("/login")

        except IntegrityError:
            messages.error(request, "Something went wrong. Try again.")

    return render(request, "common/driverreg.html")


from .models import User, Login

def userreg(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # 🔹 Check if email already exists in Login table
        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, "common/userreg.html")

        # 🔹 Create User
        user = User.objects.create(
            uname=name,
            uaddress=address,
            ucontact=contact,
            uemail=email,
            upassword=password
        )

        # 🔹 Create Login
        Login.objects.create(
            username=email,
            password=password,
            usertype="user",
            status="active"
        )

        messages.success(request, "User Registered Successfully!")
        return render(request, "common/login.html")

    return render(request, "common/userreg.html")




from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Login, User, Driver

def logins(request):
    if request.method == "POST":
        name = request.POST.get("username")
        password = request.POST.get("password")

        try:
            login_obj = Login.objects.filter(username=name, password=password).first()
            if not login_obj:
                messages.error(request, "Invalid Username or Password!")
                return render(request, "common/login.html")

            # ADMIN LOGIN
            if login_obj.usertype == 'admin':
                return render(request, "common/login.html", {
                    "msg": "Login Successful",
                    "redirect": "/adminhome"
                })

            # USER LOGIN
            elif login_obj.usertype == 'user':
                user = User.objects.get(uemail=name)
                request.session['uid'] = user.id

                return render(request, "common/login.html", {
                    "msg": "Login Successful",
                    "redirect": "/userhome"
                })

            # DRIVER LOGIN
            elif login_obj.usertype == 'driver':
                driver = Driver.objects.get(demail=name)

                if driver.status.lower() == "approved":
                    request.session['did'] = driver.id
                    return render(request, "common/login.html", {
                        "msg": "Login Successful",
                        "redirect": "/driverhome"
                    })
                else:
                    return render(request, "common/login.html", {
                        "msg": "Your account is not approved yet!"
                    })

        except Login.DoesNotExist:
            return render(request, "common/login.html", {
                "msg": "Invalid Username or Password!"
            })

    return render(request, "common/login.html")



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Driver, Login

def adminviewdriver(request):

    # ✅ APPROVE
    if request.GET.get("approve_id"):
        id = request.GET.get("approve_id")

        driver = Driver.objects.get(id=id)
        driver.status = "approved"
        driver.save()

        Login.objects.filter(driverid=driver).update(status="approved")

        messages.success(request, "Driver Approved Successfully!")
        return redirect("/adminviewdriver")

    # ✅ REJECT (Delete from both tables)
    if request.GET.get("reject_id"):
        id = request.GET.get("reject_id")

        driver = Driver.objects.get(id=id)

        # Delete login first
        Login.objects.filter(driverid=driver).delete()

        # Delete driver
        driver.delete()

        messages.error(request, "Driver Rejected and Deleted!")
        return redirect("/adminviewdriver")

    # 🔹 Separate Querysets
    requested = Driver.objects.filter(status="requested")
    approved = Driver.objects.filter(status="approved")

    return render(request, "admin/viewdriver.html", {
        "requested": requested,
        "approved": approved
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Login

def adminviewuser(request):

    # ✅ Reject User
    if request.GET.get("reject_id"):
        id = request.GET.get("reject_id")

        try:
            user = User.objects.get(id=id)

            # delete from Login table
            Login.objects.filter(username=user.uemail).delete()

            # delete from User table
            user.delete()

            messages.success(request, "User Rejected and Deleted Successfully!")

        except User.DoesNotExist:
            messages.error(request, "User not found!")

        return redirect("/adminviewuser")

    # show all users
    users = User.objects.all()
    return render(request, "admin/viewuser.html", {"data": users})


import datetime

def userviewdriver(request):  
    drivers = Driver.objects.all()
    uid = request.session['uid']

    if request.GET:
        id = request.GET.get("id")
        driverdetails = Driver.objects.get(id=id)
        userdetails = User.objects.get(id=uid)

        date = datetime.datetime.now()

        Booking.objects.create(
            uid=userdetails,
            did=driverdetails,
            date=date,
            status='requested'
        )

        messages.success(request, "Driver booking request sent successfully!")

        return HttpResponseRedirect("/userviewdriver")

    return render(request, "user/viewdriver.html", {"data": drivers})

from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from .models import Booking

from .models import Feedback

def userviewbooking(request):  
    uid = request.session['uid']

    if request.GET.get("cancel_id"):
        cancel_id = request.GET.get("cancel_id")
        booking = Booking.objects.get(id=cancel_id)
        booking.status = "cancelled"
        booking.save()
        messages.success(request, "Booking cancelled successfully!")
        return redirect("/userviewbooking")

    bookings = Booking.objects.filter(uid=uid)

    # Attach feedback info
    for b in bookings:
        b.feedback_given = Feedback.objects.filter(booking=b).exists()

    return render(request, "user/viewbooking.html", {"data": bookings})

def userpayment(request):
    booking_id = request.GET.get("id")
    booking = Booking.objects.get(id=booking_id)

    if request.method == "POST":
        booking.status = "Paid"
        booking.save()
        messages.success(request, "Payment Successful!")
        return redirect("/userviewbooking")

    return render(request, "user/payment.html", {"booking": booking})

def driverviewbooking(request):
    did = request.session['did']

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        charge = request.POST.get("charge")

        booking = Booking.objects.get(id=booking_id)
        booking.status = "approved"
        booking.charge = charge
        booking.save()

        messages.success(request, "Booking Approved Successfully!")
        return redirect("/driverviewbooking")

    bookings = Booking.objects.filter(did=did)
    return render(request, "driver/viewbooking.html", {"data": bookings})

def userfeedback(request):
    booking_id = request.GET.get("id")
    booking = get_object_or_404(Booking, id=booking_id)

    # Check if feedback already exists
    already_given = Feedback.objects.filter(booking=booking).exists()

    if already_given:
        messages.info(request, "Feedback already submitted!")
        return redirect("/userviewbooking")

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Feedback.objects.create(
            booking=booking,
            user=booking.uid,
            driver=booking.did,
            rating=rating,
            comment=comment
        )

        messages.success(request, "Feedback Submitted Successfully!")
        return redirect("/userviewbooking")

    return render(request, "user/feedback.html", {"booking": booking})


from .models import Feedback

def driverviewfeedback(request):
    did = request.session['did']

    feedbacks = Feedback.objects.filter(driver_id=did).order_by('-date')

    return render(request, "driver/viewfeedback.html", {"data": feedbacks})

def ddetection(request):
    from textapp import cd
    return HttpResponseRedirect("/userhome")




def driverdetection(request):
    from textapp import cd
    return HttpResponseRedirect("/driverhome")





# def addstudent(request):
#     if request.POST:
#         fname=request.POST.get("fname")
#         age=request.POST.get("age")
#         gender=request.POST.get("gender")
#         profile=request.FILES.get("img")
#         s=Student.objects.create(fname=fname,age=age,gender=gender,profile=profile)
#         s.save()
#         messages.info(request,"already added")
#     return render(request,"students.html")

# from django.db import connection

# from django.db.models import Q
# def viewstudent(request):
#     s=Student.objects.all()
#     print(s)
#     for i in s:
#         print(i.fname)
#     print(connection.queries)
#     t=Student.objects.get(id=2)
#     u=t
#     print(t)
#     print(t.fname)

#     t=Student.objects.filter(id=2,fname='manu')
#     print(t)
#     # print(t.fname)
#     for i in t:
#         print(i.fname)

#     t=Student.objects.filter(Q(id=2)| Q(fname='manu'))
#     print("*"*100)
#     print(t)
#     for i in t:
#         print(i.fname)
#     print("*"*100)

#     return render(request,"students.html",{'s':s,'t':t,'u':u})



# def updates(request):
#     s=Student.objects.get(id=2).update(fname='binimol')
#     s.save()
#     s=Student.objects.filter(fname='arjun').update(fname='binimol')
#     s.save()
#     return HttpResponse("hello")




# def deletes(request):
#     s=Student.objects.get(id=2).delete()
    
#     s=Student.objects.filter(fname='arjun').delete()
    
#     ##########    OR  ############
#     s=Student.objects.filter(fname='anu')
#     s.delete()
#     return HttpResponse("hello")


# def orderbyquery(request):
#     s=Student.objects.filter(fname='binimol').order_by('id')  ## Assending Order
#     s=Student.objects.filter(fname='binimol').order_by('_id')# desending order
#     return HttpResponse("hello")







# def marks(request):
#     # id=request.session['id']
#     id=1
#     if request.POST:
#         mark1=request.POST.get("mark1")
#         mark2=request.POST.get("mark2")
#         mark3=request.POST.get("mark3")
#         mark4=request.POST.get("mark4")
#         id=1
#         apl=Student.objects.get(id=1)
#         s=Mark.objects.create(mark1=mark1,mark2=mark2,mark3=mark3,mark4=mark4,studid=apl)
#         s.save()
#     return render(request,"mark.html")


# # def viewmark(request):
# #     s=Mark.objects.all()
# #     return render(request,"mark.html",{"mark":s})


# from django.db.models import Max, Min,Count,Sum,Avg


# def viewmark(request):
#     s=Mark.objects.aggregate(Min('mark1'))
#     print(s)
#     # print(mark)
#     return render(request,"mark.html",{"mark":s})

# # from django.contrib.auth.models import User



# # def adduser(request):
# #     # id=request.session['id']
# #     u=User.objects.create_user(first_name='jk',last_name='lm',username='dsdsds')
# #     u.save()
# #     # return render(request,"mark.html")
# #     return HttpResponse("hello")

# # from django.contrib.auth.models import authenticate,logout



# # def checkuser(request):
# #     # id=request.session['id']
# #     u=authenticate(username='hello',password='hjk')
# #     if u is not None:
# #         print("dkshdfsfshjf")
# #     else:
# #         print("jkashdajkh")
# #     # return render(request,"mark.html")
# #     return HttpResponse("hello")





# #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# # from .forms import studreg
# # def reg(request):
# #     if request.POST:
# #         fm=studreg(request.POST)
# #         if fm.is_valid():
# #             fm.save()
# #     else:
# #         fm=studreg()
# #     return render(request,"hello.html",{"fm":fm})

from django.http import HttpResponse
import threading

def start_drowsiness(request):
    from .utils.drowsiness import start_detection
    thread = threading.Thread(target=start_detection)
    thread.daemon = True
    thread.start()
    return HttpResponse("Drowsiness Detection Started")