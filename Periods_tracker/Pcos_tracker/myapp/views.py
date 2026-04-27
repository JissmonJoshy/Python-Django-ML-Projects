
import os

from django.shortcuts import render, redirect
from .models import*
from django.contrib import messages
from django.contrib.auth import authenticate

# Create your views here.


def index(request):
    return render(request,'index.html')


def user_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        cycle_length = request.POST.get('cycle_length')
        period_length = request.POST.get('period_length')
        last_period_date = request.POST.get('last_period_date')
        has_pcos = request.POST.get('has_pcos')

        weight = request.POST.get('weight')
        height = request.POST.get('height')
        image = request.FILES.get('image')

        # Create user
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            user_type='user',
            is_active=True
        )

        # Create period user profile
        User_profile.objects.create(
            user=user,
            name=name,
            age=age,
            phone=phone,
            email=email,
            cycle_length=cycle_length,
            period_length=period_length,
            last_period_date=last_period_date,
            has_pcos=True if has_pcos == 'on' else False,
            weight=weight,
            height=height,
            image=image
        )

        return redirect('/')

    return render(request, 'user_register.html')


def login(request):
    if request.method == "POST":
        usname = request.POST.get("email")
        pasw = request.POST.get("password")
        user = authenticate(username=usname, password=pasw)

        if user is not None:
            if user.is_superuser: 
                messages.success(request, "Login successful as Admin")
                # auth_login(request, user)
                return redirect("/admin_home")

            elif user.user_type == "user" and user.is_active: 
                request.session['uid']=user.id
                messages.success(request, "Login successful as Brand")
                # auth_login(request, user)
                return redirect("/User_home")  
            elif user.user_type == "Doctor" and user.is_active:
                request.session['uid']=user.id
                messages.success(request, "Login successful as Doctor")
                # auth_login(request, user)
                return redirect("/doctor_home")
            else:
                messages.error(request, "Account is not active or does not have the correct role.")
                return redirect("/login")

        else:
            messages.error(request, "Invalid email or password")
            return redirect("/login")
    return render(request,'login.html')






# from django.shortcuts import render, redirect
# from .models import Doctor

# def add_doctor(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         address = request.POST.get('address')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         qualification = request.POST.get('qualification')
#         experience = request.POST.get('experience')
#         specialization = request.POST.get('specialization')
#         password = request.POST.get('password')
#         image = request.FILES.get('image')

#         # Assuming the logged-in user is assigned
#         user = CustomUser.objects.create_user(username=email,password=password,user_type="Doctor")

#         doctor = Doctor.objects.create(
#             name=name,
#             address=address,
#             phone=phone,
#             email=email,
#             qualification=qualification,
#             experience=experience,
#             specialization=specialization,
#             user=user,
#             image=image
#         )
#         doctor.save()
#         return redirect('/admin_home')  # Redirect to doctor list page

#     return render(request, 'adminpage/add_doctor.html')



def add_doctor(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        specialization = request.POST.get('specialization')

        license_number = request.POST.get('license_number')
        license_document = request.FILES.get('license_document')

        password = request.POST.get('password')
        image = request.FILES.get('image')

        user = CustomUser.objects.create_user(
            username=email,
            password=password,
            user_type="Doctor"
        )

        Doctor.objects.create(
            name=name,
            address=address,
            phone=phone,
            email=email,
            qualification=qualification,
            experience=experience,
            specialization=specialization,
            license_number=license_number,
            license_document=license_document,
            image=image,
            user=user
        )

        return redirect('/admin_home')

    return render(request, 'adminpage/add_doctor.html')

def update_doctor(request, did):
    doctor = Doctor.objects.get(id=did)

    if request.method == "POST":
        doctor.name = request.POST.get('name')
        doctor.address = request.POST.get('address')
        doctor.phone = request.POST.get('phone')
        doctor.email = request.POST.get('email')
        doctor.qualification = request.POST.get('qualification')
        doctor.experience = request.POST.get('experience')
        doctor.specialization = request.POST.get('specialization')
        doctor.license_number = request.POST.get('license_number')

        if request.FILES.get('image'):
            doctor.image = request.FILES.get('image')

        if request.FILES.get('license_document'):
            doctor.license_document = request.FILES.get('license_document')

        doctor.save()
        return redirect('/view_doctors')

    return render(request, 'adminpage/update_doctor.html', {'doctor': doctor})



def delete_doctor(request, did):
    doctor = Doctor.objects.get(id=did)

    # delete login account also
    if doctor.user:
        doctor.user.delete()

    doctor.delete()

    return redirect('/view_doctors')


###########ADMIN######################33
def admin_home(request):
    return render(request,'adminpage/admin_home.html')


def admin_view_users(request):
    users = User_profile.objects.all()
    return render(request, 'adminpage/view_users.html', {'users': users})

    
def approve_user(request, uid):
    user = CustomUser.objects.get(id=uid)
    user.is_active = True
    user.save()
    return redirect('/admin_view_users')

def reject_user(request, uid):
    user = CustomUser.objects.get(id=uid)
    user.is_active = False
    user.save()
    return redirect('/admin_view_users')

from django.shortcuts import render, redirect
from .models import DietRemedy

def add_remedies(request):
    # Optional: check admin session
    # if request.session.get('user_type') != 'admin':
    #     return redirect('/login')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')

        DietRemedy.objects.create(
            title=title,
            description=description,
            category=category
        )

        return redirect('/admin_home')

    return render(request,'adminpage/add_remedies.html')




from django.shortcuts import render
from .models import Doctor



def view_doctors(request):
    doctors = Doctor.objects.all()  # Fetch all doctors
    return render(request, 'adminpage/view_doctors.html', {'doctors': doctors})

##############USER#############
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .models import User_profile, PeriodLog


def User_home(request):
    user = request.session['uid']

    profile = User_profile.objects.get(user=user)

    last_period = PeriodLog.objects.filter(user=user).order_by('-start_date').first()

    next_period = None
    if last_period:
        next_period = last_period.start_date + timedelta(days=profile.cycle_length)

    context = {
        'profile': profile,
        'last_period': last_period.start_date if last_period else "Not available",
        'next_period': next_period if next_period else "Prediction unavailable"
    }

    return render(request, 'user/User_home.html', context)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PeriodLog

from .models import User_profile, PeriodLog

# def add_period(request):
#     uid = request.session.get('uid') 


#     user_profile = User_profile.objects.get(user__id=uid)

#     if request.method == 'POST':
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         flow = request.POST.get('flow')

#         PeriodLog.objects.create(
#             user=user_profile,  
#             start_date=start_date,
#             end_date=end_date,
#             flow=flow
#         )

#         return redirect('/User_home')

#     return render(request, 'user/add_period.html')

from datetime import datetime
from django.shortcuts import render, redirect
from .models import User_profile, PeriodLog

def add_period(request):
    uid = request.session.get('uid')
    user_profile = User_profile.objects.get(user__id=uid)

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        flow = request.POST.get('flow')

        # 🔥 Convert string to date (IMPORTANT FIX)
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

        end_date = None
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        PeriodLog.objects.create(
            user=user_profile,
            start_date=start_date,
            end_date=end_date,
            flow=flow
        )

        return redirect('/User_home')

    return render(request, 'user/add_period.html')




from .models import PeriodLog, User_profile

def cycle_history(request):
    uid = request.session.get('uid')
    user_profile = User_profile.objects.get(user__id=uid)

    periods = PeriodLog.objects.filter(user=user_profile).order_by('-start_date')

    return render(request, 'user/cycle_history.html', {'periods': periods})




from .models import DietRemedy

def diet_remedies(request):
    diet = DietRemedy.objects.filter(category='Diet')
    remedies = DietRemedy.objects.filter(category='Remedy')

    return render(request, 'user/diet_remedies.html', {
        'diet': diet,
        'remedies': remedies
    })







from datetime import timedelta, date
from .models import User_profile, PeriodLog

# def next_period_tracker(request):
#     uid = request.session.get('uid')
#     user_profile = User_profile.objects.get(user__id=uid)

#     last_period = PeriodLog.objects.filter(
#         user=user_profile
#     ).order_by('-start_date').first()

#     next_period = None
#     days_left = None

#     if last_period:
#         next_period = last_period.start_date + timedelta(days=user_profile.cycle_length)
#         days_left = (next_period - date.today()).days

#     context = {
#         'profile': user_profile,
#         'last_period': last_period.start_date if last_period else None,
#         'next_period': next_period,
#         'days_left': days_left
#     }

#     return render(request, 'user/next_period.html', context)

from datetime import timedelta, date

def next_period_tracker(request):
    uid = request.session.get('uid')
    user_profile = User_profile.objects.get(user__id=uid)

    # 🔥 Always fetch latest period
    last_period = PeriodLog.objects.filter(
        user=user_profile
    ).order_by('-start_date').first()

    next_period = None
    days_left = None

    if last_period:
        next_period = last_period.start_date + timedelta(days=user_profile.cycle_length)
        days_left = (next_period - date.today()).days

    context = {
        'profile': user_profile,
        'last_period': last_period.start_date if last_period else "No period data",
        'next_period': next_period,
        'days_left': days_left
    }

    return render(request, 'user/next_period.html', context)
# from datetime import timedelta, date
# from .models import User_profile, PeriodLog

# def next_period_tracker(request):
#     uid = request.session.get('uid')
#     user_profile = User_profile.objects.get(user__id=uid)

#     last_period = PeriodLog.objects.filter(
#         user=user_profile
#     ).order_by('-start_date').first()

#     next_period = None
#     days_left = None
#     status = ""

#     if last_period:
#         cycle = user_profile.cycle_length
#         next_period = last_period.start_date + timedelta(days=cycle)

#         today = date.today()

#         # If period didn't come on expected day
#         if today > next_period:
#             next_period = next_period + timedelta(days=cycle)
#             status = "Your cycle seems delayed. New predicted date calculated."

#         days_left = (next_period - today).days

#     context = {
#         'next_period': next_period,
#         'days_left': days_left,
#         'status': status
#     }

#     return render(request, 'user/next_period.html', context)



import joblib
# from datetime import timedelta, date
# from .models import User_profile, PeriodLog, SymptomLog

# def ml_period_analysis(request):
#     uid = request.session.get('uid')
#     profile = User_profile.objects.get(user__id=uid)

#     last_period = PeriodLog.objects.filter(user=profile).order_by('-start_date').first()
#     symptoms = SymptomLog.objects.filter(user=profile).last()

#     # calculate delay
#     expected = last_period.start_date + timedelta(days=profile.cycle_length)
#     delay_days = (date.today() - expected).days

#     # BMI
#     bmi = profile.weight / ((profile.height/100) ** 2)

#     # ML input
#     X = [[
#         profile.age,
#         profile.cycle_length,
#         delay_days,
#         int(symptoms.acne),
#         int(symptoms.hairfall),
#         bmi
#     ]]

#     # load models
#     reason_model = joblib.load('reason_model.pkl')
#     pcos_model = joblib.load('pcos_model.pkl')

#     reason = reason_model.predict(X)[0]
#     pcos_result = pcos_model.predict(X)[0]

#     # next period calculation
#     next_period = expected + timedelta(days=profile.cycle_length)

#     context = {
#         'reason': reason,
#         'next_period': next_period,
#         'pcos': "High Risk" if pcos_result == 1 else "Low Risk"
#     }

# #     return render(request, 'user/ml_result.html', context)

# import joblib
# def ml_period_analysis(request):
#     uid = request.session.get('uid')
#     profile = User_profile.objects.get(user__id=uid)

#     last_period = PeriodLog.objects.filter(user=profile).order_by('-start_date').first()
#     symptoms = SymptomLog.objects.filter(user=profile).last()

#     # Calculate expected date
#     expected_date = last_period.start_date + timedelta(days=profile.cycle_length)
#     delay_days = (date.today() - expected_date).days

#     # BMI calculation (safe)
#     bmi = 0
#     if profile.weight and profile.height:
#         bmi = profile.weight / ((profile.height / 100) ** 2)

#     # Safe symptom values
#     acne = int(symptoms.acne) if symptoms else 0
#     hairfall = int(symptoms.hairfall) if symptoms else 0

#     X = [[
#         profile.age,
#         profile.cycle_length,
#         delay_days,
#         acne,
#         hairfall,
#         bmi
#     ]]

#         import os
#         import joblib

#         model_path = 'reason_model.pkl'

#         if not os.path.exists(model_path):
#             reason_model = None  # prevents crash
#         else:
#             try:
#                 reason_model = joblib.load(model_path)
#             except Exception as e:
#                 print("Model load error:", e)
#                 reason_model = None
#     pcos_model = joblib.load('pcos_model.pkl')

#     reason = reason_model.predict(X)[0]
#     pcos_pred = pcos_model.predict(X)[0]

#     next_period = expected_date + timedelta(days=profile.cycle_length)

#     context = {
#         'reason': reason,
#         'pcos': "High Risk" if pcos_pred == 1 else "Low Risk",
#         'next_period': next_period
#     }

#     return render(request, 'user/ml_result.html', context)



from datetime import timedelta, date
import os
import joblib
from django.shortcuts import render

def ml_period_analysis(request):
    uid = request.session.get('uid')
    profile = User_profile.objects.get(user__id=uid)

    last_period = PeriodLog.objects.filter(user=profile).order_by('-start_date').first()
    symptoms = SymptomLog.objects.filter(user=profile).last()

    # Safety check
    if not last_period:
        return render(request, 'user/ml_result.html', {
            'reason': "No period data found",
            'pcos': "Unknown",
            'next_period': "Add period data"
        })

    # Calculate expected date
    expected_date = last_period.start_date + timedelta(days=profile.cycle_length)
    delay_days = (date.today() - expected_date).days

    # BMI calculation (safe)
    bmi = 0
    if profile.weight and profile.height:
        bmi = profile.weight / ((profile.height / 100) ** 2)

    # Safe symptom values
    acne = int(symptoms.acne) if symptoms else 0
    hairfall = int(symptoms.hairfall) if symptoms else 0
    weight_gain = int(symptoms.weight_gain) if symptoms and hasattr(symptoms, 'weight_gain') else 0

    # ⚠️ MUST match training features EXACTLY
    X = [[
        profile.age,
        profile.cycle_length,
        bmi,
        acne,
        hairfall,
        weight_gain
    ]]

    # Load PCOS model safely
    pcos_model = None
    pcos_model_path = 'pcos_model.pkl'

    if os.path.exists(pcos_model_path):
        try:
            pcos_model = joblib.load(pcos_model_path)
        except Exception as e:
            print("PCOS Model Load Error:", e)

    # REMOVE reason_model (causing crash)
    reason = "Cycle delay due to hormonal variation"

    # Prediction
    if pcos_model:
        try:
            pcos_pred = pcos_model.predict(X)[0]
            pcos_result = "High Risk" if pcos_pred == 1 else "Low Risk"
        except:
            pcos_result = "Prediction Error"
    else:
        pcos_result = "Model not found"

    next_period = expected_date + timedelta(days=profile.cycle_length)

    context = {
        'reason': reason,
        'pcos': pcos_result,
        'next_period': next_period,
        'delay_days': delay_days
    }

    return render(request, 'user/ml_result.html', context)


# import os
# import joblib
# from django.conf import settings
# from datetime import timedelta, date
# from .models import User_profile, PeriodLog, SymptomLog

# def ml_period_analysis(request):
#     uid = request.session.get('uid')
#     profile = User_profile.objects.get(user__id=uid)

#     last_period = PeriodLog.objects.filter(user=profile).order_by('-start_date').first()
#     symptoms = SymptomLog.objects.filter(user=profile).last()

#     if not last_period:
#         return render(request, 'user/ml_result.html', {
#             'error': "No period data available"
#         })

#     # Expected date
#     expected_date = last_period.start_date + timedelta(days=profile.cycle_length)
#     delay_days = (date.today() - expected_date).days

#     # Safe BMI
#     bmi = 0
#     if profile.weight and profile.height:
#         bmi = profile.weight / ((profile.height / 100) ** 2)

#     # Safe symptoms
#     acne = int(symptoms.acne) if symptoms else 0
#     hairfall = int(symptoms.hairfall) if symptoms else 0

#     X = [[
#         profile.age,
#         profile.cycle_length,
#         delay_days,
#         acne,
#         hairfall,
#         bmi
#     ]]

#     # 🔥 CORRECT PATH (based on your screenshot)
#     reason_model_path = os.path.join(settings.BASE_DIR, 'reason_model.pkl')
#     pcos_model_path = os.path.join(settings.BASE_DIR, 'pcos_model.pkl')

#     reason_model = joblib.load(reason_model_path)
#     pcos_model = joblib.load(pcos_model_path)

#     reason = reason_model.predict(X)[0]
#     pcos_pred = pcos_model.predict(X)[0]

#     next_period = expected_date + timedelta(days=profile.cycle_length)

#     context = {
#         'reason': reason,
#         'pcos': "High Risk" if pcos_pred == 1 else "Low Risk",
#         'next_period': next_period
#     }

#     return render(request, 'user/ml_result.html', context)


# import joblib
# import numpy as np

# def predict_pcos(request):
#     if request.method == 'POST':

#         age = int(request.POST['age'])
#         cycle_length = int(request.POST['cycle_length'])
#         delay_days = int(request.POST['delay_days'])
#         acne = 1 if request.POST.get('acne') else 0
#         hairfall = 1 if request.POST.get('hairfall') else 0
#         weight_gain = 1 if request.POST.get('weight_gain') else 0
#         bmi = float(request.POST['bmi'])

#         X = [[age, cycle_length, delay_days, acne, hairfall, weight_gain, bmi]]

#         model = joblib.load('pcos_model.pkl')

#         prediction = model.predict(X)[0]
#         probability = model.predict_proba(X)[0][1] * 100

#         context = {
#             'result': "PCOS Detected" if prediction == 1 else "No PCOS Detected",
#             'chance': round(probability, 2)
#         }

#         return render(request, 'user/pcos_result.html', context)

#     return render(request, 'user/add_symptoms.html')


# import joblib
# import numpy as np
# from django.shortcuts import render

# def predict_pcos(request):
#     if request.method == 'POST':

#         age = int(request.POST['age'])
#         cycle_length = int(request.POST['cycle_length'])

#         # Period irregular? (Yes/No checkbox or dropdown)
#         irregular_periods = int(request.POST['irregular_periods'])

#         acne = 1 if request.POST.get('acne') else 0
#         hairfall = 1 if request.POST.get('hairfall') else 0
#         weight_gain = 1 if request.POST.get('weight_gain') else 0
#         bmi = float(request.POST['bmi'])

#         X = np.array([[age, cycle_length, irregular_periods, acne, hairfall, weight_gain, bmi]])

#         model = joblib.load('pcos_model.pkl')

#         prediction = model.predict(X)[0]
#         probability = model.predict_proba(X)[0][1] * 100

#         # Medical suggestion logic
#         if prediction == 1:
#             advice = "⚠️ You should consult a gynecologist for further medical tests."
#         else:
#             advice = "✅ PCOS risk appears low. Maintain a healthy lifestyle."

#         context = {
#             'result': "PCOS Detected" if prediction == 1 else "No PCOS Detected",
#             'chance': round(probability, 2),
#             'advice': advice
#         }

#         return render(request, 'user/pcos_result.html', context)

#     return render(request, 'user/add_symptoms.html')


import joblib
from django.shortcuts import render

def predict_pcos(request):
    if request.method == 'POST':

        age = int(request.POST['age'])
        cycle_length = int(request.POST['cycle_length'])
        bmi = float(request.POST['bmi'])

        acne = 1 if request.POST.get('acne') else 0
        hairfall = 1 if request.POST.get('hairfall') else 0
        weight_gain = 1 if request.POST.get('weight_gain') else 0

        X = [[age, cycle_length, bmi, acne, hairfall, weight_gain]]

        model = joblib.load('pcos_model.pkl')
        

        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0][1] * 100

        advice = (
            "⚠ Please consult a gynecologist"
            if probability >= 40
            else "✅ Low risk. Maintain healthy lifestyle"
        )

        return render(request, 'user/pcos_result.html', {
            'result': "PCOS Detected" if prediction == 1 else "No PCOS Detected",
            'chance': round(probability, 2),
            'advice': advice
        })

    return render(request, 'user/add_symptoms.html')



from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from datetime import date

def download_pcos_report(request):

    uid = request.session.get('uid')
    profile = User_profile.objects.get(user__id=uid)

    # Example values (you can pass these from session or DB)
    result = request.GET.get('result')
    chance = request.GET.get('chance')
    advice = request.GET.get('advice')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PCOS_Report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("PCOS Diagnosis Report", styles['Title']))
    elements.append(Spacer(1,20))

    elements.append(Paragraph(f"Name: {profile.name}", styles['Normal']))
    elements.append(Paragraph(f"Age: {profile.age}", styles['Normal']))
    elements.append(Paragraph(f"Date: {date.today()}", styles['Normal']))
    elements.append(Spacer(1,20))

    elements.append(Paragraph(f"Result: {result}", styles['Normal']))
    elements.append(Paragraph(f"PCOS Risk Probability: {chance}%", styles['Normal']))
    elements.append(Spacer(1,20))

    elements.append(Paragraph(f"Doctor Advice: {advice}", styles['Normal']))

    elements.append(Spacer(1,30))
    elements.append(Paragraph("This report is generated by the PCOS Prediction System.", styles['Italic']))

    doc.build(elements)

    return response


def user_view_doctors(request):
    doctors = Doctor.objects.all()  # Fetch all doctors
    return render(request, 'user/user_view_doctors.html', {'doctors': doctors})






from .models import Doctor, Appointment, User_profile

# def book_appointment(request, did):
#     uid = request.session.get('uid')
#     user_profile = User_profile.objects.get(user__id=uid)
#     doctor = Doctor.objects.get(id=did)

#     if request.method == 'POST':
#         date = request.POST.get('date')
#         time = request.POST.get('time')
#         reason = request.POST.get('reason')

#         Appointment.objects.create(
#             user=user_profile,
#             doctor=doctor,
#             appointment_date=date,
#             appointment_time=time,
#             reason=reason
#         )

#         return redirect('/user_view_appointments')

#     return render(request, 'user/book_appointment.html', {'doctor': doctor})

def book_appointment(request, did):

    uid = request.session.get('uid')
    user_profile = User_profile.objects.get(user__id=uid)
    doctor = Doctor.objects.get(id=did)

    if request.method == 'POST':

        date = request.POST.get('date')
        time = request.POST.get('time')

        visit_reason = request.POST.get('visit_reason')
        notes = request.POST.get('notes')

        report_file = request.FILES.get('report_file')

        # Combine reason + notes
        full_reason = f"{visit_reason} - {notes}"

        Appointment.objects.create(
            user=user_profile,
            doctor=doctor,
            appointment_date=date,
            appointment_time=time,
            reason=full_reason,
            report_file=report_file
        )

        return redirect('/user_view_appointments')

    return render(request, 'user/book_appointment.html', {'doctor': doctor})




def user_view_appointments(request):
    uid = request.session.get('uid')
    user_profile = User_profile.objects.get(user__id=uid)

    appointments = Appointment.objects.filter(user=user_profile).order_by('-appointment_date')

    return render(request, 'user/user_view_appointments.html', {
        'appointments': appointments
    })


def admin_view_appointments(request):
    appointments = Appointment.objects.all().order_by('-appointment_date')
    return render(request, 'adminpage/view_appointments.html', {
        'appointments': appointments
    })


from .models import Appointment
from django.shortcuts import redirect

def admin_view_appointments(request):
    appointments = Appointment.objects.all().order_by('-appointment_date')
    return render(request, 'adminpage/view_appointments.html', {
        'appointments': appointments
    })


def approve_appointment(request, aid):
    appointment = Appointment.objects.get(id=aid)
    appointment.status = "Approved"
    appointment.save()
    return redirect('/admin_view_appointments')


def reject_appointment(request, aid):
    appointment = Appointment.objects.get(id=aid)
    appointment.status = "Rejected"
    appointment.save()
    return redirect('/admin_view_appointments')






def user_profile(request):
    uid = request.session.get('uid')

    profile = User_profile.objects.get(user__id=uid)

    return render(request, 'user/user_profile.html', {
        'profile': profile
    })



def update_profile(request):
    uid = request.session.get('uid')
    profile = User_profile.objects.get(user__id=uid)

    if request.method == 'POST':
        profile.name = request.POST.get('name')
        profile.age = request.POST.get('age')
        profile.phone = request.POST.get('phone')
        profile.email = request.POST.get('email')
        profile.weight = request.POST.get('weight')
        profile.height = request.POST.get('height')

        if request.FILES.get('image'):
            profile.image = request.FILES.get('image')

        profile.save()

        return redirect('/user_profile')

    return render(request, 'user/update_profile.html', {
        'profile': profile
    })


##############Doctor######


def doctor_home(request):
    return render(request,'doctor/doctor_home.html')



def doctor_profile(request):

    did = request.session.get('uid')

    doctor = Doctor.objects.get(user=did)

    return render(request, 'doctor/doctor_profile.html', {'doctor': doctor})




def doctor_view_appointments(request):

    did = request.session.get('uid')

    doctor = Doctor.objects.get(user=did)

    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request,'doctor/view_appointments.html',{'appointments':appointments})



def doctor_give_advice(request, aid):

    appointment = Appointment.objects.get(id=aid)

    if request.method == "POST":

        home_remedies = request.POST.get('home_remedies')
        diet_plan = request.POST.get('diet_plan')
        doctor_notes = request.POST.get('doctor_notes')

        appointment.home_remedies = home_remedies
        appointment.diet_plan = diet_plan
        appointment.doctor_notes = doctor_notes
        appointment.status = "Completed"

        appointment.save()

        return redirect('/doctor_view_appointments')

    return render(request,'doctor/give_advice.html',{'appointment':appointment})







def user_view_advice(request):

    uid = request.session.get('uid')

    user_profile = User_profile.objects.get(user__id=uid)

    appointments = Appointment.objects.filter(user=user_profile)

    return render(request,'user/view_advice.html',{'appointments':appointments})