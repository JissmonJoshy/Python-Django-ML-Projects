from django.db import models

class Login(models.Model):
    email = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    userType = models.CharField(max_length=100, null=True)

class UserReg(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 
    status = models.CharField(max_length=20, default='Pending')

class FixedIncome(models.Model):
    user = models.ForeignKey(UserReg, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    addedDate = models.DateTimeField(auto_now_add=True) 
    frequency = models.CharField(max_length=50, choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ])


class OtherIncome(models.Model):
    user = models.ForeignKey(UserReg, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    addedDate = models.DateTimeField(auto_now_add=True)
    frequency = models.CharField(max_length=50, choices=[
        ('one_time', 'One-time'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ])

class FixedExpense(models.Model):
    user = models.ForeignKey(UserReg, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    # year = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=True)
    addedDate = models.DateTimeField(auto_now_add=True)
    frequency = models.CharField(max_length=50, choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ])

class OtherExpense(models.Model):
    user = models.ForeignKey(UserReg, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    addedDate = models.DateTimeField(auto_now_add=True)
    frequency = models.CharField(max_length=50, choices=[
        ('one-time', 'One-time'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ])  
   
class Uploadbill(models.Model):
    user = models.ForeignKey(UserReg, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    bill_receipt = models.FileField(upload_to='bills/', null=True, blank=True)
    addedDate = models.DateTimeField(auto_now_add=True)
    frequency = models.CharField(max_length=50, choices=[
        ('one-time', 'One-time'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ]) 