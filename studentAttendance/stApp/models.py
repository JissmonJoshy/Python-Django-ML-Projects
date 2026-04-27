from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=15)


class Department(models.Model):
    department = models.CharField(max_length=50)


class Course(models.Model):
    course = models.CharField(max_length=50)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)


class Teacher(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Student(models.Model):
    admno = models.CharField(max_length=50, null=True, unique=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    acayear = models.CharField(max_length=50, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    face_encoding = models.BinaryField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='students/', null=True, blank=True)


class Attendance(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, null=True)
