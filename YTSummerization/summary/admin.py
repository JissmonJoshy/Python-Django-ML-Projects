from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Login)
admin.site.register(Video_History)
admin.site.register(Text_History)
admin.site.register(Feedback)
admin.site.register(Premium)

