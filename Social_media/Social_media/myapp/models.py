from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Login(AbstractUser):
    type = models.CharField(max_length=100, null=True)
    viewpass = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username


class Userreg(models.Model):
    name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)
    bio = models.CharField(max_length=500, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True, blank=True)
    following = models.IntegerField(null=True, blank=True, default=0)
    followers = models.IntegerField(null=True, blank=True, default=0)
    image = models.FileField(upload_to="profile", default="image")
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)


class Posts(models.Model):
    uid = models.ForeignKey(Userreg, on_delete=models.CASCADE, null=True)
    image = models.FileField(upload_to="posts")
    caption = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now=True)
    likes = models.IntegerField(null=True)
    comments = models.IntegerField(null=True)
    location = models.CharField(
        max_length=100, null=True, blank=True, default="No location"
    )
    status = models.CharField(max_length=50,default="good")
    
class Stories(models.Model):
    uid = models.ForeignKey(Userreg, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to="posts",null=True, blank=True)
    caption = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now=True)
    type=models.CharField(max_length=100, null=True, blank=True)


class Like(models.Model):
    liker = models.ForeignKey(Userreg, on_delete=models.CASCADE, null=True)
    pid = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)


class Comments_on_Posts(models.Model):
    uid = models.ForeignKey(Userreg, on_delete=models.CASCADE, null=True)
    pid = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now=True)


class Follow(models.Model):
    follower = models.ForeignKey(
        Userreg, on_delete=models.CASCADE, null=True, related_name="follower"
    )
    following = models.ForeignKey(
        Userreg, on_delete=models.CASCADE, null=True, related_name="fol"
    )


class Chat(models.Model):
    sender = models.ForeignKey(
        Userreg, on_delete=models.CASCADE, related_name="sent_user"
    )
    receiver = models.ForeignKey(
        Userreg, on_delete=models.CASCADE, related_name="received_user"
    )
    # sender_admin = models.ForeignKey(Login, null=True, blank=True, on_delete=models.CASCADE)
    content_type = models.CharField(
        max_length=100, choices=[("text", "Text"), ("file", "File")], default=None
    )
    message = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(
        auto_now_add=True  # Automatically set to current date and time on creation
    )

    def __str__(self):
        return self.message

class Friends_list(models.Model):
    user = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='friendship_user1')
    friend = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='friendship_user2')
    date_added = models.DateTimeField(auto_now_add=True)




class AdminChat(models.Model):
    sender_admin = models.ForeignKey(Login, on_delete=models.CASCADE, null=True, blank=True)
    sender_user = models.ForeignKey(Userreg, on_delete=models.CASCADE, null=True, blank=True)

    receiver_admin = models.ForeignKey(Login, on_delete=models.CASCADE, null=True, blank=True, related_name="admin_received")
    receiver_user = models.ForeignKey(Userreg, on_delete=models.CASCADE, null=True, blank=True, related_name="user_received")

    message = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    content_type = models.CharField(max_length=20)

    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)