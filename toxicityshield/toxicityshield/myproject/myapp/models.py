from django.db import models

# Create your models here.
class UserRegister(models.Model):
    uid=models.AutoField(primary_key=True)
    u_fullname=models.CharField(max_length=100)
    u_email=models.CharField(max_length=100)
    u_phone=models.CharField(max_length=100)
    u_address=models.CharField(max_length=100)
    u_pass=models.CharField(max_length=100)
    u_status=models.CharField(max_length=100,default="pending")
    u_profile=models.CharField(max_length=100)
    u_about=models.CharField(max_length=100)
    u_from=models.CharField(max_length=100)
    u_work=models.CharField(max_length=100)
    profile_image=models.FileField()
    post_image=models.FileField()
    u1=models.CharField(max_length=100,default="")
    u2=models.CharField(max_length=100,default="")
    u3=models.CharField(max_length=100,default="")
    u4=models.CharField(max_length=100,default="")
    

    


class LoginModule(models.Model):
    l_id=models.AutoField(primary_key=True)
    l_email=models.CharField(max_length=100) 
    l_pass=models.CharField(max_length=100) 
    l_type=models.CharField(max_length=100) 
    l_status=models.CharField(max_length=100)     

class AddPost(models.Model):
    post_id=models.AutoField(primary_key=True)
    post_desc=models.CharField(max_length=100) 
    post_image=models.FileField() 
    post_type=models.CharField(max_length=100) 
    post_status=models.CharField(max_length=100) 
    u5=models.CharField(max_length=100,default="normal")
    u6=models.CharField(max_length=100,default="")
    u7=models.CharField(max_length=100,default="")
    uid=models.ForeignKey(UserRegister,on_delete=models.CASCADE,blank=True,null=True)

class CareTaker(models.Model):
    care_id=models.AutoField(primary_key=True)
    care_fullname=models.CharField(max_length=100)
    care_email=models.CharField(max_length=100)
    care_phone=models.CharField(max_length=100)
    care_address=models.CharField(max_length=100)
    care_pass=models.CharField(max_length=100)
    care_status=models.CharField(max_length=100,default="pending")
    care_profile=models.CharField(max_length=100)
    care_image=models.FileField()
    u8=models.CharField(max_length=100,default="")
    u9=models.CharField(max_length=100,default="")
    u10=models.CharField(max_length=100,default="")
    


class Chat(models.Model):
    uid = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(CareTaker, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    time = models.CharField(max_length=100)
    utype = models.CharField(max_length=100)



class FeedBack(models.Model):
    feed_id=models.AutoField(primary_key=True)
    feed_name=models.CharField(max_length=100)
    feed_email=models.CharField(max_length=100)
    saysomething=models.CharField(max_length=100)
    f_status=models.CharField(max_length=100)
    u11=models.CharField(max_length=100,default="")
    u12=models.CharField(max_length=100,default="")
    uid=models.ForeignKey(UserRegister,on_delete=models.CASCADE,blank=True,null=True)    



class Payment(models.Model):
    payment_id=models.AutoField(primary_key=True) 
    
    total_price=models.CharField(max_length=100)
    card_number=models.CharField(max_length=100) 
    card_name=models.CharField(max_length=100) 
    exp_date=models.CharField(max_length=100) 
    cvv=models.CharField(max_length=100)   
    b_status=models.CharField(max_length=100,default="pending")
    uid=models.ForeignKey(UserRegister,on_delete=models.CASCADE,blank=True,null=True)
    care_id=models.ForeignKey(CareTaker,on_delete=models.CASCADE,blank=True,null=True)
    u13=models.CharField(max_length=100,default="")
    u14=models.CharField(max_length=100,default="")
    u15=models.CharField(max_length=100,default="")
    
    
class CounselingMessage(models.Model):
    id = models.AutoField(primary_key=True)
    uid=models.ForeignKey(UserRegister,on_delete=models.CASCADE,blank=True,null=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
class C(models.Model):
    uid=models.ForeignKey(UserRegister,on_delete=models.CASCADE,blank=True,null=True)
    message1 = models.TextField()
    sent_at1 = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(AddPost, on_delete=models.CASCADE)
    uid = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_status = models.CharField(max_length=100, default="normal")
