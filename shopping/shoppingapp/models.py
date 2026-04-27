from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUSer(AbstractUser):
    usertype=models.CharField(max_length=20,null=True)

class User(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    phone=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    age=models.IntegerField(null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    user=models.ForeignKey(CustomUSer,on_delete=models.CASCADE)


class Shop(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    phone=models.CharField(max_length=50)
    owner=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    licence=models.CharField(max_length=100,null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    image = models.FileField(upload_to='shop_images/', null=True)
    user=models.ForeignKey(CustomUSer,on_delete=models.CASCADE)

class Delivery_boy(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    phone=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    user=models.ForeignKey(CustomUSer,on_delete=models.CASCADE)
    shop=models.ForeignKey(Shop,on_delete=models.CASCADE,null=True)
    proof=models.FileField(null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    status=models.CharField(max_length=50,null=True,default="Pending")

class Products(models.Model):
    name=models.CharField(max_length=100,null=True)    
    type=models.CharField(max_length=100,null=True)    
    desc=models.CharField(max_length=500,null=True)    
    price=models.IntegerField(null=True)  
    discountprice=models.IntegerField(null=True)  
    qty=models.IntegerField(default=0)
    image=models.FileField(null=True)
    datetime=models.DateTimeField(null=True)
    fname=models.CharField(max_length=20,null=True)
    fnumber=models.CharField(max_length=20,null=True)
    user=models.ForeignKey(Shop,on_delete=models.CASCADE)

class Bookings(models.Model):
    cust=models.ForeignKey(User,on_delete=models.CASCADE)  
    Product=models.ForeignKey(Products,on_delete=models.CASCADE)   
    status=models.CharField(max_length=50,default="CART")
    count=models.IntegerField(default=1)
    book_date=models.DateTimeField(auto_now_add=True)
    payment_date=models.DateTimeField(null=True)
    total=models.IntegerField()
    boy=models.ForeignKey(Delivery_boy,on_delete=models.CASCADE,null=True)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE,null=True)
    card_number = models.TextField()   # encrypted
    expiry = models.TextField()        # encrypted
    cvv = models.TextField()           # encrypted
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    book = models.ForeignKey(Bookings,on_delete=models.CASCADE,null=True)
    sender =models.CharField(max_length=50,null=True)
    pdate = models.DateTimeField(auto_now_add=True)
    month = models.CharField(max_length=50,null=True)
    file = models.FileField(null=True)
    message = models.CharField(max_length=500,null=True)  


class Feedback(models.Model):
    date=models.DateTimeField(auto_now_add=True)
    book=models.ForeignKey(Bookings,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)     
    rating=models.IntegerField(null=True)
    review=models.CharField(max_length=300)

class Salary(models.Model):
    date=models.DateTimeField(auto_now_add=True)
    boy = models.ForeignKey(Delivery_boy,on_delete=models.CASCADE,null=True)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,null=True)
    amount = models.IntegerField(null=True)

        
# aa@mail.com - jpVjTbdH   
# cc@mail.com - WIu4Ldor

# bb@mail.com - BorAPYhz 
# zz@mail.com - AApixrIZ    
#  
# dd@mail.com - 7KAN7QvT
# db@mail.com - sq3OJbJe





#Tech Used : 

# Semantic Search using a pretrained deep learning model + cosine similarity
# model was trained by - Sentence Transformers
# pretrained AI model to convert text into vectors and compare them.



# For Recipie Search - content-based recommendation approach