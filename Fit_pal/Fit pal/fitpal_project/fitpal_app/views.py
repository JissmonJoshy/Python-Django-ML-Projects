from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
import re

def index(request):
    return render(request, 'index.html')

def sign_up(request):
    return render(request, 'sign_up.html')

def sign_in(request):
    return render(request, 'sign_in.html')

def admin_dashboard(request):
    return render(request, 'Admin/admin_dashboard.html')

def user_dashboard(request):
    return render(request, 'User/user_dashboard.html')

def expert_dashboard(request):
    return render(request, 'Expert/expert_dashboard.html')

def dietician_dashboard(request):
    return render(request, 'Dietician/dietician_dashboard.html')


# def admin(request):
#     adm=Login.objects.create_superuser(username='admin',email='admin@gmail.com',viewpassword='1234',password='1234',usertype='Admin')
#     adm.save()
#     return redirect('/')


def view_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usertype = request.POST['usertype']  # ✅ get dropdown value
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            
            if user.usertype == usertype:  # ✅ match selected usertype
                if usertype == "Admin":
                    messages.info(request, "Admin login success")
                    return redirect('admin_dashboard')
                elif usertype == "User":
                    request.session['uid'] = user.id
                    messages.info(request, "User login success")
                    return redirect('/user_dashboard')
                elif usertype == "Expert":
                    request.session['uid'] = user.id
                    messages.info(request, "Expert login success")
                    return redirect('/expert_dashboard')
                elif usertype == "Dietician":
                    request.session['uid'] = user.id
                    messages.info(request, "Dietician login success")
                    return redirect('/dietician_dashboard')
            else: 
                messages.error(request, "Invalid user type selected.")
                return render(request, 'sign_in.html')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'sign_in.html')

    return render(request, 'sign_in.html')



def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']

        # -------------------------
        # EMAIL VALIDATION (only Gmail .com or .in)
        # -------------------------
        email_pattern = r'^[A-Za-z0-9._%+-]+@gmail\.(com|in)$'
        if not re.match(email_pattern, email):
            messages.error(request, "Email must be Gmail ending with .com or .in only")
            return redirect('sign_up')

        # -------------------------
        # CHECK USERNAME EXISTS
        # -------------------------
        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already taken, please choose another")
            return redirect('sign_up')

        # -------------------------
        # CHECK EMAIL EXISTS
        # -------------------------
        if Login.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('sign_up')

        # -------------------------
        # CREATE USER
        # -------------------------
        otp = get_random_string(length=6, allowed_chars='1234567890')
        
        user = Login.objects.create_user(
            username=username,
            first_name=fname,
            last_name=lname,
            email=email,
            password='temporary',
            usertype='User',
        )

        UserDetail.objects.create(
            user=user,
            fullname=fname + ' ' + lname,
            phone=phone,
            address=address,
            otp=otp,
        )

        # MAIL
        subject = "Your OTP for FitPal Registration"
        message = f"Hello {fname}, your OTP is: {otp}"
        send_mail(subject, message, 'jissjoshy3@gmail.com', [email])

        request.session['username'] = username
        return redirect('verify_otp')
    
    return render(request, 'sign_in.html')


from django.http import HttpResponse

def verify_otp(request):
    username = request.session.get('username')
    print("Session username:", username)

    if not username:
        return redirect('register')

    user = Login.objects.get(username=username)
    user_detail = UserDetail.objects.get(user=user)

    if request.method == 'POST':
        otp_entered = request.POST['otp']
        print("OTP Entered:", otp_entered)
        print("OTP Stored:", user_detail.otp)

        if otp_entered == user_detail.otp:
            generated_password = get_random_string(length=8)
            user.set_password(generated_password)
            user.save()
            user.viewpassword = generated_password
            user.save()

            user_detail.is_verified = True
            user_detail.save()

            send_mail(
                "Your FitPal Password",
                f"Hello {user.first_name}, your password is: {generated_password}",
                'jissjoshy3@gmail.com',
                [user.email]
            )

            print("OTP verified. Password sent to email.")
            return redirect('sign_in')
        else:
            print("OTP mismatch.")
            return render(request, 'otp.html', {'error': 'Invalid OTP'})
    
    return render(request, 'otp.html')



import re
from django.contrib import messages
from django.utils.crypto import get_random_string

def expert_sign_up(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']

        gmail_regex = r'^[A-Za-z0-9._%+-]+@gmail\.(com|in)$'

        # Email validation
        if not re.match(gmail_regex, email):
            messages.error(request, "Email must be a Gmail address ending with .com or .in")
            return redirect('expert_sign_up')

        # Check username exists
        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('expert_sign_up')

        # Check email exists
        if Login.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('expert_sign_up')

        # Generate random password
        generated_password = get_random_string(length=8)

        # Create expert account
        user = Login.objects.create_user(
            username=username,
            first_name=fname,
            last_name=lname,
            email=email,
            password=generated_password,
            usertype='Expert',
            is_active=False,
        )
        user.viewpassword = generated_password
        user.save()

        # Save expert details
        ExpertDetail.objects.create(
            user=user,
            fullname=f"{fname} {lname}",
            phone=phone,
            address=address,
            status='Pending',
        )

        # Send mail
        send_mail(
            "Your Expert Account Password",
            f"Hello {fname},\n\nYour password is: {generated_password}\n\nYou can now log in using this password.",
            'jissjoshy3@gmail.com',
            [email],
            fail_silently=False,
        )

        messages.success(request, "Expert registered successfully! Check your email for password.")
        return redirect('sign_in')

    return render(request, 'expert_sign_up.html')

def dietician_sign_up(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']

        gmail_regex = r'^[A-Za-z0-9._%+-]+@gmail\.(com|in)$'

        # Gmail validation
        if not re.match(gmail_regex, email):
            messages.error(request, "Only Gmail (.com or .in) allowed")
            return redirect('dietician_sign_up')

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('dietician_sign_up')

        if Login.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('dietician_sign_up')

        password = get_random_string(8)

        user = Login.objects.create_user(
            username=username,
            first_name=fname,
            last_name=lname,
            email=email,
            password=password,
            usertype='Dietician',
            is_active=False
        )
        user.viewpassword = password
        user.save()

        DieticianDetail.objects.create(
            user=user,
            fullname=f"{fname} {lname}",
            phone=phone,
            address=address,
            status='Pending'
        )

        send_mail(
            "Dietician Account Created",
            f"Hello {fname},\nYour password is: {password}",
            'jissjoshy3@gmail.com',
            [email],
            fail_silently=False
        )

        messages.success(request, "Dietician registered successfully. Check email.")
        return redirect('sign_in')

    return render(request, 'dietician_sign_up.html')


def view_users(request):
    users = UserDetail.objects.all()
    return render(request, 'Admin/view_users.html', {'users': users})

def view_experts(request):
    experts = ExpertDetail.objects.all()
    return render(request, 'Admin/view_experts.html', {'experts': experts})


def accept_expert(request, expert_id):
    expert = get_object_or_404(ExpertDetail, id=expert_id)
    expert.status = 'Accept'
    expert.save()

    expert.user.is_active = True
    expert.user.save()

    return redirect('view_experts')

def reject_expert(request, expert_id):
    expert = get_object_or_404(ExpertDetail, id=expert_id)
    expert.status = 'Reject'
    expert.save()

    expert.user.is_active = False
    expert.user.save()

    return redirect('view_experts')


def expert_profile(request):
    expert = ExpertDetail.objects.get(user=request.user)
    return render(request, 'Expert/expert_profile.html', {'expert': expert})


def upload_image_plan(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES['image']
        FitnessPlanImage.objects.create(
            expert=request.user,
            title=title,
            description=description,
            image=image
        )
        return redirect('upload_image_plan')
    return render(request, 'Expert/upload_image_plan.html')


def upload_video_plan(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        video = request.FILES['video']
        FitnessPlanVideo.objects.create(
            expert=request.user,
            title=title,
            description=description,
            video=video
        )
        return redirect('upload_video_plan')
    return render(request, 'Expert/upload_video_plan.html')

def view_image_plans(request):
    image_plans = FitnessPlanImage.objects.all()
    return render(request, 'Expert/view_image_plans.html', {'image_plans': image_plans})

def view_video_plans(request):
    video_plans = FitnessPlanVideo.objects.all()
    return render(request, 'Expert/view_video_plans.html', {'video_plans': video_plans})


def edit_image_plan(request, plan_id):
    plan = get_object_or_404(FitnessPlanImage, id=plan_id, expert=request.user)

    if request.method == "POST":
        plan.title = request.POST["title"]
        plan.description = request.POST["description"]
        if "image" in request.FILES:
            plan.image = request.FILES["image"]
        plan.save()
        return redirect("view_image_plans")

    return render(request, "Expert/edit_image_plans.html", {"plan": plan})

def delete_image_plan(request, plan_id):
    plan = get_object_or_404(FitnessPlanImage, id=plan_id, expert=request.user)
    plan.delete()
    return redirect("view_image_plans")


def edit_video_plan(request, plan_id):
    plan = get_object_or_404(FitnessPlanVideo, id=plan_id, expert=request.user)

    if request.method == "POST":
        plan.title = request.POST["title"]
        plan.description = request.POST["description"]
        if "video" in request.FILES:
            plan.video = request.FILES["video"]
        plan.save()
        return redirect("view_video_plans")

    return render(request, "Expert/edit_video_plans.html", {"plan": plan})


def delete_video_plan(request, plan_id):
    plan = get_object_or_404(FitnessPlanVideo, id=plan_id, expert=request.user)
    plan.delete()
    return redirect("view_video_plans")


def user_profile(request):
    user_detail = UserDetail.objects.get(user=request.user)
    return render(request, 'User/user_profile.html', {'user_detail': user_detail})


def image_plans(request):
    plans = FitnessPlanImage.objects.select_related('expert').order_by('-uploaded_at')
    return render(request, 'User/image_plans.html', {'plans': plans})

def video_plans(request):
    plans = FitnessPlanVideo.objects.select_related('expert').order_by('-uploaded_at')
    return render(request, 'User/video_plans.html', {'plans': plans})


def all_experts(request):
    experts = ExpertDetail.objects.filter(user__usertype='Expert', user__is_active=True)
    return render(request, 'User/all_experts.html', {'experts': experts})


from django.shortcuts import render, redirect
from .models import DietProgram, DietStep, Login

def add_diet_program(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        expert_id = request.user.id  

        program = DietProgram.objects.create(
            expert_id=expert_id,
            title=title,
            description=description
        )

        steps = request.POST.getlist("steps[]")
        for i, step in enumerate(steps, start=1):
            DietStep.objects.create(program=program, step_number=i, instruction=step)

        return redirect("view_diet_programs")

    return render(request, "Expert/add_diet_program.html")


def view_diet_programs(request):
    # Only fetch diet programs of the logged-in expert
    programs = DietProgram.objects.filter(expert=request.user).prefetch_related("steps")
    return render(request, "Expert/view_diet_programs.html", {"programs": programs})


def complete_step(request, progress_id):
    progress = get_object_or_404(UserStepProgress, id=progress_id, user_program__user=request.user)
    progress.is_completed = True
    progress.completed_at = timezone.now()
    progress.save()
    return redirect("my_diet_programs")
################################################# 909
def add_health_metrics(request):
    if request.method == "POST":
        weight = request.POST.get("weight")
        height = request.POST.get("height")
        notes = request.POST.get("notes")

        bmi = None
        if weight and height:
            bmi = round(float(weight) / ((float(height)/100) ** 2), 2)

        HealthMetric.objects.create(
            user=request.user,
            weight=weight,
            height=height,
            bmi=bmi,
            notes=notes
        )
        return redirect("my_health_metrics")

    return render(request, "User/add_health_metrics.html")

def my_health_metrics(request):
    metrics = HealthMetric.objects.filter(user=request.user).order_by("-recorded_at")
    return render(request, "User/my_health_metrics.html", {"metrics": metrics})

############################# 909

def user_view_diet_programs(request):
    programs = DietProgram.objects.all().prefetch_related("steps")
    return render(request, "User/view_user_diet_programs.html", {"programs": programs})

def join_diet_program(request, program_id):
    program = get_object_or_404(DietProgram, id=program_id)
    user = request.user

    # Check if user already joined
    user_program, created = UserDietProgram.objects.get_or_create(user=user, program=program)

    # Add steps if first time
    if created:
        for step in program.steps.all():
            UserStepProgress.objects.create(user_program=user_program, step=step)

    return redirect("my_diet_programs")

# Show programs joined by the user
def my_diet_programs(request):
    user_programs = UserDietProgram.objects.filter(user=request.user).select_related("program")

    # Add a property to check completion
    for up in user_programs:
        steps = up.userstepprogress_set.all()
        up.all_completed = all(step.is_completed for step in steps) if steps.exists() else False

    return render(request, "User/my_diet_programs.html", {"user_programs": user_programs})


from django.db.models import Count, F, Q

def joined_users(request):
    # Get all user enrollments for programs created by this expert
    user_programs = UserDietProgram.objects.filter(program__expert=request.user).select_related("user", "program")

    # Attach progress count (completed vs total steps)
    for up in user_programs:
        total_steps = up.program.steps.count()
        completed_steps = up.userstepprogress_set.filter(is_completed=True).count()
        up.progress_percent = int((completed_steps / total_steps) * 100) if total_steps > 0 else 0

    return render(request, "Expert/joined_users.html", {"user_programs": user_programs})


# CUSTOMER = sender = reply(UserDetail)
# SELLER = reciever = chat(ExpertDetail)
from datetime import date as date, datetime as dt
from django.db.models import Q, Min, Max

def chat(request):
    uid = request.session["uid"]
    name = ""
    artistData = UserDetail.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(sellerid__user=uid) & Q(customerid=id))
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    userid = ExpertDetail.objects.get(user=uid)
    if id:
        customerid = UserDetail.objects.get(id=id)
        name = customerid.fullname
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            sellerid=userid, message=message, customerid=customerid, time=formatted_time, utype="SELLER")
        sendMsg.save()
    return render(request, "Expert/RECIEVER.html", {"artistData": artistData, "getChatData": getChatData, "customerid": name, "id": id})


def reply(request):
    uid = request.session["uid"]
    name = ""
    userData = ExpertDetail.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(customerid__user=uid) & Q(sellerid=id))
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    customerid = UserDetail.objects.get(user=uid)
    if id:
        userid = ExpertDetail.objects.get(id=id)
        name = userid.fullname
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            sellerid=userid, message=message, customerid=customerid, time=formatted_time, utype="CUSTOMER")
        sendMsg.save()
    return render(request, "User/SENDER.html", {"userData": userData, "getChatData": getChatData, "userid": name, "id": id})


def view_videos_images(request):
    images = FitnessPlanImage.objects.all()
    videos = FitnessPlanVideo.objects.all()
    return render(request, "Admin/view_videos_images.html", {"images": images, "videos": videos})

def admin_view_programs(request):
    programs = DietProgram.objects.all().prefetch_related('steps')
    return render(request, 'Admin/admin_view_programs.html', {'programs': programs})

def diet_feedback(request, program_id):
    program = get_object_or_404(DietProgram, id=program_id)

    if request.method == "POST":
        feedback_text = request.POST.get("feedback")
        DietFeedback.objects.create(
            user=request.user,
            program=program,
            feedback=feedback_text
        )
        messages.success(request, "Your feedback has been added successfully!")
        return redirect("my_diet_programs")

    return render(request, "User/diet_feedback.html", {"program": program})


def all_diet_feedbacks(request):
    feedbacks = DietFeedback.objects.select_related('program', 'user').all()
    return render(request, "Admin/all_diet_feedbacks.html", {"feedbacks": feedbacks})
import pickle
import numpy as np
import time
import os
import pickle
from django.shortcuts import render

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ml_path = os.path.join(BASE_DIR, 'fitpal_app', 'ml')

model = pickle.load(open(os.path.join(ml_path, 'workout_model.pkl'), 'rb'))
gender_encoder = pickle.load(open(os.path.join(ml_path, 'gender_encoder.pkl'), 'rb'))
workout_encoder = pickle.load(open(os.path.join(ml_path, 'workout_encoder.pkl'), 'rb'))
exercise_plan_mapping = pickle.load(open(os.path.join(ml_path,'exercise_plan_mapping.pkl'),'rb'))

def workout_recommendation(request):
    recommendation = None
    exercise_steps = None

    if request.method == 'POST':
        age = int(request.POST['age'])
        gender = request.POST['gender']
        weight = float(request.POST['weight'])
        height = float(request.POST['height'])
        bmi = float(request.POST['bmi'])
        fat = float(request.POST['fat'])
        frequency = int(request.POST['frequency'])
        experience = int(request.POST['experience'])

        # Encode gender
        gender_encoded = gender_encoder.transform([gender])[0]

        features = np.array([[
            age,
            gender_encoded,
            weight,
            height,
            bmi,
            fat,
            frequency,
            experience
        ]])

        # Optional: simulate processing delay
        time.sleep(3)

        prediction = model.predict(features)[0]
        recommendation = workout_encoder.inverse_transform([prediction])[0]

        # Fetch exercise steps
        exercise_steps = exercise_plan_mapping[prediction]

    return render(request, 'User/workout_recommend.html', {
        'recommendation': recommendation,
        'exercise_steps': exercise_steps
    })

###############DIETICIAN ####################

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DieticianDetail, Login

def view_dietician(request):
    dieticians = DieticianDetail.objects.all()
    return render(request, 'Admin/view_dietician.html', {
        'dieticians': dieticians
    })


def approve_dietician(request, id):
    dietician = DieticianDetail.objects.get(id=id)

    dietician.status = "Approved"
    dietician.save()

    user = dietician.user
    user.is_active = True
    user.save()

    messages.success(request, "Dietician approved successfully")
    return redirect('view_dietician')


def reject_dietician(request, id):
    dietician = DieticianDetail.objects.get(id=id)

    user = dietician.user
    dietician.delete()
    user.delete()

    messages.error(request, "Dietician rejected and removed")
    return redirect('view_dietician')

def dietician_profile(request):
    uid = request.session.get('uid')
    dietician = DieticianDetail.objects.get(user_id=uid)

    return render(request, 'Dietician/dietician_profile.html', {
        'dietician': dietician
    })


def edit_dietician_profile(request):
    uid = request.session.get('uid')
    dietician = DieticianDetail.objects.get(user_id=uid)

    if request.method == 'POST':
        dietician.fullname = request.POST['fullname']
        dietician.phone = request.POST['phone']
        dietician.address = request.POST['address']
        dietician.save()

        messages.success(request, "Profile updated successfully")
        return redirect('dietician_profile')

    return render(request, 'Dietician/edit_dietician_profile.html', {
        'dietician': dietician
    })


def add_diet_plan(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES['image']

        plan = NutritionPlan.objects.create(
            dietician_id=request.session['uid'],
            title=title,
            description=description,
            image=image
        )

        step_titles = request.POST.getlist('step_title')
        step_descriptions = request.POST.getlist('step_description')
        step_images = request.FILES.getlist('step_image')

        for i in range(len(step_titles)):
            NutritionStep.objects.create(
                plan=plan,
                step_title=step_titles[i],
                step_description=step_descriptions[i],
                step_image=step_images[i] if i < len(step_images) else None
            )

        return redirect('view_diet_plans')

    return render(request, 'Dietician/add_diet_plans.html')


def view_diet_plans(request):
    plans = NutritionPlan.objects.filter(dietician_id=request.session['uid'])
    return render(request, 'Dietician/view_diet_plans.html', {'plans': plans})


def edit_diet_plan(request, id):
    plan = NutritionPlan.objects.get(id=id)
    steps = NutritionStep.objects.filter(plan=plan)

    if request.method == 'POST':
        plan.title = request.POST['title']
        plan.description = request.POST['description']

        if 'image' in request.FILES:
            plan.image = request.FILES['image']

        plan.save()

        step_ids = request.POST.getlist('step_id')
        step_titles = request.POST.getlist('step_title')
        step_descriptions = request.POST.getlist('step_description')
        step_images = request.FILES.getlist('step_image')

        image_index = 0

        for i in range(len(step_titles)):
            if step_ids[i] != "new":
                step = NutritionStep.objects.get(id=step_ids[i])
                step.step_title = step_titles[i]
                step.step_description = step_descriptions[i]

                if image_index < len(step_images):
                    step.step_image = step_images[image_index]
                    image_index += 1

                step.save()
            else:
                NutritionStep.objects.create(
                    plan=plan,
                    step_title=step_titles[i],
                    step_description=step_descriptions[i],
                    step_image=step_images[image_index] if image_index < len(step_images) else None
                )
                image_index += 1

        return redirect('view_diet_plans')

    return render(request, 'Dietician/edit_diet_plans.html', {
        'plan': plan,
        'steps': steps
    })



def delete_diet_plan(request, id):
    NutritionPlan.objects.filter(id=id).delete()
    return redirect('view_diet_plans')



def user_nutrition_plans(request):
    uid = request.session.get('uid')
    user = Login.objects.get(id=uid)

    plans = NutritionPlan.objects.select_related('dietician')

    joined_plans = NutritionJoinRequest.objects.filter(user=user)\
                     .values_list('plan_id', flat=True)

    return render(request, 'User/nutrition_plans.html', {
        'plans': plans,
        'joined_plans': joined_plans
    })


def join_nutrition_plan(request, plan_id):
    uid = request.session.get('uid')
    user = Login.objects.get(id=uid)
    plan = NutritionPlan.objects.get(id=plan_id)

    already_requested = NutritionJoinRequest.objects.filter(
        user=user,
        plan=plan
    ).exists()

    if already_requested:
        messages.warning(request, "You have already requested this plan.")
    else:
        NutritionJoinRequest.objects.create(
            user=user,
            plan=plan
        )
        messages.success(request, "Join request sent successfully.")

    return redirect('user_nutrition_plans')


from django.db.models import Count

from django.db.models import Count
from django.shortcuts import render

def dietician_join_requests(request):
    did = request.session.get('uid')

    requests = NutritionJoinRequest.objects.filter(
        plan__dietician_id=did
    ).select_related('user', 'plan')

    for req in requests:
        total_steps = NutritionStep.objects.filter(
            plan=req.plan
        ).count()

        completed_steps = StepCompletion.objects.filter(
            user=req.user,
            step__plan=req.plan,
            is_completed=True
        ).count()

        if total_steps > 0:
            percentage = int((completed_steps / total_steps) * 100)
        else:
            percentage = 0

        # 🔥 Attach directly to request object
        req.total_steps = total_steps
        req.completed_steps = completed_steps
        req.progress_percentage = percentage

    return render(request, 'Dietician/dietician_join_requests.html', {
        'requests': requests
    })


def update_join_request_status(request, req_id, status):
    join_req = NutritionJoinRequest.objects.get(id=req_id)
    join_req.status = status
    join_req.save()

    messages.success(request, f"Request {status.lower()} successfully.")
    return redirect('dietician_join_requests')


def user_approved_plans(request):
    uid = request.session.get('uid')
    user = Login.objects.get(id=uid)

    approved_requests = NutritionJoinRequest.objects.filter(
        user=user,
        status='Approved'
    ).select_related('plan')

    return render(request, 'User/user_approved_plans.html', {
        'approved_requests': approved_requests
    })


def user_plan_detail(request, plan_id):
    uid = request.session.get('uid')
    user = Login.objects.get(id=uid)

    plan = NutritionPlan.objects.get(id=plan_id)
    steps = NutritionStep.objects.filter(plan=plan)

    completed_steps = StepCompletion.objects.filter(
        user=user,
        is_completed=True,
        step__plan=plan
    ).values_list('step_id', flat=True)

    total_steps = steps.count()
    completed_count = len(completed_steps)

    all_completed = total_steps == completed_count and total_steps > 0

    feedback_given = PlanFeedback.objects.filter(
        user=user,
        plan=plan
    ).exists()

    if request.method == 'POST' and all_completed and not feedback_given:
        rating = request.POST['rating']
        comment = request.POST['comment']

        PlanFeedback.objects.create(
            user=user,
            plan=plan,
            rating=rating,
            comment=comment
        )

        return redirect('user_plan_detail', plan_id=plan.id)

    return render(request, 'User/plan_detail.html', {
        'plan': plan,
        'steps': steps,
        'completed_steps': completed_steps,
        'all_completed': all_completed,
        'feedback_given': feedback_given
    })


def toggle_step_completion(request, step_id):
    uid = request.session.get('uid')
    user = Login.objects.get(id=uid)
    step = NutritionStep.objects.get(id=step_id)

    completion, created = StepCompletion.objects.get_or_create(
        user=user,
        step=step
    )

    if not completion.is_completed:
        completion.is_completed = True
        completion.save()

    return redirect('user_plan_detail', plan_id=step.plan.id)


def display_dieticians(request):
    dieticians = DieticianDetail.objects.filter(
        user__is_active=True,
        status='Approved'
    )
    return render(request, 'User/display_dieticians.html', {'dieticians': dieticians})



from datetime import datetime as dt
from django.db.models import Q

def dietician_chat(request):
    uid = request.session['uid']
    dietician = DieticianDetail.objects.get(user=uid)

    users = UserDetail.objects.all()
    id = request.GET.get('id')

    chat_data = []
    name = ""

    if id:
        user = UserDetail.objects.get(id=id)
        name = user.fullname

        chat_data = DieticianChat.objects.filter(
            Q(dietician=dietician) & Q(user=user)
        )

    if request.POST:
        message = request.POST['message']
        current_time = dt.now().strftime("%H:%M")

        DieticianChat.objects.create(
            dietician=dietician,
            user=user,
            message=message,
            time=current_time,
            utype="DIETICIAN"
        )

    return render(request, "Dietician/CHAT_RECEIVER.html", {
        "users": users,
        "chat_data": chat_data,
        "username": name,
        "id": id
    })


def user_dietician_chat(request):
    uid = request.session['uid']
    user = UserDetail.objects.get(user=uid)

    dieticians = DieticianDetail.objects.filter(status="Approved")
    id = request.GET.get('id')

    chat_data = []
    name = ""

    if id:
        dietician = DieticianDetail.objects.get(id=id)
        name = dietician.fullname

        chat_data = DieticianChat.objects.filter(
            Q(user=user) & Q(dietician=dietician)
        )

    if request.POST:
        message = request.POST['message']
        current_time = dt.now().strftime("%H:%M")

        DieticianChat.objects.create(
            dietician=dietician,
            user=user,
            message=message,
            time=current_time,
            utype="USER"
        )

    return render(request, "User/CHAT_SENDER.html", {
        "dieticians": dieticians,
        "chat_data": chat_data,
        "dietician_name": name,
        "id": id
    })


def all_nutrition_feedback(request):
    feedbacks = PlanFeedback.objects.select_related(
        'user', 'plan', 'plan__dietician'
    ).order_by('-created_at')

    return render(request, 'Admin/all_nutrition_feedback.html', {
        'feedbacks': feedbacks
    })



def admin_nutrition_plans(request):
    plans = NutritionPlan.objects.prefetch_related('nutritionstep_set').order_by('-created_at')

    return render(request, 'Admin/admin_nutrition_plans.html', {
        'plans': plans
    })


def ChatBot(request):
    import os
    os.system("python chatgui.py")
    print("hello world hiiii")
    return redirect("user_dashboard")
