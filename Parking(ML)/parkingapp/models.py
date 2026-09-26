from django.db import models
from django.contrib.auth.models import User

# Admin !!!!!!!!!!!!!!!!
# username: admin@gmail.com
# password: admin


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Manager(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Amount(models.Model):
    type=models.CharField(max_length=20)
    price=models.IntegerField()
    man=models.ForeignKey(Manager,on_delete=models.CASCADE)

class Slot(models.Model):
    slot=models.IntegerField()
    type=models.CharField(max_length=20)
    price=models.IntegerField()
    status=models.CharField(max_length=20,default="Available")
    amount=models.ForeignKey(Amount,on_delete=models.CASCADE)

class Booking(models.Model):
    date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    slot=models.ForeignKey(Slot,on_delete=models.CASCADE)
    status=models.CharField(max_length=20)

class Complaint(models.Model):
    date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=300)
