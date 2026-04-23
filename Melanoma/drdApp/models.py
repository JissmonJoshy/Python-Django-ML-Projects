from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Max
# Create your models here.


class Users(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Questions(models.Model):
    question = models.CharField(max_length=100)
    o1 = models.CharField(max_length=100)
    o2 = models.CharField(max_length=100)
    
class Score(models.Model):
    date = models.DateField(auto_now_add=True)
    score = models.CharField(max_length=30)
    users = models.ForeignKey(Users, on_delete=models.CASCADE)

class ImageDetection(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    score = models.ForeignKey(Score, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="upload")
    resultVal = models.CharField(max_length=2000, null=True)
    result = models.JSONField()

class FeedbackSite(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

class Doctor(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.EmailField()
    qualification=models.CharField(max_length=100)
    experience=models.CharField(max_length=100)
    specialization=models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Booking(models.Model):
    bookeddate=models.DateField(auto_now_add=True)
    token=models.IntegerField(null=True, blank=True)
    uid=models.ForeignKey(Users,on_delete=models.CASCADE)
    docid=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    bookingdate=models.DateField()
    status=models.CharField(max_length=100)


class Payment(models.Model):
    bid=models.ForeignKey(Booking,on_delete=models.CASCADE)
    paydate=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=50)


class Prescription(models.Model):
    bid=models.ForeignKey(Booking,on_delete=models.CASCADE)
    image = models.ImageField()
    diagnosis = models.TextField()

class ChatAdmin(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    sendby = models.CharField(max_length=10, default="admin")