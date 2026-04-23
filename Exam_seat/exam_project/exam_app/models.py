from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='department/')

class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='course/')

class Semester(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester_no = models.CharField(max_length=10)  # Example: "1", "2", "3", "4"
    description = models.TextField()
    image = models.ImageField(upload_to='semester/', null=True, blank=True)

class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='subject/', null=True, blank=True)

class Student(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    address = models.TextField()
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='student/')
    register_no = models.CharField(max_length=20, unique=True, null=True, blank=True)
    face_encoding = models.BinaryField(null=True, blank=True)


class Staff(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True, blank=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    address = models.TextField()
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='staff/')
    



class Hall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    location = models.CharField(max_length=100)
    floor = models.CharField(max_length=20)
    image = models.ImageField(upload_to='hall/', null=True, blank=True)

class ExamSchedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class SeatAllocation(models.Model):
    exam = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    seat_number = models.IntegerField()

    class Meta:
        unique_together = ('exam', 'seat_number')
