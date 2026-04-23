from django.db import models
from django.contrib.auth.models import AbstractUser

class Login(AbstractUser):
    usertype = models.CharField(max_length=50)
    viewpassword = models.CharField(max_length=50)

class User(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Doctor(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=255, null=True)
    experience = models.IntegerField(null=True)
    qualification = models.CharField(max_length=100,null=True)
    specialization = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.TimeField()

    consultation_fee = models.IntegerField(null=True, blank=True)

    status = models.CharField(max_length=20, default='Pending')  
    payment_status = models.CharField(max_length=20, default='Pending')  

    created_at = models.DateTimeField(auto_now_add=True)




class LeukemiaImage(models.Model):
    image = models.ImageField(upload_to='leukemia/')
    result = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.result