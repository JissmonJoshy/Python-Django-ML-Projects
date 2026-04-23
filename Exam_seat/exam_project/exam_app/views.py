from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .models import *
from django.core.mail import send_mail
from django.contrib import messages
import random
import string
from django.contrib.auth import authenticate

# Create your views here
def index(request):
    return render(request, 'index.html')


def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def student_dashboard(request):
    return render(request, 'student/student_dashboard.html')

def staff_dashboard(request):
    return render(request, 'staff/staff_dashboard.html')



import base64
import random
import string
import pickle
import numpy as np
import face_recognition
from PIL import Image
from io import BytesIO
from django.conf import settings
import os


def student_register(request):

    courses = Course.objects.all()

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        register_no = request.POST.get("register_no")
        course_id = request.POST.get("course_id")

        captured_image = request.POST.get("captured_image")

        if not captured_image:
            messages.error(request,"Please capture your face.")
            return redirect("student_register")

        try:

            # Decode base64 image
            header, imgstr = captured_image.split(';base64,')
            image_data = base64.b64decode(imgstr)

            image = Image.open(BytesIO(image_data)).convert('RGB')
            image_np = np.array(image)

            # Face Detection
            face_locations = face_recognition.face_locations(image_np)

            if len(face_locations) != 1:
                messages.error(request,"Ensure only ONE face visible.")
                return redirect("student_register")

            encoding = face_recognition.face_encodings(image_np, face_locations)[0]
            face_encoding = pickle.dumps(encoding)

            # Save Image
            media_path = os.path.join(settings.MEDIA_ROOT,"students")
            os.makedirs(media_path,exist_ok=True)

            filename = f"{register_no}.jpg"
            filepath = os.path.join(media_path,filename)

            with open(filepath,"wb") as f:
                f.write(image_data)

            # Create Login
            otp = str(random.randint(100000,999999))

            user = Login.objects.create(
                username=username,
                email=email,
                usertype="student",
                otp=otp,
                is_verified=False
            )

            # Create Student
            Student.objects.create(
                login=user,
                course_id=course_id,
                full_name=full_name,
                phone=phone,
                address=address,
                email=email,
                register_no=register_no,
                image=f"students/{filename}",
                face_encoding=face_encoding
            )

            send_mail(
                "Your OTP",
                f"Your OTP is {otp}",
                "teamlccalwaye@gmail.com",
                [email]
            )

            request.session["otp_user_id"] = user.id

            messages.success(request,"OTP sent to email")
            return redirect("otp_verify")

        except Exception as e:
            print("Register error:",e)
            messages.error(request,"Registration failed")
            return redirect("student_register")

    return render(request,"student_register.html",{"courses":courses})


def otp_verify(request):
    if request.method == "POST":
        otp_input = request.POST.get("otp")
        user_id = request.session.get("otp_user_id")

        user = Login.objects.get(id=user_id)

        if user.otp == otp_input:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            user.set_password(password)
            user.viewpassword = password
            user.is_verified = True
            user.otp = None
            user.save()

            send_mail(
                "Your Login Password",
                f"Username: {user.username}\nPassword: {password}",
                "teamlccalwaye@gmail.com",
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "OTP verified successfully. Check your email for login details.")
            return redirect("login")

        messages.error(request, "Invalid OTP")
        return redirect("otp_verify")

    return render(request, "otp.html")

def staff_register(request):
    departments = Department.objects.all()

    if request.method == "POST":
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        phone = request.POST.get("phone").strip()
        full_name = request.POST.get("full_name").strip()
        address = request.POST.get("address").strip()
        department_id = request.POST.get("department_id")
        image = request.FILES.get("image")

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("staff_register")

        if Login.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("staff_register")

        if Staff.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists")
            return redirect("staff_register")

        user = Login.objects.create(
            username=username,
            email=email,
            usertype="staff",
            is_active=False
        )

        Staff.objects.create(
            login=user,
            department_id=department_id,   # ✅ SAVE DEPARTMENT
            full_name=full_name,
            phone=phone,
            address=address,
            email=email,
            image=image
        )

        messages.success(request, "Staff registered successfully. Wait for admin approval.")
        return redirect("login")

    return render(
        request,
        "staff_register.html",
        {"departments": departments}
    )



from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib import messages
import pickle
import face_recognition
import numpy as np


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        captured_image = request.POST.get("captured_image")

        user = authenticate(username=username,password=password)

        if user:

            request.session["user_id"] = user.id
            request.session["usertype"] = user.usertype

            if user.usertype == "admin":
                return redirect("admin_dashboard")

            if user.usertype == "staff":
                return redirect("staff_dashboard")

        # Student Login using Register No
        try:

            student = Student.objects.get(register_no=username)
            user = student.login

            if not check_password(password,user.password):
                messages.error(request,"Invalid password")
                return redirect("login")

            if not captured_image:
                messages.error(request,"Please capture face")
                return redirect("login")

            header, imgstr = captured_image.split(';base64,')
            image_data = base64.b64decode(imgstr)

            image = Image.open(BytesIO(image_data)).convert('RGB')
            image_np = np.array(image)

            face_locations = face_recognition.face_locations(image_np)

            if len(face_locations) != 1:
                messages.error(request,"Ensure only ONE face visible")
                return redirect("login")

            unknown_encoding = face_recognition.face_encodings(
                image_np,
                face_locations
            )[0]

            stored_encoding = pickle.loads(student.face_encoding)

            match = face_recognition.compare_faces(
                [stored_encoding],
                unknown_encoding,
                tolerance=0.5
            )

            if not match[0]:
                messages.error(request,"Face does not match")
                return redirect("login")

            request.session["user_id"] = user.id
            request.session["usertype"] = "student"

            messages.success(request,"Login successful")
            return redirect("student_dashboard")

        except Student.DoesNotExist:
            pass

        messages.error(request,"Invalid login credentials")

    return render(request,"login.html")

def adm(request):
    adm=Login.objects.create_superuser(username='admin',email='admin@gmail.com',viewpassword='admin',password='admin',usertype='admin')
    adm.save()
    return redirect('/')


from .models import Department
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Department
from django.shortcuts import render, redirect
from django.contrib import messages

def add_department(request):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        if Department.objects.filter(code=code).exists():
            messages.error(request, "Department code already exists")
            return redirect("add_department")

        Department.objects.create(
            name=name,
            code=code,
            description=description,
            image=image
        )
        messages.success(request, "Department added successfully")
        return redirect("add_department")
    

    departments = Department.objects.all()
    return render(request, "admin/add_department.html", {"departments": departments})

def edit_department(request, id):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    department = Department.objects.get(id=id)

    if request.method == "POST":
        department.name = request.POST.get("name")
        department.code = request.POST.get("code")
        department.description = request.POST.get("description")

        if request.FILES.get("image"):
            department.image = request.FILES.get("image")

        department.save()
        messages.success(request, "Department updated successfully")
        return redirect("add_department")

    return render(request, "admin/edit_department.html", {"department": department})

def delete_department(request, id):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    Department.objects.get(id=id).delete()
    messages.success(request, "Department deleted successfully")
    return redirect("add_department")


def add_course(request):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    departments = Department.objects.all()
    
    if request.method == "POST":
        department_id = request.POST.get("department")
        name = request.POST.get("name").strip()
        code = request.POST.get("code").strip()
        description = request.POST.get("description").strip()
        image = request.FILES.get("image")

        if Course.objects.filter(code=code).exists():
            messages.error(request, "Course code already exists")
            return redirect("add_course")

        Course.objects.create(
            department_id=department_id,
            name=name,
            code=code,
            description=description,
            image=image
        )
        messages.success(request, "Course added successfully")
        return redirect("add_course")

    courses = Course.objects.all()
    return render(request, "admin/add_course.html", {"departments": departments, "courses": courses})


def edit_course(request, id):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    course = Course.objects.get(id=id)
    departments = Department.objects.all()

    if request.method == "POST":
        course.department_id = request.POST.get("department")
        course.name = request.POST.get("name")
        course.code = request.POST.get("code")
        course.description = request.POST.get("description")

        if request.FILES.get("image"):
            course.image = request.FILES.get("image")

        course.save()
        messages.success(request, "Course updated successfully")
        return redirect("add_course")

    return render(request, "admin/edit_course.html", {"course": course, "departments": departments})


def delete_course(request, id):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    Course.objects.get(id=id).delete()
    messages.success(request, "Course deleted successfully")
    return redirect("add_course")



def add_semester(request):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    courses = Course.objects.all()

    if request.method == "POST":
        course_id = request.POST.get("course")
        semester_no = request.POST.get("semester_no").strip()
        description = request.POST.get("description").strip()
        image = request.FILES.get("image")

        Semester.objects.create(
            course_id=course_id,
            semester_no=semester_no,
            description=description,
            image=image
        )
        messages.success(request, "Semester added successfully")
        return redirect("add_semester")

    semesters = Semester.objects.all()
    return render(request, "admin/add_semester.html", {"courses": courses, "semesters": semesters})


def edit_semester(request, id):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    semester = Semester.objects.get(id=id)
    courses = Course.objects.all()

    if request.method == "POST":
        semester.course_id = request.POST.get("course")
        semester.semester_no = request.POST.get("semester_no")
        semester.description = request.POST.get("description")

        if request.FILES.get("image"):
            semester.image = request.FILES.get("image")

        semester.save()
        messages.success(request, "Semester updated successfully")
        return redirect("add_semester")

    return render(request, "admin/edit_semester.html", {"semester": semester, "courses": courses})


def delete_semester(request, id):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    Semester.objects.get(id=id).delete()
    messages.success(request, "Semester deleted successfully")
    return redirect("add_semester")



from .models import Subject, Semester

def add_subject(request):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    semesters = Semester.objects.all()

    if request.method == "POST":
        semester_id = request.POST.get("semester")
        name = request.POST.get("name").strip()
        code = request.POST.get("code").strip()
        description = request.POST.get("description").strip()
        image = request.FILES.get("image")

        if Subject.objects.filter(code=code).exists():
            messages.error(request, "Subject code already exists")
            return redirect("add_subject")

        Subject.objects.create(
            semester_id=semester_id,
            name=name,
            code=code,
            description=description,
            image=image
        )
        messages.success(request, "Subject added successfully")
        return redirect("add_subject")

    subjects = Subject.objects.all()
    return render(request, "admin/add_subject.html", {"semesters": semesters, "subjects": subjects})


def edit_subject(request, id):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    subject = Subject.objects.get(id=id)
    semesters = Semester.objects.all()

    if request.method == "POST":
        subject.semester_id = request.POST.get("semester")
        subject.name = request.POST.get("name")
        subject.code = request.POST.get("code")
        subject.description = request.POST.get("description")

        if request.FILES.get("image"):
            subject.image = request.FILES.get("image")

        subject.save()
        messages.success(request, "Subject updated successfully")
        return redirect("add_subject")

    return render(request, "admin/edit_subject.html", {"subject": subject, "semesters": semesters})


def delete_subject(request, id):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    Subject.objects.get(id=id).delete()
    messages.success(request, "Subject deleted successfully")
    return redirect("add_subject")



def add_hall(request):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    if request.method == "POST":
        name = request.POST.get("name").strip()
        capacity = request.POST.get("capacity")
        location = request.POST.get("location").strip()
        floor = request.POST.get("floor").strip()
        image = request.FILES.get("image")

        Hall.objects.create(
            name=name,
            capacity=capacity,
            location=location,
            floor=floor,
            image=image
        )
        messages.success(request, "Hall added successfully")
        return redirect("add_hall")

    halls = Hall.objects.all()
    return render(request, "admin/add_hall.html", {"halls": halls})


def edit_hall(request, id):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    hall = Hall.objects.get(id=id)

    if request.method == "POST":
        hall.name = request.POST.get("name").strip()
        hall.capacity = request.POST.get("capacity")
        hall.location = request.POST.get("location").strip()
        hall.floor = request.POST.get("floor").strip()

        if request.FILES.get("image"):
            hall.image = request.FILES.get("image")

        hall.save()
        messages.success(request, "Hall updated successfully")
        return redirect("add_hall")

    return render(request, "admin/edit_hall.html", {"hall": hall})


def delete_hall(request, id):
    if request.session.get("usertype") != "admin":
        return redirect("login")

    Hall.objects.get(id=id).delete()
    messages.success(request, "Hall deleted successfully")
    return redirect("add_hall")

def student_profile(request):
    if request.session.get("usertype") != "student":
        return redirect("login")

    user_id = request.session.get("user_id")
    student = Student.objects.get(login_id=user_id)

    return render(request, "student/student_profile.html", {"student": student})

def edit_student_profile(request):
    if request.session.get("usertype") != "student":
        return redirect("login")

    user_id = request.session.get("user_id")
    student = Student.objects.get(login_id=user_id)
    courses = Course.objects.all()

    if request.method == "POST":
        student.full_name = request.POST.get("full_name")
        student.phone = request.POST.get("phone")
        student.address = request.POST.get("address")
        student.course_id = request.POST.get("course_id")

        if request.FILES.get("image"):
            student.image = request.FILES.get("image")

        student.save()
        messages.success(request, "Profile updated successfully")
        return redirect("student_profile")

    return render(
        request,
        "student/edit_student_profile.html",
        {"student": student, "courses": courses}
    )


def display_all_students(request):
    students = Student.objects.all()
    return render(request, 'admin/display_all_students.html', {'students': students})


def reject_student(request, student_id):
    student = Student.objects.get(id=student_id)
    login_id = student.login.id
    student.delete()
    messages.success(request, "Student deleted successfully")
    Login.objects.get(id=login_id).delete()
    return redirect('display_all_students')


def display_all_staffs(request):
    staffs = Staff.objects.all()
    return render(request, 'admin/display_all_staffs.html', {'staffs': staffs})

def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def approve_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    login = staff.login

    # Generate random password
    raw_password = generate_password()

    # Save password
    login.password = make_password(raw_password)
    login.viewpassword = raw_password
    login.is_active = True
    login.save()

    # Send email
    subject = "Staff Account Approved"
    message = f"""
Dear {staff.full_name},

Your staff account has been approved.

Login Details:
Username: {login.username}
Password: {raw_password}

Please login and change your password after first login.

Regards,
Admin Team
"""
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [staff.email],
        fail_silently=False
    )

    messages.success(request, "Staff approved and login credentials sent via email")
    return redirect('display_all_staffs')


def reject_staff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    login_id = staff.login.id
    staff.delete()
    messages.success(request, "Staff deleted successfully")
    Login.objects.get(id=login_id).delete()
    return redirect('display_all_staffs')



def staff_profile(request):
    user_id = request.session.get("user_id")
    staff = get_object_or_404(Staff, login_id=user_id)
    return render(request, "staff/staff_profile.html", {"staff": staff})


def edit_staff_profile(request):
    user_id = request.session.get("user_id")
    staff = get_object_or_404(Staff, login_id=user_id)

    if request.method == "POST":
        staff.full_name = request.POST.get("full_name")
        staff.phone = request.POST.get("phone")
        staff.address = request.POST.get("address")
        staff.department_id = request.POST.get("department")

        if request.FILES.get("image"):
            staff.image = request.FILES.get("image")

        staff.save()
        messages.success(request, "Profile updated successfully")
        return redirect("staff_profile")

    departments = Department.objects.all()
    return render(
        request,
        "staff/edit_staff_profile.html",
        {"staff": staff, "departments": departments}
    )
def add_exam_schedule(request):
    subjects = Subject.objects.all()
    halls = Hall.objects.all()

    if request.method == "POST":
        subject_id = request.POST.get("subject")
        exam_date = request.POST.get("exam_date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        hall_id = request.POST.get("hall")

        conflict = ExamSchedule.objects.filter(
            hall_id=hall_id,
            exam_date=exam_date,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if conflict.exists():
            messages.error(request, "Hall already booked for this time")
            return redirect("add_exam_schedule")

        ExamSchedule.objects.create(
            subject_id=subject_id,
            hall_id=hall_id,
            exam_date=exam_date,
            start_time=start_time,
            end_time=end_time
        )

        messages.success(request, "Exam scheduled successfully")
        return redirect("view_exam_schedules")

    return render(request, "admin/add_exam_schedule.html", {
        "subjects": subjects,
        "halls": halls
    })


def view_exam_schedules(request):
    exams = ExamSchedule.objects.select_related(
        "subject", "hall"
    ).order_by("exam_date", "start_time")

    return render(request, "admin/view_exam_schedules.html", {
        "exams": exams
    })

def edit_exam_schedule(request, id):
    exam = get_object_or_404(ExamSchedule, id=id)
    subjects = Subject.objects.all()
    halls = Hall.objects.all()

    if request.method == "POST":
        subject_id = request.POST.get("subject")
        exam_date = request.POST.get("exam_date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        hall_id = request.POST.get("hall")

        conflict = ExamSchedule.objects.filter(
            hall_id=hall_id,
            exam_date=exam_date,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exclude(id=id)

        if conflict.exists():
            messages.error(request, "Hall already booked for this time")
            return redirect("edit_exam_schedule", id=id)

        exam.subject_id = subject_id
        exam.hall_id = hall_id
        exam.exam_date = exam_date
        exam.start_time = start_time
        exam.end_time = end_time
        exam.save()

        messages.success(request, "Exam updated successfully")
        return redirect("view_exam_schedules")

    return render(request, "admin/edit_exam_schedule.html", {
        "exam": exam,
        "subjects": subjects,
        "halls": halls
    })


def delete_exam_schedule(request, id):
    exam = get_object_or_404(ExamSchedule, id=id)
    exam.delete()
    messages.success(request, "Exam schedule deleted")
    return redirect("view_exam_schedules")

def assign_staff_view(request):
    exams = ExamSchedule.objects.all().order_by('exam_date', 'start_time')
    context = {
        'exams': exams
    }
    return render(request, 'admin/assign_staff.html', context)

def assign_staff_action(request, exam_id):
    exam = ExamSchedule.objects.get(id=exam_id)

    # Get all staff who are active and free at the same date and time
    available_staff = Staff.objects.filter(login__is_active=True).exclude(
        id__in=ExamSchedule.objects.filter(
            exam_date=exam.exam_date,
            start_time__lt=exam.end_time,
            end_time__gt=exam.start_time
        ).values_list('staff', flat=True)
    )

    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        if staff_id:
            staff_member = Staff.objects.get(id=staff_id)
            exam.staff = staff_member
            exam.save()
            messages.success(request, f"{staff_member.full_name} assigned successfully!")
            return redirect('assign_staff')

    context = {
        'exam': exam,
        'available_staff': available_staff
    }
    return render(request, 'admin/assign_staff_action.html', context)

def exam_schedules_staff(request):
    user_id = request.session.get("user_id")
    staff = Staff.objects.get(login_id=user_id)

    exams = ExamSchedule.objects.filter(
        staff=staff
    ).order_by('exam_date', 'start_time')

    return render(request, "staff/exam_schedules_staff.html", {
        "exams": exams
    })


def exam_schedules_student(request):
    user_id = request.session.get("user_id")
    student = Student.objects.get(login_id=user_id)

    exams = ExamSchedule.objects.filter(
        subject__semester__course=student.course
    ).order_by('exam_date', 'start_time')

    return render(request, "student/exam_schedules_student.html", {
        "exams": exams,
        "student": student
    })


def exam_list_for_seat_allocation(request):
    exams = ExamSchedule.objects.all().order_by('exam_date')
    return render(request, "admin/exam_list_allocate_seats.html", {
        "exams": exams
    })
import random
import random

def allocate_seats(request, exam_id):
    exam = ExamSchedule.objects.get(id=exam_id)

    students = Student.objects.filter(course=exam.subject.semester.course)

    allocated = SeatAllocation.objects.filter(exam=exam)
    allocated_seats = [a.seat_number for a in allocated]
    allocated_student_ids = [a.student.id for a in allocated]

    total_seats = exam.hall.capacity
    seat_numbers = list(range(1, total_seats + 1))

    available_seats = [seat for seat in seat_numbers if seat not in allocated_seats]

    # 🔥 NEW: Unallocated students only
    unallocated_students = students.exclude(id__in=allocated_student_ids)

    if request.method == "POST":

        if not available_seats:
            messages.error(request, "No available seats left!")
            return redirect("allocate_seats", exam_id=exam.id)

        if not unallocated_students:
            messages.warning(request, "All students already allocated!")
            return redirect("allocate_seats", exam_id=exam.id)

        # 🔥 Shuffle both lists
        random.shuffle(available_seats)
        students_list = list(unallocated_students)
        random.shuffle(students_list)

        allocations = []

        for student, seat in zip(students_list, available_seats):
            allocations.append(
                SeatAllocation(
                    exam=exam,
                    student=student,
                    seat_number=seat
                )
            )

        # 🔥 Bulk create (fast)
        SeatAllocation.objects.bulk_create(allocations)

        messages.success(request, "All students allocated seats successfully!")
        return redirect("allocate_seats", exam_id=exam.id)

    return render(request, "admin/allocate_seats.html", {
        "exam": exam,
        "students": students,
        "seat_numbers": seat_numbers,
        "allocated_seats": allocated_seats,
        "allocated": allocated,
        "allocated_student_ids": allocated_student_ids,
        "available_seats": available_seats
    })


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def reset_allocations(request, exam_id):
    exam = get_object_or_404(ExamSchedule, id=exam_id)

    # Delete all seat allocations for this exam
    deleted_count, _ = SeatAllocation.objects.filter(exam=exam).delete()

    messages.success(request, f"{deleted_count} seat allocations cleared successfully!")
    return redirect("allocate_seats", exam_id=exam.id)


def delete_seat_allocation(request, allocation_id):
    allocation = get_object_or_404(SeatAllocation, id=allocation_id)
    exam_id = allocation.exam.id
    allocation.delete()
    messages.success(request, f"Seat {allocation.seat_number} for {allocation.student.full_name} removed successfully!")
    return redirect("allocate_seats", exam_id=exam_id)


def ChatBot(request):
    import os
    os.system("python chatgui.py")  # Runs the Python file
    print("hello world hiiii")
    return redirect("student_dashboard")