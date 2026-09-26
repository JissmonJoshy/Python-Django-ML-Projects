from django.db import models
from django.contrib.auth.models import AbstractUser

###admin####

# username: admin
# password: admin

# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)


class User(models.Model):
    login = models.ForeignKey(Login,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to='users/')



class EmotionHistory(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    text = models.TextField()
    predicted_emotion = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)