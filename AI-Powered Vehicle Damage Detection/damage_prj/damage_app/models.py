from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
########ADMIN#########
#username: admin
#password: admin

class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)

class UserProfile(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class InsuranceProfile(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150)
    assessor_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    license_number = models.CharField(max_length=100, unique=True)
    profile_pic = models.ImageField(upload_to='insurance_profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Claim(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    insurance = models.ForeignKey(
        InsuranceProfile,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='claims/'
    )

    prediction = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    confidence = models.FloatField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
