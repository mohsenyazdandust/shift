from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

admin.site.register(User)
admin.site.register(File)
admin.site.register(BankInfo)
admin.site.register(Code)
admin.site.register(Shift)
admin.site.register(RequestEdit)
admin.site.register(ControlShift)
