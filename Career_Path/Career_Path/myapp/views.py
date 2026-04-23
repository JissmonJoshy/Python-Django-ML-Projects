
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib import messages
from django.db.models import Q
from httpx import request
from .models import *

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.

def index(request):
    return render(request, 'index.html')


def adm(request):
    adm=Login.objects.create_superuser(username='admin',email='admin@gmail.com',viewpassword='admin',password='admin',usertype='admin')
    adm.save()
    return redirect('/')

# def delete_login(request):
#     Login.objects.filter(id=2).delete()
#     return redirect('')

def adminhome(request):
    return render(request, 'adminpg/adminhome.html')

def clienthome(request):
    return render(request, 'client/clienthome.html')   
def company_reg(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        img = request.FILES.get('img')
        proof = request.FILES.get('proof')
        certification = request.FILES.get('certification')

        if Login.objects.filter(email=email).exists():
            messages.info(request, "Email already registered")
            return redirect('company_reg')

        if not phone.isdigit() or len(phone) != 10:
            messages.info(request, "Invalid phone number")
            return redirect('company_reg')

        log = Login.objects.create_user(
            username=email,
            password=password,
            email=email,
            usertype='company',
            is_active=0,
            viewpassword=password
        )
        log.save()

        Company.objects.create(
            loginid=log,
            name=name,
            email=email,
            phone=phone,
            address=address,
            img=img,
            proof=proof,
            certification=certification  
        )

        messages.success(request, "Company registered successfully. Await admin approval.")
        return redirect('login')

    return render(request, 'company_reg.html')

def tutor_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        qualification = request.POST['qualification']
        img = request.FILES.get('img')
        proof = request.FILES.get('proof')
        certification = request.FILES.get('certification')

        if Login.objects.filter(email=email).exists():
            messages.info(request, "Email already registered")
            return redirect('tutor_register')

        if not phone.isdigit() or len(phone) != 10:
            messages.info(request, "Invalid phone number")
            return redirect('tutor_register')

        log = Login.objects.create_user(
            username=email,
            password=password,
            email=email,
            usertype='tutor',
            is_active=0,
            viewpassword=password
        )

        Tutor.objects.create(
            loginid=log,
            name=name,
            email=email,
            phone=phone,
            address=address,
            qualification=qualification,
            img=img,
            proof=proof,
            certification=certification
        )

        messages.success(request, "Tutor registered successfully. Await admin approval.")
        return redirect('login')

    return render(request, 'tutor_register.html')

def Client_reg(request):
    if request.method == 'POST':
        name=request.POST['name']
        address =  request.POST["address"]
        password =  request.POST["password"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        qua=request.POST['qua']
        img = request.FILES.get('img')
        if Login.objects.filter(email=email).exists():
            messages.info(request,"Already Have Registered")
        log = Login.objects.create_user(username=email, password=password,email=email,usertype='client', viewpassword=password)
        log.save()
        client = Client.objects.create(loginid=log,name=name, email=email, address=address, phone=phone, dob=dob, img=img,qualification=qua)
        client.save()
        messages.success(request, "Registration Successful")
        return redirect('login')
    else:
        return render(request, 'client_reg.html')
    

def view_companies(request):
    companies = Company.objects.all()
    return render(request, 'adminpg/view_companies.html', {'companies': companies})


def approve_company(request):
    cid = request.GET.get('id')
    company = Company.objects.get(id=cid)
    login = company.loginid
    login.is_active = 1
    login.save()
    messages.success(request, "Company approved successfully")
    return redirect('/view_companies')


def delete_company(request):
    cid = request.GET.get('id')
    company = Company.objects.get(id=cid)
    login = company.loginid
    company.delete()
    login.delete()
    messages.success(request, "Company deleted successfully")
    return redirect('/view_companies')

from django.contrib.auth import authenticate, login as auth_login

def login(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request,username=username, password=password)
        
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                request.session['uid'] = user.id
                if user.usertype == "admin":
                    messages.info(request, "Welcome To The Admin Page")
                    return redirect("/adminhome")
                elif user.usertype == "client":
                    messages.info(request, "Welcome To The Client Dashboard")
                    return redirect("/clienthome")
                elif user.usertype == "tutor":
                    messages.info(request, "Welcome To The Tutor Dashboard")
                    return redirect("/tutorhome")
                elif user.usertype == "company":
                    messages.info(request, "Welcome To The Company Dashboard")
                    return redirect("/companyhome")  # Replace with actual company dashboard URL
                else:
                    messages.warning(request, "Invalid user role.")
                    return redirect("/login")
            else:
                messages.warning(request, "Account is inactive.")
                return redirect("/login")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("/login")
    
    return render(request, 'login.html')



###############ADMIN############

def admin_viewClients(request):
    clients = Client.objects.all()
    return render(request, 'adminpg/view_clients.html', {'clients': clients})



def adm_dlClient(request):
    id= request.GET.get('id')
    client = Client.objects.get(id=id).delete()
    messages.success(request, "Client Deleted Successfully")
    return redirect('/admin_viewClients')
  


def tutor_add_course(request):
    if 'uid' not in request.session:
        return redirect('/login')

    login_user = Login.objects.get(id=request.session['uid'])
    tutor = Tutor.objects.get(loginid=login_user)

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        duration = request.POST['duration']
        fees = request.POST['fees']
        img = request.FILES.get('img')

        Course.objects.create(
            name=name,
            description=description,
            duration=duration,
            fees=fees,
            img=img,
            tutor=tutor
        )

        messages.success(request, "Course added successfully")
        return redirect('/tutorhome')

    return render(request, 'tutor/tutor_add_course.html')


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'adminpg/courselist.html', {'courses': courses})


def adm_viewCourses(request):
    id= request.GET.get('id')
    courses = Course.objects.get(id=id)
    return render(request, 'adminpg/adm_viewCourses.html', {'courses': courses})



def adm_viewapplycourse(request):
    courses= Course.objects.filter(status='applied')
    return render(request, 'adminpg/adm_viewapplycourse.html', {'courses': courses})


def approve(request):
    
    course_id = request.GET.get('course_id')
    
    course = Course.objects.get(id=course_id)
    course.status = 'Approved'
    course.save()
    messages.success(request, "Course application approved successfully.")
        
    return redirect('/adm_viewapplycourse')


def add_jobs(request):
    login_id = request.session.get('uid')

    if not login_id:
        return redirect('/login')

    user = Login.objects.get(id=login_id)

    if user.usertype != 'company':
        return redirect('/login')

    company = Company.objects.filter(loginid=user).first()

    if not company:
        messages.error(request, "Company profile not found. Please complete company registration.")
        return redirect('/companyhome')

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']
        salary = request.POST['salary']
        img = request.FILES['img']
        job_type = request.POST['job_type']  # ✅ NEW

        Job.objects.create(
            name=title,
            description=description,
            company=company,
            location=location,
            salary=salary,
            img=img,
            job_type=job_type  # ✅ NEW
        )

        messages.success(request, "Job Added Successfully")
        return redirect('/companyhome')

    return render(request, 'company/add_jobs.html')

def company_added_jobs(request):
    login_id = request.session.get('uid')

    if not login_id:
        return redirect('/login')

    user = Login.objects.get(id=login_id)

    if user.usertype != 'company':
        return redirect('/login')

    company = Company.objects.filter(loginid=user).first()

    jobs = Job.objects.filter(company=company).order_by('-created_at')

    return render(request, 'company/company_added_jobs.html', {'jobs': jobs})

def edit_company_job(request, id):
    login_id = request.session.get('uid')

    if not login_id:
        return redirect('/login')

    user = Login.objects.get(id=login_id)
    company = Company.objects.filter(loginid=user).first()

    job = Job.objects.get(id=id, company=company)

    if request.method == 'POST':
        job.name = request.POST['title']
        job.description = request.POST['description']
        job.location = request.POST['location']
        job.salary = request.POST['salary']

        if 'img' in request.FILES:
            job.img = request.FILES['img']

        job.save()
        messages.success(request, "Job Updated Successfully")
        return redirect('company_added_jobs')

    return render(request, 'company/edit_company_jobs.html', {'job': job})

def delete_company_job(request, id):
    login_id = request.session.get('uid')

    if not login_id:
        return redirect('/login')

    user = Login.objects.get(id=login_id)
    company = Company.objects.filter(loginid=user).first()

    Job.objects.filter(id=id, company=company).delete()

    messages.success(request, "Job Deleted Successfully")
    return redirect('company_added_jobs')



def adm_viewJobs(request):
    jobs = Job.objects.all()
    return render(request, 'adminpg/adm_viewJobs.html', {'jobs': jobs})


def dlt_course(request):
    id= request.GET.get('id')
    client = Course.objects.get(id=id).delete()
    messages.success(request, "Course Deleted Successfully")
    return redirect("/course_list")




def view_feedbacks(request):
    feedbacks = Feedback.objects.select_related('client', 'course').all()
    return render(request, 'adminpg/view_feedback.html', {'feedbacks': feedbacks})


def add_question(request):
    courses = Course.objects.all()

    if request.method == "POST":
        course = Course.objects.get(id=request.POST['course'])

        option1 = request.POST['option1']
        option2 = request.POST['option2']
        option3 = request.POST['option3']
        option4 = request.POST['option4']

        correct_key = request.POST['correct_answer']

        if correct_key == 'option1':
            correct_answer = option1
        elif correct_key == 'option2':
            correct_answer = option2
        elif correct_key == 'option3':
            correct_answer = option3
        else:
            correct_answer = option4

        Question.objects.create(
            course=course,
            question=request.POST['question'],
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_answer=correct_answer
        )

        messages.success(request, "Question added successfully")
        return redirect('/add_question')

    return render(request, 'adminpg/add_questions.html', {'courses': courses})


def view_questions(request):
    courses = Course.objects.all()
    selected_course = request.GET.get('course')
    questions = None

    if selected_course:
        questions = Question.objects.filter(course_id=selected_course)

    return render(request, 'adminpg/view_questions.html', {
        'courses': courses,
        'questions': questions,
        'selected_course': selected_course
    })


################CLIENT############


def clientprofile(request):
    uid= request.session['uid']
    client = Client.objects.get(loginid=uid)
    return render(request, 'client/clientprofile.html', {'client': client})



def edit_client_profile(request):
    if 'uid' not in request.session:
        messages.error(request, "Please log in first.")
        return redirect('/login')

    uid = request.session['uid']
    client = Client.objects.get(loginid=uid)

    if request.method == 'POST':
        client.name = request.POST.get('name', client.name)
        client.address = request.POST.get('address', client.address)
        client.email = request.POST.get('email', client.email)
        client.phone = request.POST.get('phone', client.phone)
        client.dob = request.POST.get('dob', client.dob)
        client.qualification = request.POST.get('qualification', client.qualification)

        if 'img' in request.FILES:
            client.img = request.FILES['img']

        client.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('/clientprofile')

    return render(request, 'client/edit_client_profile.html', {'client': client})




def client_view_courses(request):
    courses = Course.objects.filter(status__iexact='approved')
    return render(request, 'client/client_view_courses.html', {'courses': courses})


def client_view_coursedetails(request):
    id = request.GET.get('id')
    courses = Course.objects.get(id=id)
    return render(request, 'client/client_view_coursedetails.html', {'courses': courses})



def applycourse(request):
    if 'uid' not in request.session:
        messages.error(request, "Please log in to apply for a course.")
        return redirect('/login')  

    uid = request.session['uid']
    course_id = request.GET.get('id')

    try:
        client = Client.objects.get(loginid=uid)

        # Check if the client has already applied for or been approved for a course
        existing_course = Course.objects.filter(clients=client).exclude(status='Rejected').first()

        if existing_course:
            messages.warning(request, "You have already applied for a course.")
            return redirect('/client_view_courses')

        # Proceed to apply for the new course
        course = Course.objects.get(id=course_id)
        course.clients = client
        course.status = 'applied'
        course.save()

        messages.success(request, "Course application submitted successfully.")
    except Course.DoesNotExist:
        messages.error(request, "Course not found.")
    except Client.DoesNotExist:
        messages.error(request, "Client not found.")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")

    return redirect('/client_view_courses')


def course_payment(request):
    if 'uid' not in request.session:
        return redirect('/login')

    course_id = request.GET.get('id')
    client = Client.objects.get(loginid=request.session['uid'])
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        link = generate_meet_link()

        Enrollment.objects.create(
            client=client,
            course=course,
            status='paid',
            meet_link=link
        )

        messages.success(request, "Payment successful and class link generated")
        return redirect('/client_my_courses')

    return render(request, 'client/course_payment.html', {'course': course})

def client_my_courses(request):
    if 'uid' not in request.session:
        return redirect('/login')

    client = Client.objects.get(loginid=request.session['uid'])
    enrollments = Enrollment.objects.filter(client=client)

    return render(request, 'client/client_my_courses.html', {
        'enrollments': enrollments
    })


def client_view_notes(request, course_id):
    if 'uid' not in request.session:
        return redirect('/login')

    client = Client.objects.get(loginid=request.session['uid'])

    # check if client enrolled in this course (security ✅)
    is_enrolled = Enrollment.objects.filter(client=client, course_id=course_id).exists()

    if not is_enrolled:
        return redirect('/client-my-courses')

    notes = Notes.objects.filter(course_id=course_id).order_by('-id')

    return render(request, 'client/client_view_notes.html', {
        'notes': notes
    })

import random
import string

def generate_meet_link():
    import uuid
    return f"https://meet.jit.si/{uuid.uuid4()}"


def tutor_enrolled_students(request):
    if 'uid' not in request.session:
        return redirect('/login')

    tutor = Tutor.objects.get(loginid=request.session['uid'])

    enrollments = Enrollment.objects.filter(
        course__tutor=tutor,
        status='paid'
    ).select_related('client', 'course')

    notes = Notes.objects.filter(tutor=tutor)

    return render(request, 'tutor/tutor_enrolled_students.html', {
        'enrollments': enrollments,
        'notes': notes
    })

def add_notes(request):
    if 'uid' not in request.session:
        return redirect('/login')

    tutor = Tutor.objects.get(loginid=request.session['uid'])
    courses = Course.objects.filter(tutor=tutor)

    if request.method == "POST":
        course_id = request.POST['course']
        title = request.POST['title']
        file = request.FILES['file']

        course = Course.objects.get(id=course_id)

        Notes.objects.create(
            course=course,
            tutor=tutor,
            title=title,
            file=file
        )

        return redirect('/add-notes')

    return render(request, 'tutor/add_notes.html', {
        'courses': courses
    })

def view_notes(request):
    if 'uid' not in request.session:
        return redirect('/login')

    tutor = Tutor.objects.get(loginid=request.session['uid'])

    notes = Notes.objects.filter(tutor=tutor).order_by('-id')

    return render(request, 'tutor/view_notes.html', {
        'notes': notes
    })

def delete_note(request, id):
    if 'uid' not in request.session:
        return redirect('/login')

    note = Notes.objects.get(id=id)
    note.delete()

    return redirect('/view-notes')

def approved_courses(request):
    if 'uid' not in request.session:
        messages.error(request, "Please log in to view approved courses.")
        return redirect('/login')  

    uid = request.session['uid']
    client = Client.objects.get(loginid=uid)
    approved_courses = Course.objects.filter(clients=client, status='Approved')

    return render(request, 'client/approved_courses.html', {'approved_courses': approved_courses})


# def payment(request):
#     if 'uid' not in request.session:
#         messages.error(request, "Please log in to make a payment.")
#         return redirect('/login')  

#     uid = request.session['uid']
#     client = Client.objects.get(loginid=uid)
#     courses = Course.objects.filter(clients=client, status='Approved')

#     if request.method == 'POST':
#         # Handle payment logic here
#         messages.success(request, "Payment successful.")
#         return redirect('/clienthome')

#     return render(request, 'client/payment_page.html', {'courses': courses})
def payment(request):
    if 'uid' not in request.session:
        messages.error(request, "Please log in to make a payment.")
        return redirect('/login')  

    uid = request.session['uid']
    client = Client.objects.get(loginid=uid)
    courses = Course.objects.filter(clients=client, status='Approved', payment_status='unpaid')

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        try:
            course = Course.objects.get( clients=client)
            course.payment_status = 'paid'
            course.save()
            messages.success(request, "Payment successful.")
        except Course.DoesNotExist:
            messages.error(request, "Invalid course selection.")
        return redirect('/clienthome')

    return render(request, 'client/payment_page.html', {'courses': courses})


def client_view_jobs(request):
    jobs = Job.objects.all()

    search = request.GET.get('search')
    if search:
        jobs = jobs.filter(
            Q(name__icontains=search) | Q(company__name__icontains=search)
        )

    job_type = request.GET.get('job_type')
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    applications = []

    if 'uid' in request.session:
        login_user = Login.objects.get(id=request.session['uid'])
        client = Client.objects.get(loginid=login_user)
        applications = JobApply.objects.filter(client=client)

    return render(request, 'client/client_view_jobs.html', {
        'jobs': jobs,
        'applications': applications   # ✅ send full objects
    })
import uuid

def generate_meet_link():
    return f"https://meet.jit.si/{uuid.uuid4()}"


def apply_job(request, job_id):
    if 'uid' not in request.session:
        return redirect('/login')

    job = Job.objects.get(id=job_id)
    login_user = Login.objects.get(id=request.session['uid'])
    client = Client.objects.get(loginid=login_user)

    already_applied = JobApply.objects.filter(job=job, client=client).exists()
    if already_applied:
        messages.warning(request, "You already applied for this job")
        return redirect('/client_view_jobs')

    if request.method == "POST":
        cv = request.FILES.get('cv')

        meet_link = generate_meet_link()  # ✅ CREATE LINK

        JobApply.objects.create(
            job=job,
            client=client,
            name=client.name,
            email=client.email,
            phone=client.phone,
            qualification=client.qualification,
            cv=cv,
            meet_link=meet_link,  # ✅ SAVE
            status='Applied'
        )

        messages.success(request, "Job applied successfully")
        return redirect('/client_view_jobs')

    return render(request, 'client/apply_job.html', {
        'job': job,
        'client': client
    })



def client_interest(request):
    if request.method == 'POST':
        stream = request.POST.get('qualification')
        fav_subject = request.POST.get('fav_subject')
        tech_skills = request.POST.getlist('tech_skills')
        soft_skills = request.POST.getlist('soft_skills')
        languages_known = request.POST.getlist('languages_known')
        interest = request.POST.get('interest')
        hobbies = request.POST.getlist('hobbies')
        age = request.POST.get('Age')
        tenth_mark = request.POST.get('ten_mark')
        twelfth_mark = request.POST.get('mark')

        # Optional: convert lists to comma-separated strings if storing in CharField
        hobbies_str = ", ".join(hobbies)
        tech_skills_str = ", ".join(tech_skills)
        soft_skills_str = ", ".join(soft_skills)
        languages_str = ", ".join(languages_known)

        # Load dataset
        df = pd.read_csv(f"{BASE_DIR}/myapp/indian_career_dataset_100k.csv")

        # Combine all textual features into a single string for each row
        df['combined_text'] = df['stream'] + ' ' + \
                            df['favorite_subject'] + ' ' + \
                            df['technical_skills'] + ' ' + \
                            df['soft_skills'] + ' ' + \
                            df['languages_known'] + ' ' + \
                            df['interests'] + ' ' + \
                            df['hobbies']

        # Features and target
        X = df['combined_text']
        y = df['career']

        # Convert target labels to numerical values
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        # Convert text features to numerical vectors
        vectorizer = TfidfVectorizer()
        X_vectorized = vectorizer.fit_transform(X)

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y_encoded, test_size=0.2, random_state=42)

        # Model: Random Forest
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluation
        y_pred = model.predict(X_test)
        print("✅ Accuracy:", accuracy_score(y_test, y_pred))
        print("🔍 Classification Report:")
        print(classification_report(y_test, y_pred, target_names=le.classes_))

        # Prediction function
        def predict_career(new_data_dict):
            combined = new_data_dict['stream'] + ' ' + \
                    new_data_dict['favorite_subject'] + ' ' + \
                    new_data_dict['technical_skills'] + ' ' + \
                    new_data_dict['soft_skills'] + ' ' + \
                    new_data_dict['languages_known'] + ' ' + \
                    new_data_dict['interests'] + ' ' + \
                    new_data_dict['hobbies']
            vectorized = vectorizer.transform([combined])
            prediction = model.predict(vectorized)
            return le.inverse_transform(prediction)[0]

        # Test the predictor
        sample_input = {
            "stream": stream,
            "favorite_subject": fav_subject,
            "technical_skills": tech_skills_str,
            "soft_skills": soft_skills_str,
            "languages_known": languages_str,
            "interests": interest,
            "hobbies": hobbies_str
        }
        print("🔍 Sample Input:", sample_input)
        suggested_career = predict_career(sample_input)
        print("🧠 Predicted Career:", suggested_career )

        return render(request, 'client/career_suggestion.html', {'career': suggested_career})

    return render(request,'client/client_interests.html')

def give_feedback(request):
    if 'uid' not in request.session:
        messages.warning(request, "You must log in to give feedback.")
        return redirect('/login')

    client = Client.objects.get(loginid=request.session['uid'])
    selected_course_id = request.GET.get('course_id')

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        feedback_text = request.POST.get('feedback')
        rating = request.POST.get('rating')

        if not course_id or not feedback_text or not rating:
            messages.warning(request, "All fields are required.")
        else:
            course = Course.objects.get(id=course_id)
            Feedback.objects.create(
                client=client,
                course=course,
                feedback=feedback_text,
                rating=rating
            )
            messages.success(request, "Thank you! Your feedback has been submitted.")
            return redirect('/client_my_courses')

    courses = Course.objects.filter(clients=client)
    return render(
        request,
        'client/feedback_form.html',
        {
            'courses': courses,
            'selected_course_id': selected_course_id
        }
    )



def tutor_feedbacks(request):
    if 'uid' not in request.session:
        return redirect('/login')

    tutor = Tutor.objects.get(loginid=request.session['uid'])

    feedbacks = Feedback.objects.filter(course__tutor=tutor).select_related('client', 'course')

    return render(request, 'tutor/tutor_feedbacks.html', {
        'feedbacks': feedbacks
    })



from random import sample

def attempt_quiz(request, course_id):
    if 'uid' not in request.session:
        messages.error(request, "Please log in to attempt quiz.")
        return redirect('/login')  

    client = Client.objects.get(loginid=request.session['uid'])
    course = Course.objects.get(id=course_id)
    questions = list(Question.objects.filter(course=course))

    if len(questions) < 5:
        messages.warning(request, "Not enough questions for this course to attempt quiz.")
        return redirect('/approved_courses')

    # pick 5 random questions
    selected_questions = sample(questions, 5)

    if request.method == "POST":
        score = 0
        for q in selected_questions:
            selected_answer = request.POST.get(f"q_{q.id}")
            if selected_answer == q.correct_answer:
                score += 1

        QuizAttempt.objects.create(
            client=client,
            course=course,
            score=score,
            total_questions=5
        )

        messages.success(request, f"Quiz submitted successfully. Your score: {score}/5")
        return redirect('/approved_courses')

    return render(request, 'client/attempt_quiz.html', {'course': course, 'questions': selected_questions})


def view_marks(request):
    if 'uid' not in request.session:
        messages.error(request, "Please login to view marks.")
        return redirect('/login')

    client = Client.objects.get(loginid=request.session['uid'])
    attempts = QuizAttempt.objects.filter(client=client).order_by('-created_at')

    return render(request, 'client/view_marks.html', {
        'attempts': attempts
    })
#############COMPANY############    


def companyhome(request):
    return render(request, 'company/companyhome.html')

def company_profile(request):
    uid = request.session.get('uid')
    company = Company.objects.get(loginid_id=uid)
    return render(request, 'company/company_profile.html', {'company': company})


def edit_company_profile(request):
    uid = request.session.get('uid')
    company = Company.objects.get(loginid_id=uid)

    if request.method == 'POST':
        company.name = request.POST['name']
        company.phone = request.POST['phone']
        company.address = request.POST['address']

        if request.FILES.get('img'):
            company.img = request.FILES.get('img')

        company.save()
        messages.success(request, "Profile updated successfully")
        return redirect('/company_profile')

    return render(request, 'company/edit_company_profile.html', {'company': company})


def job_applicants_company(request):
    if 'uid' not in request.session:
        return redirect('/login')

    login_user = Login.objects.get(id=request.session['uid'])
    company = Company.objects.get(loginid=login_user)

    applicants = JobApply.objects.filter(job__company=company)

    return render(request, 'company/job_applicants_company.html', {
        'applicants': applicants
    })
def add_job_feedback(request, job_id):
    if 'uid' not in request.session:
        return redirect('/login')

    login_user = Login.objects.get(id=request.session['uid'])
    client = Client.objects.get(loginid=login_user)
    job = Job.objects.get(id=job_id)
    company = job.company

    applied = JobApply.objects.filter(job=job, client=client).exists()
    if not applied:
        messages.warning(request, "Apply for job before giving feedback")
        return redirect('/client_view_jobs')

    if request.method == "POST":
        feedback_text = request.POST.get('feedback')
        rating = request.POST.get('rating')

        JobFeedback.objects.create(
            job=job,
            company=company,
            client=client,
            rating=rating,
            feedback=feedback_text
        )

        messages.success(request, "Feedback submitted successfully")
        return redirect('/client_view_jobs')

    return render(request, 'client/add_job_feedback.html', {
        'job': job,
        'company': company
    })


def admin_view_feedback(request):
    if 'uid' not in request.session:
        return redirect('/login')

    feedbacks = JobFeedback.objects.all().order_by('-created_at')

    return render(request, 'adminpg/admin_view_feedback.html', {
        'feedbacks': feedbacks
    })


def company_view_feedback(request):
    if 'uid' not in request.session:
        return redirect('/login')

    login_user = Login.objects.get(id=request.session['uid'])
    company = Company.objects.get(loginid=login_user)

    feedbacks = JobFeedback.objects.filter(company=company).order_by('-created_at')

    return render(request, 'company/company_view_feedback.html', {
        'feedbacks': feedbacks
    })


def view_tutors(request):
    tutors = Tutor.objects.select_related('loginid').all()
    return render(request, 'adminpg/view_tutors.html', {'tutors': tutors})

def approve_tutor(request, tid):
    tutor = Tutor.objects.get(id=tid)
    login = tutor.loginid

    if login:
        login.is_active = 1
        login.save()

    messages.success(request, "Tutor approved successfully")
    return redirect('view_tutors')


def reject_tutor(request, tid):
    tutor = Tutor.objects.get(id=tid)
    login = tutor.loginid

    if tutor:
        tutor.delete()

    if login:
        login.delete()

    messages.success(request, "Tutor deleted successfully")
    return redirect('view_tutors')


def tutorhome(request):
    clients = Client.objects.all()
    return render(request, "tutor/tutorhome.html", {"clients": clients})


def tutor_profile(request):
    if 'uid' not in request.session:
        return redirect('/login')

    login = Login.objects.get(id=request.session['uid'])
    tutor = Tutor.objects.get(loginid=login)

    return render(request, 'tutor/tutor_profile.html', {'tutor': tutor})


def edit_tutor_profile(request):
    if 'uid' not in request.session:
        return redirect('/login')

    login = Login.objects.get(id=request.session['uid'])
    tutor = Tutor.objects.get(loginid=login)

    if request.method == "POST":
        tutor.name = request.POST['name']
        tutor.phone = request.POST['phone']
        tutor.address = request.POST['address']
        tutor.qualification = request.POST['qualification']

        if request.FILES.get('img'):
            tutor.img = request.FILES.get('img')

        tutor.save()
        messages.success(request, "Profile updated successfully")
        return redirect('/tutor_profile')

    return render(request, 'tutor/edit_tutor_profile.html', {'tutor': tutor})



def tutor_view_courses(request):
    if 'uid' not in request.session:
        return redirect('/login')

    tutor = Tutor.objects.get(loginid_id=request.session['uid'])
    courses = Course.objects.filter(tutor=tutor)

    return render(request, 'tutor/tutor_view_courses.html', {'courses': courses})


def tutor_edit_course(request, cid):
    if 'uid' not in request.session:
        return redirect('/login')

    course = Course.objects.get(id=cid)

    if request.method == 'POST':
        course.name = request.POST['name']
        course.description = request.POST['description']
        course.duration = request.POST['duration']
        course.fees = request.POST['fees']

        if request.FILES.get('img'):
            course.img = request.FILES['img']

        course.status = 'pending'  
        course.save()

        messages.success(request, "Course updated & sent for approval")
        return redirect('/tutor_view_courses')

    return render(request, 'tutor/tutor_edit_course.html', {'course': course})


def tutor_delete_course(request, cid):
    if 'uid' not in request.session:
        return redirect('/login')

    Course.objects.filter(id=cid).delete()
    messages.success(request, "Course deleted")
    return redirect('/tutor_view_courses')
    


def admin_view_courses(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'adminpg/admin_view_courses.html', {'courses': courses})


def approve_course(request, id):
    Course.objects.filter(id=id).update(status='approved')
    return redirect('/admin_view_courses')

def reject_course(request, id):
    Course.objects.filter(id=id).update(status='rejected')
    return redirect('/admin_view_courses')

from django.shortcuts import redirect
from django.db.models import Q

def chat(request):
    uid = request.session["uid"]
    tutor_id = request.GET.get("id")

    tutors = Tutor.objects.all()   # 👈 list of tutors

    chats = []
    selected_tutor = None

    if tutor_id:
        selected_tutor = Tutor.objects.get(id=tutor_id)
        tutor_login = selected_tutor.loginid

        chats = Chat.objects.filter(
            Q(sender_id=uid, receiver=tutor_login) |
            Q(sender=tutor_login, receiver_id=uid)
        ).order_by("id")

        if request.method == "POST":
            msg = request.POST["message"]

            Chat.objects.create(
                sender_id=uid,
                receiver=tutor_login,
                message=msg
            )

    return render(request, "client/chat.html", {
        "tutors": tutors,
        "chats": chats,
        "selected_tutor": selected_tutor
    })



def reply(request):
    uid = request.session["uid"]
    client_id = request.GET.get("id")

    clients = Client.objects.all()

    chats = []
    selected_client = None

    if client_id:
        selected_client = Client.objects.get(id=client_id)
        client_login = selected_client.loginid

        chats = Chat.objects.filter(
            Q(sender_id=uid, receiver=client_login) |
            Q(sender=client_login, receiver_id=uid)
        ).order_by("id")

        if request.method == "POST":
            msg = request.POST["message"]

            Chat.objects.create(
                sender_id=uid,
                receiver=client_login,
                message=msg
            )

    return render(request, "tutor/reply.html", {
        "clients": clients,
        "chats": chats,
        "selected_client": selected_client
    })

from django.db.models import Q

def chat_company(request):
    uid = request.session["uid"]
    company_id = request.GET.get("id")

    companies = Company.objects.all()

    chats = []
    selected_company = None

    if company_id:
        selected_company = Company.objects.get(id=company_id)
        company_login = selected_company.loginid

        chats = Chat.objects.filter(
            Q(sender_id=uid, receiver=company_login) |
            Q(sender=company_login, receiver_id=uid)
        ).order_by("id")

        if request.method == "POST":
            msg = request.POST["message"]

            Chat.objects.create(
                sender_id=uid,
                receiver=company_login,
                message=msg
            )

    return render(request, "client/chat_company.html", {
        "companies": companies,
        "chats": chats,
        "selected_company": selected_company
    })

def reply_company(request):
    uid = request.session["uid"]
    client_id = request.GET.get("id")

    clients = Client.objects.all()

    chats = []
    selected_client = None

    if client_id:
        selected_client = Client.objects.get(id=client_id)
        client_login = selected_client.loginid

        chats = Chat.objects.filter(
            Q(sender_id=uid, receiver=client_login) |
            Q(sender=client_login, receiver_id=uid)
        ).order_by("id")

        if request.method == "POST":
            msg = request.POST["message"]

            Chat.objects.create(
                sender_id=uid,
                receiver=client_login,
                message=msg
            )

    return render(request, "company/reply_company.html", {
        "clients": clients,
        "chats": chats,
        "selected_client": selected_client
    })


def admin_job_applicants(request):
    applications = JobApply.objects.select_related('job', 'client').all()
    return render(request, 'adminpg/job_applicants.html', {'applications': applications})

def admin_course_enrollments(request):
    enrollments = Enrollment.objects.select_related('client', 'course').all()
    notes = Notes.objects.select_related('course').all()
    return render(request, 'adminpg/admin_course_enrollments.html', {
        'enrollments': enrollments,
        'notes': notes
    })