from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
########ADMIN#########
#username: admin
#password: admin

class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)

class Club_Manager(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    club_name = models.CharField(max_length=150)
    manager_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    league = models.CharField(max_length=100)
    club_budget = models.DecimalField(max_digits=15, decimal_places=2)
    established_year = models.PositiveIntegerField()
    stadium = models.CharField(max_length=150)
    club_logo = models.ImageField(upload_to="club_logo/")
    created_at = models.DateTimeField(auto_now_add=True)

class Scout(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    club = models.ForeignKey(Club_Manager, on_delete=models.CASCADE)
    scout_name = models.CharField(max_length=100) 
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    experience = models.PositiveIntegerField(help_text="Years")
    region = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class PerformancePrediction(models.Model):
    scout = models.ForeignKey(Scout,on_delete=models.CASCADE)
    player_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=30,null=True, blank=True)
    overall_rating = models.FloatField(null=True, blank=True)
    predicted_rating = models.FloatField(null=True, blank=True)
    prediction_date = models.DateTimeField(auto_now_add=True)
    club = models.CharField(max_length=100,null=True, blank=True)
    nationality = models.CharField(max_length=100,null=True, blank=True)
    potential = models.FloatField(null=True, blank=True)
    pace = models.IntegerField(null=True, blank=True)
    shooting = models.IntegerField(null=True, blank=True)
    passing = models.IntegerField(null=True, blank=True)
    dribbling = models.IntegerField(null=True, blank=True)
    defending = models.IntegerField(null=True, blank=True)
    physical = models.IntegerField(null=True, blank=True)
    goals = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)
    market_value = models.BigIntegerField(null=True, blank=True)

class SimilarPlayerRecommendation(models.Model):

    club_manager = models.ForeignKey(
        Club_Manager,
        on_delete=models.CASCADE
    )

    selected_player = models.CharField(max_length=100)

    recommendation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('club_manager', 'selected_player')

    def __str__(self):
        return self.selected_player
    


class RecruitmentRecommendation(models.Model):

    club_manager = models.ForeignKey(
        Club_Manager,
        on_delete=models.CASCADE
    )

    position = models.CharField(max_length=20)

    max_age = models.IntegerField()

    min_rating = models.IntegerField()

    recommendation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "club_manager",
            "position",
            "max_age",
            "min_rating"
        )