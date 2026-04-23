from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import datetime as dt

import nltk

nltk.download("punkt")
nltk.download("wordnet")


def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


# Create your views here.


def logins(request):
    if request.POST:
        email = request.POST["email"]
        passw = request.POST["password"]
        print(email)
        print(passw)
        user = authenticate(username=email, password=passw)
        print(user)

        if user is not None:
            login(request, user)
            if user.userType == "Admin":
                messages.info(request, "Login Success")
                return redirect("/admhome")
            elif user.userType == "User":
                id = user.id
                email = user.username
                request.session["uid"] = id
                request.session["email"] = email
                messages.info(request, "Login Success")
                return redirect("/user_home")
            elif user.userType == "Advocate":
                id = user.id
                email = user.username
                request.session["aid"] = id
                request.session["email"] = email

                messages.info(request, "Login Success")
                return redirect("/advocatehome")
        else:
            print("Hiii")
            messages.error(request, "Invalid Username/Password")
    return render(request, "login.html")

import random
from django.core.mail import send_mail
from django.conf import settings

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = Login.objects.get(username=email)

            # GENERATE OTP
            otp = random.randint(100000, 999999)

            request.session["reset_email"] = email
            request.session["otp"] = str(otp)

            # SEND EMAIL
            send_mail(
                "Password Reset OTP",
                f"Your OTP is: {otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            messages.success(request, "OTP sent to your email")
            return redirect("/verify_otp/")

        except Login.DoesNotExist:
            messages.error(request, "Email not registered")

    return render(request, "forgot_password.html")

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")

        if entered_otp == session_otp:
            messages.success(request, "OTP Verified Successfully")
            return redirect("/set_new_password")   # ✅ go to new page
        else:
            messages.error(request, "Invalid OTP")

    return render(request, "verify_otp.html")

from django.contrib.auth.hashers import check_password

def set_new_password(request):
    email = request.session.get("reset_email")

    if not email:
        return redirect("/login")

    user = Login.objects.get(username=email)

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # ✅ check match
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("/set_new_password")

        # ✅ check old password reuse
        if check_password(new_password, user.password):
            messages.error(request, "New password cannot be same as old password")
            return redirect("/set_new_password")

        # ✅ save password
        user.set_password(new_password)
        user.viewPass = new_password
        user.save()

        # clear session
        request.session.flush()

        messages.success(request, "Password changed successfully")
        return redirect("/login")

    return render(request, "set_new_password.html")

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime

def Userregister(request):
    current_date = datetime.today().strftime("%Y-%m-%d")

    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        ac_no = request.POST["ac_no"]
        aadhaar = request.POST["aadhaar"]
        password = request.POST["password"]
        image = request.FILES["image"]

        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email Already Exists")
            return redirect("/login")

        else:
            logUser = Login.objects.create_user(
                username=email,
                password=password,
                userType="User",
                viewPass=password,
                is_active=False,
            )

            userReg = UserRegistration.objects.create(
                name=name,
                email=email,
                phone=phone,
                gender=gender,
                address=address,
                Account_no=ac_no,
                aadhaar=aadhaar,
                dob=dob,
                loginid=logUser,
                image=image,
            )

            # SEND EMAIL
            send_mail(
                subject="Registration Successful - Awaiting Admin Approval",
                message=f"""
Hello {name},

Your registration was completed successfully and wait for admin approval.

Login Email: {email}
Password: {password}

Thank you for registering.
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "Registration Completed Successfully and Wait for Admin Approval")
            return redirect("/login")

    return render(request, "userReg.html", {"current_date": current_date})

def show_case_requests(request):
    case_requests = Case_request.objects.all()
    return render(request, 'Admins/show_case_requests.html', {'case_requests': case_requests})


def approve_user(request, id):
    Login.objects.filter(id=id).update(is_active=True)
    messages.success(request, "User Approved")
    return redirect("/admviewusers")


def reject_user(request, id):
    Login.objects.filter(id=id).delete()
    messages.error(request, "User Rejected")
    return redirect("/admviewusers")

    
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def AdvocateReg(request):
    view = Case_Category.objects.all()

    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        password = request.POST["password"]
        district = request.POST["district"]
        education = request.POST["education"]
        category = request.POST["cases"]

        image = request.FILES.get("image")
        files = request.FILES.get("files")

        fs = FileSystemStorage()

        # ✅ SAVE FILES TEMPORARILY
        image_name = fs.save(image.name, image)
        file_name = fs.save(files.name, files)

        # ✅ STORE ONLY FILE PATH (STRING)
        request.session["adv_data"] = {
            "name": name,
            "email": email,
            "phone": phone,
            "dob": dob,
            "gender": gender,
            "address": address,
            "password": password,
            "district": district,
            "education": education,
            "category": category,
            "image": image_name,
            "files": file_name
        }
        messages.info(request, "Please Proceed to Payment to Complete Registration")
        return redirect("Regpay")

    return render(request, "AdvocateReg.html", {"view": view})


from django.conf import settings
import os
from django.core.mail import send_mail
from django.conf import settings
import os

def Regpay(request):
    data = request.session.get("adv_data")

    if not data:
        return redirect("/AdvocateReg")

    if request.method == "POST":

        # CREATE LOGIN
        logUser = Login.objects.create_user(
            username=data["email"],
            password=data["password"],
            userType="Advocate",
            viewPass=data["password"],
            is_active=False,
        )

        Advocate.objects.create(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            gender=data["gender"],
            address=data["address"],
            dob=data["dob"],
            category=data["category"],
            qualification=data["education"],
            district=data["district"],
            loginid=logUser,
            image=data["image"],
            files=data["files"],
            Regfee="Paid"
        )

        # SEND EMAIL
        send_mail(
            subject="Advocate Registration Successful",
            message=f"""
Hello {data['name']},

Your advocate registration has been completed successfully.

Your payment has been received.
Your account is currently under admin verification.

Login Email: {data['email']}

You will be able to login after admin approval.

Thank you.
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[data["email"]],
            fail_silently=False,
        )

        request.session.flush()

        messages.success(
            request,
            "Registration Completed Successfully and Wait for Admin Approval"
        )
        return redirect("/login")

    return render(request, "Regpayment.html")


def admhome(request):
    return render(request, "Admins/index.html")


def advocatehome(request):
    return render(request, "Advocate/index.html")


def userhome(request):
    return render(request, "User/index.html")

def admviewusers(request):
    view = UserRegistration.objects.select_related('loginid').all()
    return render(request, "Admins/users.html", {"view": view})


def admviewadvocate(request):
    view = Advocate.objects.all()
    return render(request, "Admins/advocates.html", {"view": view})


def add_case_category(request):
    if request.POST:
        Category = request.POST.get("Category")
        Decsription = request.POST.get("desc")

        add = Case_Category.objects.create(Category=Category, Description=Decsription)
        add.save()
        messages.info(request, "Category Added Successfully")
    return render(request, "Admins/add_case_category.html")


def addipc_section(request):
    if request.POST:
        ipc = request.POST.get("ipc")
        Decsription = request.POST.get("desc")

        add = IPC_sections.objects.create(IPC=ipc, Description=Decsription)
        add.save()
        messages.info(request, "IPC Sections Added Successfully")
    return render(request, "Admins/addipc_section.html")


def userview_Advocate(request):
    vie = Advocate.objects.filter(loginid__is_active=1)
    print(vie)
    return render(request, "User/advocate_view.html", {"vie": vie})


def user_home(request):
    return render(request, "User/index.html")


def user_add_feed(request):
    id=request.GET['id']
    uid = request.session["uid"]
    ad=Advocate.objects.get(id=id)
    Uid = UserRegistration.objects.get(loginid=uid)
    current_date = datetime.today().strftime("%Y-%m-%d")
    if request.POST:
        sub = request.POST.get("exampleForm")
        feedback = request.POST.get("feedback")

        add = Feedback.objects.create(
            sub=sub, Feedback=feedback,aid=ad ,uid=Uid,date=current_date, Type="User"
        )
        add.save()
        messages.info(request, "Feedback Successfully")
        return redirect('/userhome')
    return render(request, "User/add_feedback.html")


def user_view_ipc(request):
    view = IPC_sections.objects.all()
    return render(request, "User/view_ipc.html", {"view": view})


def user_book_case(request):
    email = request.GET.get("email")
    aid = Advocate.objects.get(email=email)
    uid = request.session["uid"]
    Uid = UserRegistration.objects.get(loginid=uid)
    current_date = datetime.today().strftime("%Y-%m-%d")
    view = Advocate.objects.filter(email=email)

    if request.method == "POST":
        sub = request.POST.get("sub")
        desc = request.POST.get("desc")
        files = request.FILES.getlist("case_files")  # Handling multiple files

        case_request = Case_request.objects.create(
            user=Uid, advocate=aid, sub=sub, date=current_date, desc=desc
        )

        for file in files:
            CaseFile.objects.create(case_request=case_request, file=file)

        messages.info(request, "Request Added Successfully")

    return render(request, "User/case_book.html", {"view": view})


def user_view_request(request):
    uid = request.session["uid"]
    email = request.session["email"]

    Uid = UserRegistration.objects.get(loginid=uid)

    # ACTIVE CASES
    active_cases = Case_request.objects.filter(
        user__email=email
    ).exclude(
        status__in=["Completed", "Cancelled"]
    ).select_related('advocate')

    # COMPLETED CASES
    completed_cases = Case_request.objects.filter(
        user__email=email,
        status="Completed"
    ).select_related('advocate')

    # CANCELLED CASES
    cancelled_cases = Case_request.objects.filter(
        user__email=email,
        status="Cancelled"
    ).select_related('advocate')

    for case in active_cases:
        case.filtered_advocates = Advocate.objects.filter(
            category=case.advocate.category
        ).exclude(id=case.advocate.id)

    return render(request, "User/user_view_request.html", {
        "active_cases": active_cases,
        "completed_cases": completed_cases,
        "cancelled_cases": cancelled_cases,
    })


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings

def cancel_case_request(request):
    rid = request.GET.get("rid")

    case = get_object_or_404(Case_request, id=rid)

    if case.request != "pending":
        messages.error(
            request,
            "Case cannot be cancelled after advocate approval/rejection."
        )
        return redirect("user_view_request")

    case.request = "Cancelled"
    case.status = "Cancelled"
    case.save()

    # ✅ SEND EMAIL TO ADVOCATE
    send_mail(
        subject="Case Cancelled by User",
        message=f"""
Hello {case.advocate.name},

The user has cancelled their case request.

Case Details:
Subject: {case.sub}
User: {case.user.name}
Email: {case.user.email}

This case is no longer active.

Thank you.
        """,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[case.advocate.email],
        fail_silently=False,
    )

    messages.success(request, "Case Cancelled Successfully & Advocate Notified")
    return redirect("user_view_request")

def upload_case_file(request):
    if request.method == "POST" and request.FILES.get("case_file"):
        case_id = request.POST.get("case_id")
        case = get_object_or_404(Case_request, id=case_id)

        # Save file in Case_request model
        case.user_uploaded_file = request.FILES["case_file"]
        case.save()

        # Save file in CaseFile model
        CaseFile.objects.create(case_request=case, file=request.FILES["case_file"])

    return redirect("/user_view_request/")

def change_advocate_request(request):
    if request.method == "POST":
        case_id = request.POST.get("case_id")
        new_advocate_id = request.POST.get("new_advocate_id")

        try:
            case = Case_request.objects.get(id=case_id)
            new_advocate = Advocate.objects.get(id=new_advocate_id)

            # Save the requested advocate instead of changing directly
            case.requested_advocate = new_advocate
            case.request = "Pending Approval"  # Update request status
            case.save()

            messages.success(request, "Advocate change request submitted successfully!")
        except Case_request.DoesNotExist:
            messages.error(request, "Case request not found.")
        except Advocate.DoesNotExist:
            messages.error(request, "Selected advocate not found.")

    return redirect("/user_view_request")


def users_request(request):
    pending_requests = Case_request.objects.filter(request="Pending Approval", requested_advocate__isnull=False)
    approved_requests = Case_request.objects.filter(request="Approved")
    return render(request, "Admins/users_request.html", {
        "pending_requests": pending_requests,
        "approved_requests": approved_requests
    })


def approve_advocate_change(request, case_id):
    try:
        case = Case_request.objects.get(id=case_id)

        if case.requested_advocate:
            case.advocate = case.requested_advocate  # Assign new advocate
            case.requested_advocate = None  # Clear request field
            case.request = "Approved"
            case.save()

            # Update Case_details if exists
            if Case_details.objects.filter(rid=case).exists():
                case_details = Case_details.objects.get(rid=case)
                case_details.advocate = case.advocate
                case_details.save()

            messages.success(request, "Advocate change approved successfully!")
        else:
            messages.error(request, "No advocate change request found.")

    except Case_request.DoesNotExist:
        messages.error(request, "Case request not found.")

    return redirect("/users_request")

def reject_advocate_change(request, case_id):
    try:
        case = Case_request.objects.get(id=case_id)
        case.requested_advocate = None  # Clear request
        case.request = "Rejected"
        case.save()

        messages.success(request, "Advocate change request rejected!")
    except Case_request.DoesNotExist:
        messages.error(request, "Case request not found.")

    return redirect("/users_request")

def adv_view_request(request): 
    uid = request.session["aid"]
    Uid = Advocate.objects.get(loginid=uid)

    view = Case_request.objects.filter(
        request="pending", 
        advocate=Uid.id
    ).prefetch_related('files')

    ap = Case_request.objects.filter(
        request__in=["Approved", "Pending Approval"], 
        advocate=Uid.id
    ).exclude(status__in=["Completed", "Failed"]).prefetch_related('files')

    rj = Case_request.objects.filter(
        request="Rejected", 
        advocate=Uid.id
    )

    completed = Case_request.objects.filter(
        request="Approved",
        status="Completed",
        advocate=Uid.id
    ).prefetch_related('files')

    failed = Case_request.objects.filter(
        request="Approved",
        status="Failed",
        advocate=Uid.id
    ).prefetch_related('files')

    # ✅ NEW
    cancelled = Case_request.objects.filter(
        request="Cancelled",
        advocate=Uid.id
    ).prefetch_related('files')

    return render(request, "Advocate/view_case_request.html", {
        "view": view, 
        "ap": ap, 
        "rj": rj,
        "completed": completed,
        "failed": failed,
        "cancelled": cancelled   # ✅ PASS THIS
    })

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

def approve_case_request(request):
    rid = request.GET.get("id")

    case = Case_request.objects.get(id=rid)

    case.request = "Approved"
    case.save()

    # SEND EMAIL
    send_mail(
        subject="Your Case Request Has Been Approved",
        message=f"""
Hello {case.user.name},

Your case request has been APPROVED by advocate.

Case Subject: {case.sub}

You may now continue further communication with the advocate.

Thank You.
        """,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[case.user.email],
        fail_silently=False,
    )

    messages.success(request, "Request Accepted & Email Sent")
    return redirect("adv_view_request")
def reject_case_request(request):
    rid = request.GET.get("id")

    case = Case_request.objects.get(id=rid)

    case.request = "Rejected"
    case.save()

    # SEND EMAIL
    send_mail(
        subject="Your Case Request Has Been Rejected",
        message=f"""
Hello {case.user.name},

We regret to inform you that your case request has been REJECTED by advocate.

Case Subject: {case.sub}

Please contact support or submit another request if needed.

Thank You.
        """,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[case.user.email],
        fail_silently=False,
    )

    messages.error(request, "Request Rejected & Email Sent")
    return redirect("adv_view_request")


def approve_advocate(request):
    id = request.GET.get("id")
    approve = Login.objects.filter(id=id).update(is_active=1)
    messages.info(request, "Request Accepted")
    return redirect("/admviewadvocate")


def reject_advocate(request):
    id = request.GET.get("id")

    Login.objects.filter(id=id).delete()

    messages.info(request, "Advocate Deleted")
    return redirect("/admviewadvocate")




def advocate_add_feed(request):
    aid = request.session["aid"]
    aaid = Advocate.objects.get(loginid=aid)
    current_date = datetime.today().strftime("%Y-%m-%d")

    if request.POST:
        sub = request.POST.get("exampleForm")
        feedback = request.POST.get("feedback")
        uid = request.POST.get("uid")  # Get selected user from the form

        user_instance = UserRegistration.objects.get(id=uid)  # Fetch user object

        add = Feedback.objects.create(
            sub=sub,
            Feedback=feedback,
            aid=aaid,
            uid=user_instance,  # Link to corresponding user
            date=current_date,
            Type="Advocate",
        )
        add.save()
        messages.info(request, "Feedback Added Successfully")
        return redirect('/advocatehome')

    users = UserRegistration.objects.all()  # Fetch all users for selection
    return render(request, "Advocate/add_feedback.html", {"users": users})


def view_feedback_user(request):
    view=Feedback.objects.filter(Type="User")
    return render(request,'Advocate/view_feedback_user.html',{'view':view})

def adv_view_ipc(request):
    view = IPC_sections.objects.all()
    return render(request, "Advocate/view_ipc.html", {"view": view})


# def adv_view_approved_case(request):
#     current_date = datetime.today().strftime("%Y-%m-%d")
#     print(current_date)
#     aid = request.session["aid"]
#     aaid = Advocate.objects.get(loginid=aid)
#     rid = request.GET.get("id")
#     rrid = Case_request.objects.get(id=rid)
#     uid = request.GET.get("uid")
#     uuid = UserRegistration.objects.get(id=uid)
#     print("userid", uuid.id)
#     view = Case_request.objects.filter(request="Approved", id=rid)

#     if "files" in request.POST:
#         status = request.POST.get("status")
#         date = request.POST.get("date")
#         case = Case_request.objects.filter(id=rid).update(date=date, status=status)
#         return HttpResponse(
#             "<script>alert('Status Updated');window.location='/adv_view_request'</script>"
#         )

#     elif "Describe" in request.POST:
#         desc = request.POST.get("desc")
#         fees = request.POST.get("fees")
#         file = request.FILES["file"]
#         if Case_details.objects.filter(desc=desc, fees=fees).exists():
#             messages.success(request, "Already Exists")
#         else:
#             upload = Case_details.objects.create(
#                 desc=desc,
#                 fees=fees,
#                 rid_id=rrid.id,
#                 file=file,
#                 user_id=uuid.id,
#                 advocate_id=aaid.id,
#                 status="NotPaid",
#             )
#             upload.save()
#             messages.success(request, "Files Uploaded")
#             return HttpResponse(
#                 "<script>alert('File And Fees Uploaded');window.location='/adv_view_request'</script>"
#             )
#         # else:
#         #     messages.info(request, "Please Select Petitions from Case Request")
#     return render(
#         request, "Advocate/cases.html", {"view": view, "current_date": current_date}
#     )

def adv_view_approved_case(request):  
    current_date = datetime.today().strftime("%Y-%m-%d")

    aid = request.session["aid"]
    aaid = Advocate.objects.get(loginid=aid)

    rid = request.GET.get("id")
    rrid = Case_request.objects.get(id=rid)

    uid = request.GET.get("uid")
    uuid = UserRegistration.objects.get(id=uid)

    view = Case_request.objects.filter(request="Approved", id=rid)

    if request.method == "POST":
        status = request.POST.get("status")
        date = request.POST.get("date")
        desc = request.POST.get("desc")
        fees = request.POST.get("fees")
        file = request.FILES.get("file")

        Case_request.objects.filter(id=rid).update(date=date, status=status)

        if status == "Completed":

            if not fees or not file or not desc:
                messages.error(request, "Fees, File and Description required")
                return redirect(request.path + f"?id={rid}&uid={uid}")

            Case_details.objects.create(
                desc=desc,
                fees=fees,
                rid_id=rrid.id,
                file=file,
                user_id=uuid.id,
                advocate_id=aaid.id,
                status="NotPaid",
            )

            messages.success(request, "Case Completed & Details Added")

        else:
            if fees or file or desc:
                messages.error(request, "Add details only when Completed")
                return redirect(request.path + f"?id={rid}&uid={uid}")

            messages.success(request, "Status Updated")

        return redirect("/adv_view_request")

    return render(request, "Advocate/cases.html", {
        "view": view, 
        "current_date": current_date
    })

def view_payment_details(request):
    aid=request.session['aid']
    adv=Advocate.objects.get(loginid=aid)
    data=Case_details.objects.filter(advocate=adv)
    return render(request,'Advocate/view_payment_details.html',{'data':data})


def user_profile(request):
    uid = request.session["uid"]
    view = UserRegistration.objects.filter(loginid=uid)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        password = request.POST.get("password")
        image = request.FILES.get("image")

        if image:
            userid = UserRegistration.objects.get(loginid=uid)
            userid.image = image
            userid.save()

            up = UserRegistration.objects.filter(loginid=uid).update(
                name=name, email=email, phone=phone, address=address
            )

            pas_up = Login.objects.get(id=uid)
            pas_up.set_password(password)
            pas_up.viewPass = password
            pas_up.save()

            HttpResponse(
                "<script>alert('profile updated');window.location='/user_profile'</script>"
            )

        else:
            up = UserRegistration.objects.filter(loginid=uid).update(
                name=name, email=email, phone=phone, address=address
            )

            pas_up = Login.objects.get(id=uid)
            pas_up.set_password(password)
            pas_up.viewPass = password
            pas_up.save()

            HttpResponse(
                "<script>alert('profile updated');window.location='/user_profile'</script>"
            )

    return render(request, "User/profile.html", {"view": view})


def user_case_files(request):
    uid = request.session["uid"]
    Uid = UserRegistration.objects.get(loginid=uid)

    rid = request.GET.get("rid")   # ✅ get case id from URL

    view = Case_details.objects.filter(user=Uid, rid_id=rid)

    return render(request, "User/user_case_files.html", {"view": view})

def chat(request):
    import chatgui

    return redirect("/")


def payment_page(request):
    amut = request.GET.get("amt")
    cid = request.GET.get("cid")

    if request.POST:
        up = Case_details.objects.filter(id=cid, status="NotPaid").update(
            status="Paid"
        )
        return redirect("/Applied_success")
    return render(request, "User/payment_page.html", {"amount": amut})

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from django.shortcuts import get_object_or_404
from .models import Case_details

def download_invoice(request, cid):
    case = get_object_or_404(Case_details, id=cid)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{cid}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # TITLE
    elements.append(Paragraph("INVOICE", styles['Title']))
    elements.append(Spacer(1, 20))

    # USER DETAILS
    elements.append(Paragraph(f"<b>Customer:</b> {case.user.name}", styles['Normal']))
    elements.append(Paragraph(f"<b>Email:</b> {case.user.email}", styles['Normal']))
    elements.append(Spacer(1, 10))

    # CASE DETAILS
    elements.append(Paragraph(f"<b>Case:</b> {case.rid.sub}", styles['Normal']))
    elements.append(Paragraph(f"<b>Advocate:</b> {case.advocate.name}", styles['Normal']))
    elements.append(Spacer(1, 10))

    # PAYMENT DETAILS
    elements.append(Paragraph(f"<b>Amount Paid:</b> ₹{case.fees}", styles['Normal']))
    elements.append(Paragraph(f"<b>Status:</b> {case.status}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # FOOTER
    elements.append(Paragraph("Thank you for your payment!", styles['Normal']))

    doc.build(elements)

    return response


def payment_view(request):
    uid = request.session["uid"]
    view = Case_details.objects.filter(user=uid)
    return render(request, "User/payment_details.html", {"view": view})


def Applied_success(request):
    return render(request, "User/Applied_success.html")


def userchat(request):
    uid = request.session["uid"]
    Uid = UserRegistration.objects.get(loginid=uid)
    # Artists
    name = ""
    pimage = ""
    aid = request.GET.get("aid")
    email = request.GET.get("email")
    artistData = Advocate.objects.filter(email=email)
    getChatData = Chat.objects.filter(Q(uid=Uid) & Q(Advo__email=email))
    print("getChatData ", getChatData)
    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%H:%M")
    userid = UserRegistration.objects.get(loginid__id=uid)
    if aid:
        advocate_id = Advocate.objects.get(email=email)
        name = advocate_id.name
        pimage = advocate_id.image
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            uid=userid,
            message=message,
            Advo=advocate_id,
            time=formatted_time,
            utype="USER",
        )
        sendMsg.save()
    return render(
        request,
        "User/chat.html",
        {
            "artistData": artistData,
            "getChatData": getChatData,
            "artistid": name,
            "image": pimage,
        },
    )


def reply(request):
    email = request.session["email"]
    uid = request.session["aid"]
    Aid = Advocate.objects.get(loginid=uid)
    print(uid)
    name = ""
    pimage = ""
    userData = UserRegistration.objects.filter(loginid__is_active=1)
    id = request.GET.get("uid")
    uemail = request.GET.get("email")
    print("User Details :", id)
    UserId = UserRegistration.objects.get(email=uemail)
    getChatData = Chat.objects.filter(Q(Advo__loginid=uid) & Q(uid__email=uemail))
    print("HELLO", getChatData)
    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%H:%M")
    advo_id = Advocate.objects.get(email=email)
    advo = advo_id.id
    if id:
        userid = UserRegistration.objects.get(loginid=id)
        name = userid.name
        pimage = userid.image
        print("userid : ", userid)
        print("name : ", name)
        print("image : ", pimage)
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            uid=userid,
            message=message,
            Advo_id=advo,
            time=formatted_time,
            utype="ADVOCATE",
        )
        sendMsg.save()
    return render(
        request,
        "Advocate/chat.html",
        {
            "userData": userData,
            "getChatData": getChatData,
            "userid": name,
            "image": pimage,
        },
    )


def admviewfeedback(request):
    feedbacks = Feedback.objects.all()
    ratings = Rating.objects.all()
    return render(request, "Admins/view_feedback.html", {"feedbacks": feedbacks, "ratings": ratings})

def udp(request):
    dele = Login.objects.filter(id=9).update(is_active=1)
    return HttpResponse("deleted")


def delete_feedback(request):
    fid = request.GET.get("fid")
    if fid:
        dele = Feedback.objects.filter(id=fid).delete()
        return HttpResponse(
            "<script>alert('Feedback Deleted');window.location='/admviewfeedback';</script>"
        )

def delete_rating(request):
    fid = request.GET.get("fid")
    if fid:
        dele = Rating.objects.filter(id=fid).delete()
        return HttpResponse(
            "<script>alert('Feedback Deleted');window.location='/admviewfeedback';</script>"
        )



def add_rating(request):
    uid = request.session.get("uid")
    Uid = UserRegistration.objects.get(loginid=uid)
    aid = request.GET.get("aid")
    email = request.GET.get("email")
    Aid = Advocate.objects.get(loginid=aid)
    rid = request.GET.get("rid")
    Rid = Case_request.objects.get(id=rid)

    if request.method == "POST":
        rating = request.POST.get("rating")
        text = request.POST.get("text")
        # if Rating.objects.filter(uid=Uid).exists():
        #     return HttpResponse(
        #         "<script>alert('Rating Already Added');window.location='/user_view_request';</script>"
        #     )
        # else:
        add = Rating.objects.create(aid=Aid, rid=Rid,text=text, rating=rating, uid=Uid)
        add.save()
        ratings = Rating.objects.filter(aid=Aid)
        total_ratings = ratings.count()
        if total_ratings > 0:
            total_sum = sum(r.rating for r in ratings)
            avg_rating = total_sum / total_ratings
            print("totalSum: ", total_sum)
            print("Avg.rating: ", avg_rating)
            update = Advocate.objects.filter(email=email).update(
                advo_rating=avg_rating
            )
            return HttpResponse(
                "<script>alert('Rating Added');window.location='/user_view_request';</script>"
            )

    return render(request, "User/add_rating.html")





def view_feedback_advocate(request):
    view=Feedback.objects.filter(Type="Advocate")
    return render(request,'User/view_feedback_advocate.html',{'view':view})

###############newly added

def view_ratings(request):
    aid = request.session.get("aid")  
    advocate = Advocate.objects.get(loginid=aid)
    ratings = Rating.objects.filter(aid=advocate).order_by('-date')  

    return render(request, "Advocate/view_ratings.html", {"ratings": ratings})
from django.db.models import Count
from django.shortcuts import render
from .models import *

def admin_dashboard(request):

    total_users = UserRegistration.objects.count()
    total_advocates = Advocate.objects.count()
    total_cases = Case_request.objects.count()
    total_ipc = IPC_sections.objects.count()

    # 🔷 STATUS COUNTS
    ongoing = Case_request.objects.filter(status="Ongoing").count()
    completed = Case_request.objects.filter(status="Completed").count()
    not_updated = Case_request.objects.filter(status="Not_Updated").count()
    failed = Case_request.objects.filter(status="Failed").count()
    processing = Case_request.objects.filter(status="Start Processing").count()

    # 🔷 CASES PER ADVOCATE (BAR CHART)
    advocate_data = Case_request.objects.values('advocate__name').annotate(total=Count('id'))

    advocate_names = [i['advocate__name'] for i in advocate_data]
    advocate_counts = [i['total'] for i in advocate_data]

    context = {
        "total_users": total_users,
        "total_advocates": total_advocates,
        "total_cases": total_cases,
        "total_ipc": total_ipc,

        "ongoing": ongoing,
        "completed": completed,
        "not_updated": not_updated,
        "failed": failed,
        "processing": processing,

        "advocate_names": advocate_names,
        "advocate_counts": advocate_counts,
    }

    return render(request, "Admins/admin_dashboard.html", context)


def adv_profile(request):
    aid = request.session.get("aid")
    adv = Advocate.objects.get(loginid=aid)
    return render(request, "Advocate/advocate_profile.html", {"adv": adv})

import re
from django.contrib import messages

def edit_adv_profile(request):
    aid = request.session.get("aid")
    adv = Advocate.objects.get(loginid=aid)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        district = request.POST.get("district")

        image = request.FILES.get("image")

        # ✅ PHONE VALIDATION
        if not re.match(r'^[6789][0-9]{9}$', phone):
            messages.error(request, "Invalid phone number")
            return redirect(request.path)

        adv.name = name
        adv.phone = phone
        adv.address = address
        adv.district = district

        if image:
            adv.image = image

        adv.save()

        messages.success(request, "Profile Updated Successfully")
        return redirect("/adv_profile")

    return render(request, "Advocate/edit_adv_profile.html", {"adv": adv})