from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.

class CustomUser(AbstractUser):
    userType = models.CharField(blank=True,max_length=10)
    phone = models.CharField(max_length=15,null=True)
    address = models.TextField(null=True)
    city = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=50,null=True)
    zip = models.CharField(max_length=10,null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True)
    verification_image = models.ImageField(null=True)
    update_cou = models.IntegerField(default=0,null=True)
    last_update = models.DateTimeField(auto_now=True,null=True)
    account_balance = models.FloatField(default=0.0)

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    
    def update_user(self, first_name, last_name, email, phone, address, city, state, zip):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.update_cou += 1
        self.last_update = datetime.now()
        self.save()
    
    def change_password(self, password):
        self.set_password(password)
        self.save()

    def user_joined_this_year(self):
        return CustomUser.objects.filter(date_joined__year=datetime.now().year).count()
    
    def no_of_branches(self):
        return CustomUser.objects.filter(userType='Branch').count()
    
    def no_of_customers(self):
        return CustomUser.objects.filter(userType='Customer').count()

class Complaints(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    complaint = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.complaint[:50] + '...'
    
    def complaint_count(self):
        return Complaints.objects.all().count()
    
    def complaints_of_this_month(self):
        return Complaints.objects.filter(date__month=datetime.now().month).count()
    
    
class Atm_card_request(models.Model):
    branch = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='branch')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    card_type = models.CharField(max_length=50)
    request_date = models.DateTimeField(auto_now_add=True)
    branch_status = models.CharField(max_length=50, default='Pending')
    admin_status = models.CharField(max_length=50, default='Pending')
    cardno = models.CharField(max_length=16, null=True)
    expiry_date = models.DateField(null=True)
    cvv = models.CharField(max_length=3, null=True)
    card_issue_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.card_type + ' - ' + self.user.username
    
    def approved_requests(self):
        return Atm_card_request.objects.filter(status='Approved').count()
    
    def pending_requests(self):
        return Atm_card_request.objects.filter(status='Pending').count()
    
    def rejected_requests(self):
        return Atm_card_request.objects.filter(status='Rejected').count()
    
    def update_status(self, status):
        self.status = status
        self.save()

    def issue_card(self, cardno, expiry_date, cvv):
        self.cardno = cardno
        self.expiry_date = expiry_date
        self.cvv = cvv
        self.branch_status = 'Approved'
        self.card_issue_date = datetime.now()
        self.save()


class UserDeposits(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount) + ' - ' + self.user.username
    
    def deposit_count(self):
        return UserDeposits.objects.all().count()
    
    def deposits_of_this_month(self):
        return UserDeposits.objects.filter(date__month=datetime.now().month).count()
    
    def my_deposits(self, user):
        return UserDeposits.objects.filter(user=user).count
    
    def my_deposits_of_this_month(self, user):
        return UserDeposits.objects.filter(user=user, date__month=datetime.now().month).count()
    
    
class UserWithdrawals(models.Model):
    atmcard = models.ForeignKey(Atm_card_request, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    withdrawer_photo = models.ImageField(upload_to='withdrawer_photos', null=True)

    def __str__(self):
        return str(self.amount) 
    
    def withdrawal_count(self):
        return UserWithdrawals.objects.all().count()
    
    def withdrawals_of_this_month(self):
        return UserWithdrawals.objects.filter(date__month=datetime.now().month).count()
    
    def customer_withdrawals(self, user):
        return UserWithdrawals.objects.filter(atmcard__user=user).count()
    
    def customer_withdrawals_of_this_month(self, user):
        return UserWithdrawals.objects.filter(atmcard__user=user, date__month=datetime.now().month).count()
    
    def branceh_withdrawals(self, branch):
        return UserWithdrawals.objects.filter(atmcard__branch=branch).count()
    
    def branch_withdrawals_of_this_month(self, branch):
        return UserWithdrawals.objects.filter(atmcard__branch=branch, date__month=datetime.now().month).count()
    
    def crad_withdrawals(self, cardno):
        return UserWithdrawals.objects.filter(atmcard__cardno=cardno).count()
    
