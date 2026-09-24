from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)

class MVD(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    profile_pic = models.ImageField(upload_to='mvd_profile/')
    job_post = models.CharField(max_length=100)
    address = models.TextField()
    dob = models.DateField()
    aadhar_image = models.ImageField(upload_to='mvd_aadhar/')
    gender = models.CharField(max_length=20)
    experience = models.CharField(max_length=100)
    joining_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='active')


class Prediction(models.Model):
    mvd = models.ForeignKey(MVD, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='predictions/')
    result = models.CharField(max_length=50)
    confidence = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.result