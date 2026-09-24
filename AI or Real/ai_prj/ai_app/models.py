from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
########ADMIN#########
#username: admin
#password: admin

class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)


class User(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    profile = models.ImageField(upload_to="users/")



class PredictionHistory(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    image = models.ImageField(upload_to='predictions/')

    prediction = models.CharField(max_length=50, blank=True, null=True)

    confidence = models.FloatField(null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)