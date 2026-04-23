from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)

class UserDetail(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

class DieticianDetail(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    status = models.CharField(max_length=20, default='Pending')


class ExpertDetail(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    status = models.CharField(max_length=20, default='Pending')

class FitnessPlanImage(models.Model):
    expert = models.ForeignKey(Login, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='fitness_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class FitnessPlanVideo(models.Model):
    expert = models.ForeignKey(Login, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(upload_to='fitness_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class DietProgram(models.Model):
    expert = models.ForeignKey(Login, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class DietStep(models.Model):
    program = models.ForeignKey(DietProgram, on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField()
    instruction = models.TextField()


class UserDietProgram(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    program = models.ForeignKey(DietProgram, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

class UserStepProgress(models.Model):
    user_program = models.ForeignKey(UserDietProgram, on_delete=models.CASCADE)
    step = models.ForeignKey(DietStep, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

class HealthMetric(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    sellerid = models.ForeignKey(ExpertDetail, on_delete=models.CASCADE)
    customerid = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    time = models.CharField(max_length=100)
    utype = models.CharField(max_length=100)
# CUSTOMER = sender = reply(UserDetail)
# SELLER = reciever = chat(ExpertDetail)

class DietFeedback(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    program = models.ForeignKey(DietProgram, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class NutritionPlan(models.Model):
    dietician = models.ForeignKey(Login, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='diet_plans/')
    created_at = models.DateTimeField(auto_now_add=True)


class NutritionStep(models.Model):
    plan = models.ForeignKey(NutritionPlan, on_delete=models.CASCADE)
    step_title = models.CharField(max_length=100)
    step_description = models.TextField()
    step_image = models.ImageField(upload_to='diet_steps/', null=True, blank=True)


class NutritionJoinRequest(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    plan = models.ForeignKey(NutritionPlan, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        default='Pending'
    )  # Pending / Approved / Rejected
    created_at = models.DateTimeField(auto_now_add=True)

class StepCompletion(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    step = models.ForeignKey(NutritionStep, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'step')


class DieticianChat(models.Model):
    dietician = models.ForeignKey(DieticianDetail, on_delete=models.CASCADE)
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    time = models.CharField(max_length=100)
    utype = models.CharField(max_length=20)  # DIETICIAN / USER

class PlanFeedback(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    plan = models.ForeignKey(NutritionPlan, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1–5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'plan')


