from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(UserRegister)
admin.site.register(LoginModule)
admin.site.register(AddPost)
admin.site.register(Payment)
admin.site.register(Chat)
admin.site.register(CareTaker)