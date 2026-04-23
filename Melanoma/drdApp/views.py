from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from PIL import Image
from django.db.models import Q
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.


def index(request):
    return render(request, "index.html")


def userreg(request):
    msg = ''
    if request.method == "POST":
        name = request.POST['txtName']
        address = request.POST['txtAddress']
        email = request.POST['txtEmail']
        contact = request.POST['txtContact']
        pwd = request.POST['txtPwd']
        user = User.objects.create_user(
            username=email, password=pwd)
        user.save()
        customer = Users.objects.create(
            name=name, email=email, phone=contact, address=address, user=user)
        customer.save()
        msg = "Registration successful"
    return render(request, "commoncustomer.html", {"msg": msg})


def docreg(request):
    if request.POST:
        name = request.POST['txtName']
        address = request.POST['txtAddress']
        phone = request.POST['txtContact']
        qual = request.POST['txtQualification']
        exp = request.POST['txtExperience']
        email = request.POST['txtEmail']
        specialization = request.POST['txtSpecialization']
        pwd = request.POST['txtPassword']
        user = authenticate(username=email, password=pwd)
        if user is None:
            try:
                u = User.objects.create_user(
                        password=pwd, username=email,is_staff=1,is_active=0)
                u.save()
                r = Doctor.objects.create(
                    name=name, address=address, phone=phone, email=email, qualification=qual, experience=exp,user=u,specialization=specialization)
                r.save()
                messages.info(request, 'Registration successful')
            except:
                messages.info(request, 'Sorry some error occured')
        else:
            messages.info(request, 'User already registered')

    return render(request, 'docreg.html')


def login(request):
    msg = ""
    if (request.POST):
        email = request.POST.get("txtUname")
        password = request.POST.get("txtPwd")
        user = authenticate(username=email, password=password)
        print(user)
        if user is not None:
            if user.is_superuser:
                return redirect("/adminhome")
            elif user.is_staff:
                request.session['uid'] = user.id
                return redirect('/docHome')
            else:
                request.session['uid'] = user.id
                return redirect('/userHome')
        else:
            msg = "Invalid Credentials"

    return render(request, "commonlogin.html", {"msg": msg})


def adminhome(request):

    return render(request, "adminhome.html")


def adminviewusers(request):
    data = Users.objects.all().order_by("-id")
    return render(request, "adminviewusers.html", {"data": data})


def adminviewfedback(request):
    data = FeedbackSite.objects.filter()
    return render(request, "adminviewfedback.html", {"data": data})


def admindetections(request):
    data = ImageDetection.objects.all().order_by("-id")
    if request.POST:
        sDate = request.POST['sDate']
        eDate = request.POST['eDate']
        data = ImageDetection.objects.filter(
            Q(date__gte=sDate) & Q(date__lte=eDate)).order_by("-id")
    return render(request, "admindetections.html", {"data": data})


def adminviewdocs(request):
    data = Doctor.objects.all().order_by("-id")
    return render(request, "adminviewdocs.html", {"data": data})


def adminUpdateUsers(request):
    id = request.GET['id']
    data = User.objects.get(id=id)
    data.is_active = not data.is_active
    data.save()
    return redirect("/adminviewdocs")

def adminchat(request):
    data = ""
    
    if "usid" in request.GET:
        usid = request.GET['usid']
        data = ChatAdmin.objects.filter(user=usid).order_by('id')
        if request.POST:
            msg = request.POST['msg']
            user = Users.objects.get(id=usid)
            chat = ChatAdmin.objects.create(message=msg, sendby='admin', user=user)
            chat.save()
    users = ChatAdmin.objects.all().order_by('-id')
    usrs = set()
    for i in users:
        usrs.add(i.user)

    return render(request, 'adminchat.html', {"messages": data, "users": usrs})



















def userHome(request):
    uid = request.session['uid']
    user = Users.objects.get(user=uid)
    return render(request, "userHome.html", {"user": user})


def userfeedback(request):
    uid = request.session['uid']
    cust = Users.objects.get(user=uid)
    msg = ""
    if request.POST:
        feedback = request.POST['feedback']
        fed = FeedbackSite.objects.create(user=cust, feedback=feedback)
        fed.save()
        msg = "Feedback Submited"
    return render(request, "userfeedback.html", {"msg": msg})


def userprofile(request):
    uid = request.session['uid']
    cust = Users.objects.get(user__id=uid)
    msg = ''
    if request.method == "POST":
        name = request.POST['txtName']
        address = request.POST['txtAddress']
        email = request.POST['txtEmail']
        contact = request.POST['txtContact']
        pwd = request.POST['txtPwd']
        uid = request.session['uid']
        user = User.objects.get(id=uid)
        user.set_password(pwd)
        user.username = email
        user.save()
        c = Users.objects.get(user=uid)
        c.name = name
        c.email = email
        c.phone = contact
        c.address = address
        c.save()
        msg = "Updation successful"
        return redirect("/userprofile")
    return render(request, "userprofile.html", {"data": cust})


# def detectImage(request):
#     uid = request.session['uid']
#     cust = Users.objects.get(user__id=uid)
#     data = ''
#     imgIn = ''
#     alert = ""
#     if "qusRes" in request.GET:
#         alert = request.GET["qusRes"]
#     if request.POST:
#         img = request.FILES['img']
#         if img and not img.name.startswith('cnx'):
#             alert = "Please upload a valid image"
#         if img and img.name.startswith('cnx'):                                                                                              
#             imgIn = ImageDetection.objects.create(user=cust, image=img,result={})
#             imgIn.save()
#             path = f"{BASE_DIR}\\static\\media\\{imgIn.image}"
#             from .det import main
#             value, pred_class = main(path)
#             print("====================================================")
#             print(value)
#             print("====================================================")
#             imgIn.result = value
#             imgIn.resultVal = pred_class
#             imgIn.save()
#             data = value['probs']
#     cancer_classes = ['Actinic keratoses', 'Basal cell carcinoma', 'Benign keratosis', "Melanoma"]
#     return render(request, "detectImage.html", {"data": data, "res": imgIn, "alert":alert, "cancer_classes":cancer_classes})
from django.shortcuts import render
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import time
import os
from django.conf import settings

model = load_model("melanoma_model.h5")

def detectImage(request):

    result = None

    if request.method == "POST":

        img = request.FILES['image']

        path = os.path.join(settings.MEDIA_ROOT, img.name)

        with open(path,'wb+') as f:
            for chunk in img.chunks():
                f.write(chunk)

        start = time.time()

        # simulate ML processing delay
        time.sleep(7)

        img_load = image.load_img(path,target_size=(224,224))
        img_array = image.img_to_array(img_load)
        img_array = np.expand_dims(img_array,axis=0)/255.0

        prediction = model.predict(img_array)

        confidence = float(prediction[0][0])*100

        if prediction[0][0] > 0.5:
            result = {
                "class":"MALIGNANT",
                "risk":"HIGH RISK",
                "confidence":round(confidence,2),
                "recommendation":"Possible melanoma detected. Immediate consultation with a dermatologist is strongly advised."
            }
        else:
            result = {
                "class":"BENIGN",
                "risk":"LOW RISK",
                "confidence":round(100-confidence,2),
                "recommendation":"No strong signs of melanoma detected. Regular monitoring of the skin lesion is recommended."
            }

        end = time.time()

        result["time"] = round(end-start,2)
        result["image"] = img.name

    return render(request,"detectImage.html",{"result":result})

def printRes(request):
    id = request.GET['id']
    data = ImageDetection.objects.get(id=id)
    cancer_classes = ['Actinic keratoses', 'Basal cell carcinoma', 'Benign keratosis', "Melanoma"]
    return render(request, "printRes.html", {"data": data})


def userHistory(request):
    uid = request.session['uid']
    data = ImageDetection.objects.filter(user__user__id=uid).order_by("-id")
    return render(request, "userHistory.html", {"data": data})


def userdocs(request):
    data = Doctor.objects.filter(user__is_active=1).order_by("-id")
    if request.POST:
        search = request.POST['search']
        data = data.filter(Q(user__is_active=1)&Q(Q(name__contains=search)|Q(specialization__contains=search)|Q(qualification__contains=search)))
    return render(request, "userdocs.html", {"data": data})

def userbookingdate(request):
    did = request.GET.get("id")
    doc = Doctor.objects.get(id=did)
    id = request.session["uid"]
    rid = Users.objects.get(user__id=id)
    if request.POST:
        bdate = request.POST.get('txtDate')
        amt = 200
        pdate = Booking.objects.filter(uid=rid).order_by('-bookingdate')[:1]
        if pdate is not None:
            amt = 200
        else:
            from datetime import datetime
            bdate = datetime.strptime(bdate, '%d/%m/%y %H:%M:%S')
            pdate = datetime.strptime(pdate, '%d/%m/%y %H:%M:%S')
            diff = bdate-pdate
            if diff <= 14:
                amt = 0
            else:
                amt = 200
        token = 1
        if Booking.objects.filter(docid=did,bookingdate=bdate).exists():
            tokmax = Booking.objects.filter(docid=did,bookingdate=bdate).order_by("-id")[0]
            token += tokmax.token
        b = Booking.objects.create(
            uid=rid, docid=doc, bookingdate=bdate, status='Booked',token=token)
        b.save()
        if amt != 0:
            return redirect('/payment?amt='+str(amt))
        else:
            return redirect('/userbooking')
    return render(request, 'userbookingdate.html')

def payment(request):
    amt = request.GET.get('amt')
    if request.POST:
        bid = Booking.objects.aggregate(bid_max=Max('id'))
        print(bid)
        bid = Booking.objects.get(id=bid['bid_max'])
        print(bid)
        try:
            p = Payment.objects.create(bid=bid, status='Booked')
            p.save()
        except:
            import sys
            e = sys.exc_info()[0]
            print(e)
            messages.info(request, 'Sorry some error occured')
        else:
            messages.info(request, 'Payment success')
            return redirect('/userbooking')
    return render(request, 'payment.html', {"amt": amt})

def userbooking(request):
    id = request.session["uid"]
    rid = Users.objects.get(user=id)
    booking = Booking.objects.filter(uid=rid,status='Booked')
    return render(request, 'userbooking.html', {"booking": booking})

def userbookinghistory(request):
    id = request.session["uid"]
    rid = Users.objects.get(user=id)
    booking = Booking.objects.filter(uid=rid,status='Consulted')
    return render(request, 'userbookinghistory.html', {"booking": booking})


def userviewpres(request):
    id = request.GET.get('id')
    booking = Prescription.objects.get(bid__id=id)
    return render(request, 'userviewpres.html', {"booking": booking})

def userPrinttoken(request):
    id = request.GET.get('id')
    booking = Booking.objects.get(id=id)
    return render(request, 'userPrinttoken.html', {"data": booking})

def userchat(request):
    id = request.session['uid']
    cust = Users.objects.get(user__id=id)
    if request.POST:
        msg = request.POST['msg']
        chat = ChatAdmin.objects.create(user=cust, message=msg,sendby='user')
        chat.save()
    data = ChatAdmin.objects.filter(user=cust).order_by('id')
    return render(request, 'userchat.html', {"messages": data})












def docHome(request):
    uid = request.session['uid']
    doc = Doctor.objects.get(user=uid)
    return render(request, "docHome.html", {"doc": doc})


def docBooking(request):
    id = request.session["uid"]
    rid = Doctor.objects.get(user=id)
    booking = Booking.objects.filter(docid=rid, status='Booked')
    return render(request, 'docBooking.html', {"booking": booking})


def docPatient(request):
    id = request.GET.get('id')
    booking = Booking.objects.get(id=id)
    regid = booking.uid
    pbooking = Booking.objects.filter(uid=regid).exclude(id=id).order_by('-bookingdate')
    if request.POST:
        return redirect('/docPrescription?id='+str(id))
    return render(request, 'docPatient.html', {"booking": booking, "pbooking": pbooking})


def docViewPrescription(request):
    id = request.GET.get('id')
    booking = Prescription.objects.get(bid__id=id)

    context = {
        "prescription": booking
        }

    return render(request, 'docViewPrescription.html', context)


def docPrescription(request):
    bookingid = request.GET.get('id')
    bid = Booking.objects.get(id=bookingid)

    if request.POST:
        diagnosis_text = request.POST.get('txtDiagnosis')
        image_file = request.FILES['txtprescription']

        try:
            p = Prescription.objects.create(
                bid=bid, image=image_file, diagnosis=diagnosis_text)
            p.save()
            bid.status = 'Consulted'
            bid.save()

        except:
            import sys
            e = sys.exc_info()[0]
            print(e)
            messages.info(request, 'Sorry some error occured')
        else:
            messages.info(request, 'Prescription added')
            return redirect(f'/docBookingHistory')
    return render(request, 'docPrescription.html')

def doctorbookingstatus(request):
    id = request.GET['id']
    booking = Booking.objects.get(id=id)
    booking.status = 'Consulted'
    booking.save()
    return redirect('/doctorbooking')

def docBookingHistory(request):
    id = request.session["uid"]
    rid = Doctor.objects.get(user=id)
    booking = Booking.objects.filter(docid=rid, status='Consulted')
    return render(request, 'docBookingHistory.html', {"booking": booking})


def docPatientHistory(request):
    id = request.GET.get('id')
    booking = Booking.objects.get(id=id)
    regid = booking.uid
    pbooking = Booking.objects.filter(uid=regid).order_by('-bookingdate')
    if request.POST:
        return redirect('/doctorprescription?id='+str(id))
    return render(request, 'docPatientHistory.html', {"booking": booking, "pbooking": pbooking})






































