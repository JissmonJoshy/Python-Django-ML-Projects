from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    viewpassword = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, blank=True, null=True)
    
class DataStorage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='processed_images/')
    orgImage = models.FileField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class DecUpload(models.Model):
    file = models.FileField(upload_to='dec_images/')
    created_at = models.DateTimeField(auto_now_add=True)

class ImgToImgEnc(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='img_to_img_enc/')
    created_at = models.DateTimeField(auto_now_add=True)
    output = models.FileField(upload_to='img_to_img_enc/', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    key = models.FileField(upload_to='img_to_img_enc/', null=True)

class ImgToImgDec(models.Model):
    file = models.FileField(upload_to='img_to_img_enc/')
    key = models.FileField(upload_to='img_to_img_enc/', null=True)


class EncodedText(models.Model):
    timeNow = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    encodeImage = models.ImageField(null=True, blank=True)
    inputImage = models.ImageField(null=True, blank=True)


class EncodedTextDec(models.Model):
    file = models.FileField(upload_to='img_to_img_enc/')