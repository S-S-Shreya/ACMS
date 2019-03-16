from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Users)
admin.site.register(Documents)
admin.site.register(User_Document)
admin.site.register(Latest_Version)