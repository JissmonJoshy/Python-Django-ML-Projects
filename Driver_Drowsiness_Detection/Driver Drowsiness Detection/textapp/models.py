
from django.db import models




class Driver(models.Model):
    dname=models.CharField(max_length=100,null=False, blank=False)
    daddress=models.CharField(max_length=100,null=False, blank=False)
    dcontact=models.CharField(max_length=100,null=False, blank=False)
    demail=models.CharField(max_length=100,null=False, blank=False)
    dpassword=models.CharField(max_length=100,null=False, blank=False)
    status=models.CharField(max_length=100,null=False, blank=False)


class Login(models.Model):
    username=models.CharField(max_length=100,blank=True)
    password=models.CharField(max_length=100,blank=True)
    usertype=models.CharField(max_length=100,blank=True)
    status=models.CharField(max_length=100,blank=True)
    driverid=models.ForeignKey(Driver,null=True,on_delete=models.CASCADE)



class User(models.Model):
    uname=models.CharField(max_length=100,blank=True)
    uaddress=models.CharField(max_length=100,blank=True)
    ucontact=models.CharField(max_length=100,blank=True)
    uemail=models.CharField(max_length=100,blank=True)
    upassword=models.CharField(max_length=100,blank=True)


class Booking(models.Model):
    uid=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    did=models.ForeignKey(Driver,null=True,on_delete=models.CASCADE)
    date=models.CharField(max_length=100,blank=True)
    status=models.CharField(max_length=100,blank=True)
    charge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class Feedback(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)