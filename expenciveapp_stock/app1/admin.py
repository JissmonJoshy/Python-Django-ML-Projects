from django.contrib import admin
from . models import*

# Register your models here.
admin.site.register(Login)
admin.site.register(UserReg)
admin.site.register(FixedIncome)
admin.site.register(OtherIncome)
admin.site.register(FixedExpense)
admin.site.register(OtherExpense)
admin.site.register(Uploadbill)