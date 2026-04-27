from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.




class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=15)



class User_profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    cycle_length = models.IntegerField(help_text="Average cycle length (days)")
    period_length = models.IntegerField(help_text="Period duration (days)")
    last_period_date = models.DateField()

    has_pcos = models.BooleanField(default=False)

    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    image = models.FileField(upload_to='user_images/', null=True, blank=True)

    def __str__(self):
        return self.name






class PeriodLog(models.Model):
    user = models.ForeignKey(User_profile, on_delete=models.CASCADE,null=True)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    flow = models.CharField(
        max_length=10,
        choices=[
            ('Light', 'Light'),
            ('Medium', 'Medium'),
            ('Heavy', 'Heavy')
        ]
    )

    def __str__(self):
        return f"{self.user.username} - {self.start_date}"



class SymptomLog(models.Model):
    user = models.ForeignKey(User_profile, on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True)

    hairfall = models.BooleanField(default=False)
    acne = models.BooleanField(default=False)
    pain = models.BooleanField(default=False)
    mood_swings = models.BooleanField(default=False)
    fatigue = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.date}"



class DietRemedy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=[('Diet', 'Diet'), ('Remedy', 'Remedy')]
    )

    def __str__(self):
        return self.title




class Doctor(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    qualification = models.CharField(max_length=100, null=True)
    experience = models.CharField(max_length=100, null=True)
    specialization = models.CharField(max_length=100, null=True)

    license_number = models.CharField(max_length=50,null=True, blank=True)
    license_document = models.FileField(upload_to='doctor_license/', null=True, blank=True)

    image = models.FileField(upload_to='doctor_images/', null=True, blank=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)




class Appointment(models.Model):

    user = models.ForeignKey(User_profile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    reason = models.TextField()

    report_file = models.FileField(upload_to='appointment_reports/', null=True, blank=True)

    # 🔹 Doctor Response
    home_remedies = models.TextField(null=True, blank=True)
    diet_plan = models.TextField(null=True, blank=True)
    doctor_notes = models.TextField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Completed', 'Completed'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.doctor.name} - {self.appointment_date}"