from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(File)
admin.site.register(BankInfo)
admin.site.register(Code)
admin.site.register(Shift)
