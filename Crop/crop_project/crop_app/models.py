from django.db import models
from django.contrib.auth.models import AbstractUser

class Login(AbstractUser):
    usertype = models.CharField(max_length=50)
    viewpassword = models.CharField(max_length=50)

class Farmer(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to='farmer_images/', null=True, blank=True)


class Buyer(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class GovernmentOfficer(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=100)
    image = models.ImageField(upload_to='officers/')
    created_at = models.DateTimeField(auto_now_add=True)


class DeliveryBoy(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class SeedFertiliser(models.Model):
    officer = models.ForeignKey(GovernmentOfficer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='seeds_fertilisers/')
    quantity = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FarmerCart(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    product = models.ForeignKey(SeedFertiliser, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='cart')  # cart / paid
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_boy = models.ForeignKey(DeliveryBoy,on_delete=models.SET_NULL,null=True,blank=True)


class Product(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)


class ProductCart(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.SET_NULL, null=True, blank=True)

class ProductFeedback(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(ProductCart, on_delete=models.CASCADE)
    rating = models.IntegerField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class SeedFertiliserFeedback(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    product = models.ForeignKey(SeedFertiliser, on_delete=models.CASCADE)
    order = models.OneToOneField(FarmerCart, on_delete=models.CASCADE)
    rating = models.IntegerField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class FarmerOfficerChat(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    officer = models.ForeignKey(GovernmentOfficer, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    time = models.CharField(max_length=50)
    sender_type = models.CharField(max_length=20)  # FARMER / OFFICER


class FarmingAlert(models.Model):
    officer = models.ForeignKey(GovernmentOfficer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='farming_alerts/images/', null=True, blank=True)
    video = models.FileField(upload_to='farming_alerts/videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
