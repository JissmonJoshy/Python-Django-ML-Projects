from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
import random
import string
from django.core.mail import send_mail
import os
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Avg
from datetime import datetime

# Create your views here.
def index(request):
    return render(request,'index.html')

def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:

            login(request, user)

            # SESSION
            request.session['login_id'] = user.id

            # ADMIN
            if user.is_superuser:
                messages.success(request, "Admin Login Successfully")
                return redirect('admin_dashboard')

            # MVD USER
            elif user.usertype == 'club_manager':
                messages.success(request, "Club Manager Login Successfully")
                return redirect('club_manager_dashboard')
            
            elif user.usertype == 'scout':
                messages.success(request, "Scout Login Successfully")
                return redirect('scout_dashboard')

            else:
                messages.error(request, "Invalid user type")
                return redirect('login_view')
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('login')
    return render(request, 'login.html')

def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def club_manager_dashboard(request):
    return render(request, 'club_manager/club_manager_dashboard.html')

def scout_dashboard(request):
    return render(request, 'scout/scout_dashboard.html')

def register_club_manager(request):
    if request.method=="POST":

        club_name=request.POST['club_name'].strip()
        manager_name=request.POST['manager_name'].strip()
        email=request.POST['email'].strip()
        phone=request.POST['phone'].strip()
        country=request.POST['country'].strip()
        league=request.POST['league'].strip()
        club_budget=request.POST['club_budget']
        established_year=request.POST['established_year']
        stadium=request.POST['stadium'].strip()
        username=request.POST['username'].strip()
        password=request.POST['password']

        club_logo=request.FILES.get('club_logo')

        if Login.objects.filter(username=username).exists():
            messages.error(request,"Username already exists.")
            return redirect("register_club_manager")

        if Club_Manager.objects.filter(email=email).exists():
            messages.error(request,"Email already exists.")
            return redirect("register_club_manager")

        if len(phone)!=10 or not phone.isdigit():
            messages.error(request,"Enter valid 10 digit phone number.")
            return redirect("register_club_manager")

        current_year=datetime.now().year

        if int(established_year)<1800 or int(established_year)>current_year:
            messages.error(request,"Invalid established year.")
            return redirect("register_club_manager")

        if len(password)<6:
            messages.error(request,"Password must contain minimum 6 characters.")
            return redirect("register_club_manager")

        login=Login.objects.create_user(
            username=username,
            password=password,
            usertype="club_manager",
            viewpassword=password,
            is_active=False
        )

        Club_Manager.objects.create(

            login=login,

            club_name=club_name,
            manager_name=manager_name,
            email=email,
            phone=phone,

            country=country,
            league=league,

            club_budget=club_budget,

            established_year=established_year,

            stadium=stadium,

            club_logo=club_logo,
        )

        messages.success(request,"Registration Successful. Wait for Admin Approval.")

        return redirect("login")
    return render(request,"register_club_manager.html")

def admin_view_club_manager(request):
    clubs = Club_Manager.objects.all().order_by("-id")
    return render(request, "admin/admin_view_club_manager.html", {"clubs": clubs})

def admin_toggle_club_manager(request, id):
    club = get_object_or_404(Club_Manager, id=id)
    if club.login.is_active:
        club.login.is_active = False
        messages.success(request, "Club Manager Deactivated Successfully.")
    else:
        club.login.is_active = True
        messages.success(request, "Club Manager Activated Successfully.")
    club.login.save()
    return redirect("admin_view_club_manager")

def admin_delete_club_manager(request, id):
    club = get_object_or_404(Club_Manager, id=id)
    club.login.delete()     
    messages.success(request, "Club Manager Deleted Successfully.")
    return redirect("admin_view_club_manager")


def register_scout(request):
    login_id = request.session['login_id']
    club = Club_Manager.objects.get(login_id=login_id)
    if request.method == "POST":

        scout_name = request.POST['scout_name'].strip()
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        phone = request.POST['phone'].strip()
        experience = request.POST['experience']
        region = request.POST['region'].strip()

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register_scout")

        if Scout.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register_scout")

        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, "Enter valid phone number.")
            return redirect("register_scout")

        password = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=8
            )
        )

        login = Login.objects.create_user(
            username=username,
            password=password,
            usertype="scout",
            viewpassword=password,
            is_active=True
        )

        Scout.objects.create(
            login=login,
            club=club,
            scout_name=scout_name,
            email=email,
            phone=phone,
            experience=experience,
            region=region
        )

        subject = "Scout Login Credentials"

        message = f"""
Welcome to Football Recruitment Intelligence System.

Username : {username}

Password : {password}

Please login and change your password.

Thank You.
"""

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        messages.success(request, "Scout Registered Successfully.")
        return redirect("register_scout")
    scouts = Scout.objects.filter(club=club).order_by("-id")

    return render(request, "club_manager/register_scout.html", {
        "scouts": scouts
    })



def toggle_scout(request, id):
    login_id = request.session['login_id']
    club = Club_Manager.objects.get(login_id=login_id)
    scout = get_object_or_404(
        Scout,
        id=id,
        club=club
    )

    scout.login.is_active = not scout.login.is_active
    scout.login.save()
    return redirect("register_scout")


def delete_scout(request, id):
    login_id = request.session['login_id']
    club = Club_Manager.objects.get(login_id=login_id)
    scout = get_object_or_404(
        Scout,
        id=id,
        club=club
    )
    scout.login.delete()
    messages.success(request, "Scout Deleted Successfully.")
    return redirect("register_scout")



def club_manager_profile(request):
    login_id = request.session['login_id']
    club = Club_Manager.objects.get(login_id=login_id)
    if request.method == "POST":
        club.manager_name = request.POST['manager_name']
        club.email = request.POST['email']
        club.phone = request.POST['phone']
        club.country = request.POST['country']
        club.league = request.POST['league']
        club.club_budget = request.POST['club_budget']
        club.established_year = request.POST['established_year']
        club.stadium = request.POST['stadium']

        if 'club_logo' in request.FILES:
            club.club_logo = request.FILES['club_logo']
        club.save()
        messages.success(request,"Profile Updated Successfully")
        return redirect("club_manager_profile")
    return render(
        request,
        "club_manager/club_manager_profile.html",
        {"club":club}
    )

def scout_profile(request):
    login_id = request.session['login_id']
    scout = Scout.objects.get(login_id=login_id)
    if request.method == "POST":
        scout.scout_name = request.POST['scout_name']
        scout.email = request.POST['email']
        scout.phone = request.POST['phone']
        scout.experience = request.POST['experience']
        scout.region = request.POST['region']
        scout.save()
        messages.success(request,"Profile Updated Successfully")

        return redirect("scout_profile")
    return render(
        request,
        "scout/scout_profile.html",
        {"scout":scout}
    )

def admin_view_scouts(request):
    scouts = Scout.objects.select_related(
        'club',
        'login'
    ).order_by('-id')

    return render(
        request,
        "admin/admin_view_scouts.html",
        {"scouts": scouts}
    )

def admin_toggle_scout(request, id):
    scout = get_object_or_404(Scout, id=id)
    scout.login.is_active = not scout.login.is_active
    scout.login.save()
    if scout.login.is_active:
        messages.success(request, "Scout Activated Successfully.")
    else:
        messages.success(request, "Scout Deactivated Successfully.")
    return redirect("admin_view_scouts")

def admin_delete_scout(request, id):
    scout = get_object_or_404(Scout, id=id)
    scout.login.delete()
    messages.success(request, "Scout Deleted Successfully.")
    return redirect("admin_view_scouts")

from .predict import predict_player
def performance_prediction(request):

    result = None

    if request.method == "POST":

        player_name = request.POST["player_name"]

        result = predict_player(player_name)

        if result:

            scout = Scout.objects.get(
                login_id=request.session["login_id"]
            )

            PerformancePrediction.objects.create(

                scout=scout,

                player_name=result["player_name"],

                club=result["club"],

                nationality=result["nationality"],

                age=result["age"],

                position=result["position"],

                overall_rating=result["overall_rating"],

                predicted_rating=result["predicted_rating"],

                potential=result["potential"],

                pace=result["pace"],

                shooting=result["shooting"],

                passing=result["passing"],

                dribbling=result["dribbling"],

                defending=result["defending"],

                physical=result["physical"],

                goals=result["goals"],

                assists=result["assists"],

                market_value=result["market_value"]

            )

        else:

            messages.error(
                request,
                "Player Not Found."
            )

    return render(

        request,

        "scout/performance_prediction.html",
        {

            "result":result
        }
    )

from .recommendation import similar_players
import pandas as pd
import os
from django.http import JsonResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

csv_path = os.path.join(
    BASE_DIR,
    "dataset",
    "football_master_dataset.csv"
)

df = pd.read_csv(csv_path)


def similar_player_recommendation(request):

    result = None

    if request.method == "POST":

        player_name = request.POST.get("player_name")

        result = similar_players(player_name)

        if result:

            club_manager = Club_Manager.objects.get(
                login_id=request.session["login_id"]
            )

            SimilarPlayerRecommendation.objects.get_or_create(
                club_manager=club_manager,
                selected_player=player_name
            )

    return render(
        request,
        "club_manager/similar_player.html",
        {
            "result": result
        }
    )


def search_players(request):

    term = request.GET.get("term", "")

    players = (
        df[df["name"].str.contains(term, case=False, na=False)]
        ["name"]
        .drop_duplicates()
        .head(10)
        .tolist()
    )

    return JsonResponse(players, safe=False)


from .recruitment import recommend_players

def recruitment_recommendation(request):

    recommendations = None

    positions = [
        "GK",
        "CB",
        "LB",
        "RB",
        "CDM",
        "CM",
        "CAM",
        "LW",
        "RW",
        "ST"
    ]

    if request.method == "POST":

        position = request.POST["position"]
        max_age = int(request.POST["max_age"])
        min_rating = int(request.POST["min_rating"])

        recommendations = recommend_players(
            position,
            max_age,
            min_rating
        )

        club_manager = Club_Manager.objects.get(
            login_id=request.session["login_id"]
        )

        RecruitmentRecommendation.objects.get_or_create(

            club_manager=club_manager,

            position=position,

            max_age=max_age,

            min_rating=min_rating

        )

    return render(

        request,

        "club_manager/recruitment_recommendation.html",

        {

            "positions": positions,

            "recommendations": recommendations

        }

    )



from django.db.models import Count

def admin_stats(request):

    total_clubs = Club_Manager.objects.count()

    total_scouts = Scout.objects.count()

    total_predictions = PerformancePrediction.objects.count()

    total_similar = SimilarPlayerRecommendation.objects.count()

    total_recruitment = RecruitmentRecommendation.objects.count()

    # Club-wise Scouts
    club_data = Scout.objects.values(
        "club__club_name"
    ).annotate(
        total=Count("id")
    )

    club_names = []
    scout_counts = []

    for row in club_data:

        club_names.append(row["club__club_name"])

        scout_counts.append(row["total"])


    # Position Distribution
    position_data = PerformancePrediction.objects.values(
        "position"
    ).annotate(
        total=Count("id")
    )

    positions = []
    position_count = []

    for row in position_data:

        positions.append(row["position"])

        position_count.append(row["total"])


    # Similar Player Searches

    similar = SimilarPlayerRecommendation.objects.values(
        "selected_player"
    ).annotate(
        total=Count("id")
    ).order_by("-total")[:10]

    players=[]

    player_count=[]

    for row in similar:

        players.append(row["selected_player"])

        player_count.append(row["total"])


    # Recruitment

    recruitment = RecruitmentRecommendation.objects.values(
        "position"
    ).annotate(
        total=Count("id")
    )

    recruit_position=[]

    recruit_count=[]

    for row in recruitment:

        recruit_position.append(row["position"])

        recruit_count.append(row["total"])


    # Performance Rating

    excellent=PerformancePrediction.objects.filter(
        predicted_rating__gte=90
    ).count()

    verygood=PerformancePrediction.objects.filter(
        predicted_rating__gte=85,
        predicted_rating__lt=90
    ).count()

    good=PerformancePrediction.objects.filter(
        predicted_rating__gte=80,
        predicted_rating__lt=85
    ).count()

    average=PerformancePrediction.objects.filter(
        predicted_rating__gte=70,
        predicted_rating__lt=80
    ).count()

    poor=PerformancePrediction.objects.filter(
        predicted_rating__lt=70
    ).count()

    return render(

        request,

        "admin/admin_stats.html",

        {

            "total_clubs":total_clubs,

            "total_scouts":total_scouts,

            "total_predictions":total_predictions,

            "total_similar":total_similar,

            "total_recruitment":total_recruitment,

            "club_names":club_names,

            "scout_counts":scout_counts,

            "positions":positions,

            "position_count":position_count,

            "players":players,

            "player_count":player_count,

            "recruit_position":recruit_position,

            "recruit_count":recruit_count,

            "rating":[
                excellent,
                verygood,
                good,
                average,
                poor
            ]

        }

    )
