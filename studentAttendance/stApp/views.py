from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
import pickle
import numpy as np
import sklearn
from .models import *
# Create your views here.


def index(request):
    return render(request, "index.html")


def login(request):
    msg = ""
    if (request.POST):
        email = request.POST.get("uName")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        print(user)
        if user is not None:
            if user.is_superuser:
                return redirect("/adminhome")
            elif user.user_type == 'Teacher':
                request.session['uid'] = user.id
                return redirect('/teacherhome')
            elif user.user_type == 'Student':
                request.session['uid'] = user.id
                return redirect('/studenthome')
            elif user.user_type == 'Parent':
                request.session['uid'] = user.id
                return redirect('/parenthome')
        else:
            msg = "Invalid Credentials"

    return render(request, "login.html", {"msg": msg})


# def MarkAttendance(request):
#     from stApp import facetraining, final
#     data = Student.objects.values('name')
#     print(data)
#     res = final.fun2(data)
#     print(res)
#     if res != 'unknown':
#         std = Student.objects.get(id=res)
#     else:
#         return redirect("/MarkAttendance")
#     if request.POST:
#         status = request.POST['status']
#         if status == 'confirm':
#             from django.utils import timezone
#             current_date = timezone.now().date()
#             if Attendance.objects.filter(date=current_date,student=std,status='Present').exists():
#                 flag = 0
#             else:
#                 at = Attendance.objects.create(student=std,status='Present')
#                 at.save()
#                 flag = 1
#             return render(request, "MarkAttendance.html", {'std':std, "flag":flag})
#         else:
#             return redirect("/MarkAttendance")
#     return render(request, "MarkAttendance.html", {'std':std})


# def MarkAttendance(request):
#     from stApp import facetraining, final
#     data = Student.objects.values('name', 'id')  # 'id' must match recognizer ID
#     res = final.fun2(data)

#     if res != 'unknown':
#         try:
#             std = Student.objects.get(id=res)
#         except Student.DoesNotExist:
#             return render(request, "MarkAttendance.html", {"msg": "Student not found"})
#     else:
#         return redirect("/MarkAttendance")

#     if request.method == 'POST':
#         status = request.POST.get('status')
#         print(status,"$#%^&*()&^#$*&^%$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
#         if status == 'confirm':
#             from django.utils import timezone
#             current_date = timezone.now().date()
#             if not Attendance.objects.filter(date=current_date, student=std, status='Present').exists():
#                 Attendance.objects.create(student=std, status='Present')
#                 flag = 1
#                 msg="Attendence Added"
#                 return render(request, "MarkAttendance.html", {'msg':msg})
#             else:
#                 flag = 0
#                 msg="login failed"
#             return render(request, "MarkAttendance.html", {'std': std, "flag": flag,"msg":msg})
#         else:
#             return redirect("/MarkAttendance")

#     return render(request, "MarkAttendance.html", {'std': std})


def MarkAttendance(request):
    from stApp import final
    from django.utils import timezone

    data = Student.objects.values('name', 'id')

    res = final.fun2(data)

    if res != "unknown":
        try:
            std = Student.objects.get(id=res)
        except:
            return render(request, "MarkAttendance.html", {"msg": "Student not found"})
    else:
        return render(request, "MarkAttendance.html", {"msg": "Face not recognized"})

    if request.method == 'POST':
        status = request.POST.get('status')

        if status == 'confirm':
            current_date = timezone.now().date()

            Attendance.objects.get_or_create(
                student=std,
                date=current_date,
                defaults={'status': 'Present'}
            )

            return render(request, "MarkAttendance.html", {
                "msg": "Attendance Marked Successfully",
                "std": std
            })

        else:
            return render(request, "MarkAttendance.html", {
                "msg": "Cancelled",
                "std": std
            })

    return render(request, "MarkAttendance.html", {'std': std}) 




# from django.shortcuts import render, redirect
# from stApp import final
# from .models import Student, Attendance
# from django.utils import timezone

# def MarkAttendance(request):
#     # Step 1: Fetch student data
#     data = Student.objects.values('id', 'name')  # Ensure these match the face dataset

#     # Step 2: Recognize face using camera
#     recognized_id = final.fun2(data)

#     if recognized_id == "unknown":
#         return render(request, "MarkAttendance.html", {"msg": "⚠️ Face not recognized. Try again."})

#     # Step 3: Match student from DB
#     try:
#         std = Student.objects.get(id=recognized_id)
#     except Student.DoesNotExist:
#         return render(request, "MarkAttendance.html", {"msg": "⚠️ Face recognized, but no matching student found."})

#     # Step 4: Handle POST (Confirm button)
#     if request.method == 'POST':
#         status = request.POST.get('status')
#         if status == 'confirm':
#             current_date = timezone.now().date()
#             already_marked = Attendance.objects.filter(date=current_date, student=std, status='Present').exists()

#             if not already_marked:
#                 Attendance.objects.create(student=std, status='Present')
#                 return render(request, "MarkAttendance.html", {'std': std, 'flag': 1, 'msg': "✅ Attendance marked successfully."})
#             else:
#                 return render(request, "MarkAttendance.html", {'std': std, 'flag': 0, 'msg': "✅ Attendance already marked."})
#         else:
#             return redirect("/MarkAttendance")
        

#     # Step 5: Show confirmation page
#     return render(request, "MarkAttendance.html", {'std': std})




def adminhome(request):
    return render(request, "adminhome.html")


def adminadddepartment(request):
    msg = ''
    sty = ''
    if request.POST:
        dept = request.POST['dept']
        if Department.objects.filter(department=dept).exists():
            msg = "Department already exists"
            sty = "bg-danger p-3 text-light"
        else:
            d = Department.objects.create(department=dept)
            d.save()
            msg = "Department added"
            sty = "bg-success p-3 text-light"
    data = Department.objects.all()
    return render(request, "adminadddepartment.html", {"data": data, "msg":msg, "sty":sty})

def adminbatch(request):
    msg = ''
    sty = ''
    if request.POST:
        dept = request.POST['dept']
        batch = request.POST['batch']
        d = Department.objects.get(id=dept)
        if Course.objects.filter(course=batch, dept=d).exists():
            msg = "Batch already exists"
            sty = "bg-danger p-3 text-light"
        else:
            d = Course.objects.create(course=batch, dept=d)
            d.save()
            msg = "Batch added"
            sty = "bg-success p-3 text-light"
    data = Course.objects.all()
    depts = Department.objects.all()
    return render(request, "adminbatch.html", {"data": data, "msg":msg, "sty":sty, "depts":depts})

def admindeletedepartment(request):
    id = request.GET['id']
    data = Department.objects.get(id=id)
    data.delete()
    return redirect("/adminadddepartment")

def admindeletebatch(request):
    id = request.GET['id']
    data = Course.objects.get(id=id)
    data.delete()
    return redirect("/adminbatch")

def adminaddteachers(request):
    depts = Department.objects.all()
    msg = ''
    sty = ''
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        dept = request.POST['dept']
        if CustomUser.objects.filter(username=email).exists():
            msg = "Username already exists"
            sty = "bg-danger p-3 text-light"
        else:
            user = CustomUser.objects.create_user(
                username=email, password=phone, user_type='Teacher')

            user.save()
            getDept = Department.objects.get(id=dept)
            tec = Teacher.objects.create(
                name=name, email=email, phone=phone, address=address, dept=getDept, user=user)
            tec.save()
            msg = "Teacher details added"
            sty = "bg-success p-3 text-light"

    return render(request, "adminaddteachers.html", {"depts": depts, "msg":msg, "sty":sty})

def deleteTeacher(request):
    id = request.GET['id']
    data = Teacher.objects.get(id=id)
    data.delete()
    return redirect("/adminviewteachers")

def teacherhome(request):
    uid = request.session['uid']
    tid = Teacher.objects.get(user=uid)
    request.session['tid'] = tid.id
    return render(request, "teacherhome.html")


def teacheraddstudent(request):
    tid = request.session['tid']
    tec = Teacher.objects.get(id=tid)
    did = tec.dept
    courses = Course.objects.filter(dept=did)
    msg = ''
    sty = ''

    if request.POST:
        adno = request.POST['adno']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        acayear = request.POST['acayear']
        address = request.POST['address']
        course = request.POST['course']
        getDept = Course.objects.get(id=course)


        # user = CustomUser.objects.create_user(
        # username=email, password=phone, user_type='Student')
        # tec = Student.objects.create(admno=adno,
        #                             name=name, email=email, phone=phone, address=address, acayear=acayear, course=getDept, user=user)
        # user.save()
        # tec.save()
        # uid = tec.id
        # from . import fd
        # fd.fun(uid)

        # user = CustomUser.objects.create_user(
        # username=email, password=phone, user_type='Student')
        # tec = Student.objects.create(admno=adno,
        #                             name=name, email=email, phone=phone, address=address, acayear=acayear, course=getDept, user=user)
        # user.save()
        # tec.save()
        # uid = tec.id
        # from . import fd
        # fd.fun(uid)

        try:
            user = CustomUser.objects.create_user(
            username=email, password=phone, user_type='Student')
            tec = Student.objects.create(admno=adno,
                                        name=name, email=email, phone=phone, address=address, acayear=acayear, course=getDept, user=user)
            user.save()
            tec.save()
            uid = tec.id
            from . import fd
            fd.fun(uid)
        except:
            msg = "Error Occured"
            sty = "bg-danger p-3 text-light"
        else:
            msg = "Registration successful"
            sty = "bg-success p-3 text-light"


    return render(request, "teacheraddstudents.html", {"courses": courses, "msg": msg, "sty":sty})

def teacherViewStudents(request):
    students = Student.objects.all()
    return render(request, "teacherViewStudents.html", {"students": students})


def teacherattendance(request):
    data = ''
    if request.POST:
        course = request.POST['course']
        date = request.POST['date']
        data = Attendance.objects.filter(date=date,student__course__id=course)
    courses = Course.objects.all()
    return render(request, "teacherattendance.html", {"courses": courses, "data":data})

def adminViewAtt(request):
    data = ''
    if request.POST:
        course = request.POST['course']
        date = request.POST['date']
        data = Attendance.objects.filter(date=date,student__course__id=course)
    courses = Course.objects.all()
    return render(request, "adminViewAtt.html", {"courses": courses, "data":data})

def updateStatus(request):
    id = request.GET['id']
    status = request.GET['status']
    data = Attendance.objects.get(id=id)
    data.status = status
    data.save()
    return redirect("/teacherattendance")

def adminupdateStatus(request):
    id = request.GET['id']
    status = request.GET['status']
    data = Attendance.objects.get(id=id)
    data.status = status
    data.save()
    return redirect("/adminViewAtt")


def adminviewteachers(request):
    datas = Teacher.objects.all()
    return render(request, "adminviewteachers.html", {"datas": datas})



def studenthome(request):
    uid = request.session['uid']
    data = Student.objects.get(user=uid)
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        ePass = request.POST['ePass']
        user = CustomUser.objects.get(id=uid)
        user.set_password(ePass)
        user.save()
        stu = Student.objects.get(user=uid)
        stu.name = name
        stu.email = email
        stu.phone = phone
        stu.address = address
        stu.save()
        return redirect("/studenthome")
    return render(request, "studenthome.html", {"data": data})


def studentviewattendance(request):
    uid = request.session['uid']
    stu = Student.objects.get(user=uid)
    data = Attendance.objects.filter(student=stu.id).order_by("-id")
    if request.POST:
        date = request.POST['date']
        data = Attendance.objects.filter(student=stu.id, date=date).order_by("-id")
    return render(request, "studentviewattendance.html", {"data": data})
