from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
########ADMIN#########
#username: admin
#password: admin

class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)

class Quality_Inspector(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    profile = models.ImageField(upload_to="quality_inspector/")

class Store_Manager(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    store_name = models.CharField(max_length=150)
    profile = models.ImageField(upload_to="store_manager/")


class PredictionHistory(models.Model):

    RESULT_CHOICES = (
        ("Fresh", "Fresh"),
        ("Rotten", "Rotten"),
    )

    CLASS_CHOICES = (
        ("Fresh Apple", "Fresh Apple"),
        ("Fresh Banana", "Fresh Banana"),
        ("Fresh Orange", "Fresh Orange"),
        ("Rotten Apple", "Rotten Apple"),
        ("Rotten Banana", "Rotten Banana"),
        ("Rotten Orange", "Rotten Orange"),
    )

    inspector = models.ForeignKey(
        Quality_Inspector,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="inspection_images/"
    )

    predicted_class = models.CharField(
        max_length=50,
        choices=CLASS_CHOICES
    )

    freshness = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES
    )

    confidence = models.FloatField()

    verified = models.BooleanField(default=False)

    verified_by = models.ForeignKey(
        Store_Manager,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    verified_date = models.DateTimeField(
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )


class InspectionReport(models.Model):

    prediction = models.OneToOneField(
        PredictionHistory,
        on_delete=models.CASCADE
    )

    report_number = models.CharField(
        max_length=30,
        unique=True
    )

    remarks = models.TextField()

    recommendation = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )