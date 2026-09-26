from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Login(AbstractUser):
    usertype=models.CharField(max_length=50,null=True)
    view_password=models.CharField(max_length=50,null=True)

class User(models.Model):
    loginId = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    firstName = models.CharField(max_length=100, null=True)
    lastName = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    place = models.CharField(max_length=100, null=True)
    image = models.FileField(upload_to='user_images/', null=True, blank=True) 

class Owner(models.Model):
    loginId=models.ForeignKey(Login,on_delete=models.CASCADE,null=True)
    firstName = models.CharField(max_length=100, null=True)
    lastName = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    place = models.CharField(max_length=100, null=True)
    image = models.FileField(upload_to='file', null=True)
    status = models.CharField(max_length=20,default='Pending')


class Station(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)
    station_name = models.CharField(max_length=150, null=True)
    location = models.CharField(max_length=150, null=True)
    contact_number = models.CharField(max_length=15, null=True)
    licence_number=models.CharField(max_length=15, null=True)
    operating_hours = models.CharField(max_length=100, null=True)
    charging_types = models.CharField(max_length=200, null=True)
    image = models.FileField(upload_to='file', null=True)
    price=models.CharField(max_length=50,null=True)
    waiting_area = models.CharField(max_length=200, null=True)
    status=models.CharField(max_length=20,default='Pending')
    
class Booking(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, default='Booked')
    

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    # payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    receipt_image = models.ImageField(upload_to='payment_receipts/', null=True, blank=True)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    feedback = models.TextField(null=True, blank=True)