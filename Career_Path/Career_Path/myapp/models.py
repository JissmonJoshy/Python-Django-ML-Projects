from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Login(AbstractUser):
    usertype = models.CharField(max_length=10, default='user')
    viewpassword = models.CharField(max_length=100, null=True)
    
class Tutor(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=255, null=True)
    qualification = models.CharField(max_length=100, null=True)
    proof= models.FileField(upload_to='tutor_proofs/', null=True, blank=True)
    certification = models.FileField(upload_to='tutor_certifications/', null=True, blank=True)
    img = models.FileField(upload_to='tutor_images/', null=True, blank=True)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Client(models.Model):
    name= models.CharField(max_length=100,null=True)
    email = models.EmailField()
    address = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=15, null=True)
    dob = models.DateField(null=True, blank=True)
    img= models.FileField(upload_to='client_images/', null=True, blank=True)
    loginid= models.ForeignKey(Login, on_delete=models.CASCADE, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Company(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    address = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=15, null=True)
    img= models.FileField(upload_to='company_images/', null=True, blank=True)
    loginid= models.ForeignKey(Login, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    proof = models.FileField(upload_to='company_proofs/', null=True, blank=True)
    certification = models.FileField(upload_to='company_certifications/', null=True, blank=True)

    

class Course(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100,null=True)
    duration = models.CharField(max_length=50, null=True)
    fees=models.CharField(max_length=20, null=True)
    img= models.FileField(upload_to='course_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True)
    clients = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    
class Enrollment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='applied')
    meet_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Notes(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    file = models.FileField(upload_to='notes/')
    created_at = models.DateTimeField(auto_now_add=True)

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('internship', 'Internship'),
        ('fulltime', 'Full Time'),
        ('parttime', 'Part Time'),
    ]
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True, blank=True)
    location = models.CharField(max_length=100, null=True)
    salary = models.CharField(max_length=20, null=True)
    img = models.FileField(upload_to='job_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='fulltime')  # ✅ NEW
    


class JobApply(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)
    cv = models.FileField(upload_to='cvs/')
    status = models.CharField(max_length=20, default='Applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    meet_link = models.URLField(null=True, blank=True)  # ✅ NEW

class JobFeedback(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=5,null=True)


class ClientInterest(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    interest=models.CharField(max_length=100, null=True, blank=True)
    Age= models.CharField(max_length=10, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    hobbies = models.CharField(max_length=100, null=True, blank=True)
    fav_subject = models.CharField(max_length=100, null=True, blank=True)
    ten_mark=models.CharField(max_length=200,null=True)
    mark=models.CharField(max_length=200,null=True)


class Feedback(models.Model):
    client=models.ForeignKey(Client,on_delete=models.CASCADE,null=True,blank=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    feedback=models.CharField(max_length=200,null=True)
    rating=models.CharField(max_length=200,null=True)

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class QuizAttempt(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    sender = models.ForeignKey(Login, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Login, on_delete=models.CASCADE, related_name="receiver")
    message = models.TextField()
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)